import uuid
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import obter_configuracao
from app.features.auth.exceptions import AutenticacaoError
from app.features.auth.models import Usuario
from app.features.auth.types import UsuarioRepositoryProtocol

SECRET_KEY = obter_configuracao().jwt_secret_key
ALGORITHM = "HS256"
EXPIRACAO_TOKEN_MINUTOS = 480  # 8 horas, cobrindo um turno completo

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, repository: UsuarioRepositoryProtocol):
        self.repository = repository

    def primeiro_acesso(
        self, matricula: str, codigo_ativacao: str, pin: str
    ) -> Usuario:
        usuario = self.repository.buscar_por_matricula(matricula)

        if usuario is None:
            raise AutenticacaoError("Dados de ativação inválidos.")

        if usuario.pin_definido or usuario.codigo_ativacao_hash is None:
            raise AutenticacaoError("Dados de ativação inválidos.")

        if not pwd_context.verify(codigo_ativacao, usuario.codigo_ativacao_hash):
            raise AutenticacaoError("Dados de ativação inválidos.")

        pin_hash = pwd_context.hash(pin)
        return self.repository.ativar_usuario(usuario, pin_hash)

    def login(self, matricula: str, pin: str) -> str:
        usuario = self.repository.buscar_por_matricula(matricula)

        if usuario is None:
            raise AutenticacaoError("Matrícula ou PIN inválidos.")

        if not usuario.pin_definido:
            raise AutenticacaoError("Matrícula ou PIN inválidos.")

        if not pwd_context.verify(pin, usuario.senha_hash):
            raise AutenticacaoError("Matrícula ou PIN inválidos.")

        return self._gerar_token(usuario)

    def validar_token(self, token: str) -> Usuario:
        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM],
            )
            if "sub" not in payload or "exp" not in payload:
                raise KeyError("claims obrigatórias ausentes")
            usuario_id = uuid.UUID(payload["sub"])
        except (JWTError, KeyError, TypeError, ValueError):
            raise AutenticacaoError("Token inválido ou expirado.")

        usuario = self.repository.buscar_por_id(usuario_id)
        if usuario is None:
            raise AutenticacaoError("Token inválido ou expirado.")

        return usuario

    def _gerar_token(self, usuario: Usuario) -> str:
        expira_em = datetime.now(timezone.utc) + timedelta(
            minutes=EXPIRACAO_TOKEN_MINUTOS
        )
        payload = {
            "sub": str(usuario.id),
            "matricula": usuario.matricula,
            "exp": expira_em,
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

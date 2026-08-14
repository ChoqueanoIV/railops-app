from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.passagem import Linha, PassagemServico, Radio, Terminal


class LinhaRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_por_terminal(self, terminal: Terminal) -> list[Linha]:
        return (
            self.db.query(Linha)
            .filter(Linha.terminal == terminal)
            .order_by(Linha.codigo)
            .all()
        )


class RadioRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_ou_criar(self, numero: str) -> Radio:
        radio = self.db.query(Radio).filter(Radio.numero == numero).first()
        if radio is not None:
            return radio

        radio = Radio(numero=numero)
        self.db.add(radio)
        self.db.flush()
        return radio


class PassagemRepository:
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, passagem: PassagemServico) -> PassagemServico:
        try:
            self.db.add(passagem)
            self.db.commit()
            self.db.refresh(passagem)
            return passagem
        except SQLAlchemyError:
            self.db.rollback()
            raise

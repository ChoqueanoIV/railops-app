from app.features.auth.controller import router as feature_router
from app.features.auth.models import Usuario as FeatureUsuario
from app.features.auth.repository import UsuarioRepository as FeatureRepository
from app.features.auth.schemas import LoginRequest as FeatureLoginRequest
from app.features.auth.service import AuthService as FeatureAuthService
from app.models.usuario import Usuario as LegacyUsuario
from app.repositories.usuario_repository import UsuarioRepository as LegacyRepository
from app.routers.auth_router import router as legacy_router
from app.schemas.auth_schema import LoginRequest as LegacyLoginRequest
from app.services.auth_service import AuthService as LegacyAuthService


def test_adaptadores_legados_reexportam_a_feature_sem_duplicar_tipos():
    assert LegacyUsuario is FeatureUsuario
    assert LegacyRepository is FeatureRepository
    assert LegacyLoginRequest is FeatureLoginRequest
    assert LegacyAuthService is FeatureAuthService
    assert legacy_router is feature_router

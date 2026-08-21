from app.features.passagens.controller import router as feature_router
from app.features.passagens.models import PassagemServico as FeaturePassagemServico
from app.features.passagens.repository import (
    PassagemRepository as FeaturePassagemRepository,
)
from app.features.passagens.schemas import (
    PassagemBrisamarRequest as FeatureBrisamarRequest,
)
from app.features.passagens.service import PassagemService as FeaturePassagemService
from app.models.passagem import PassagemServico as LegacyPassagemServico
from app.repositories.passagem_repository import (
    PassagemRepository as LegacyPassagemRepository,
)
from app.routers.passagem_router import router as legacy_router
from app.schemas.passagem_schema import PassagemBrisamarRequest as LegacyBrisamarRequest
from app.services.passagem_service import PassagemService as LegacyPassagemService


def test_adaptadores_legados_reexportam_passagens_sem_duplicar_tipos():
    assert LegacyPassagemServico is FeaturePassagemServico
    assert LegacyPassagemRepository is FeaturePassagemRepository
    assert LegacyBrisamarRequest is FeatureBrisamarRequest
    assert LegacyPassagemService is FeaturePassagemService
    assert legacy_router is feature_router

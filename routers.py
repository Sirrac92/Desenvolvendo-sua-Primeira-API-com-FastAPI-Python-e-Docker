from fastapi import APIRouter
from atleta.controller import router as atleta
from categorias.controller import router as categoria
from centro_treinamento.controller import router as centro_treinamento




api_router = APIRouter()
api_router.include_router(atleta, prefix="/atleta", tags=["atletas"])
api_router.include_router(categoria, prefix="/categoria", tags=["categorias"])
api_router.include_router(centro_treinamento, prefix="/centros treinamento", tags=["centros treinamento"])




from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy import select
from centro_treinamento.models import CentroTrinamentoModel
from centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from contrib.repository.dependencias import DatabaseDependency

router = APIRouter()

@router.post(
    '/',
    summary="Create um novo centro de treinamento",
    status_code=status.HTTP_201_CREATED, 
    response_model=CentroTreinamentoOut,  
)

async def post(
    db_session: DatabaseDependency,
    centro_teinamento_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:   
    centro_trienamento_out = CentroTreinamentoOut(id=uuid4(), **centro_teinamento_in.model_dump())
    centro_treinamento_model = CentroTrinamentoModel(**centro_trienamento_out.model_dump())
    
    db_session.add(centro_treinamento_model)
    await db_session.commit()
    
    return centro_trienamento_out

@router.get(
    '/',
    summary="consultar todos os centros",
    status_code=status.HTTP_200_OK, 
    response_model=list[CentroTreinamentoOut],  
)

async def query(
    db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
    categorias: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTrinamentoModel))).scalar().all()
    
    return categorias

@router.get(
    '/{id}',
    summary="consulta um centro de treinamento pelo id",
    status_code=status.HTTP_200_OK, 
    response_model=CentroTreinamentoOut,  
)

async def query(id:UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    categoria: CentroTreinamentoOut = (await db_session.execute(select(CentroTrinamentoModel).filter_by(id=id))).scalar().first()
    
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='categoria nao encontrada no id:{id}')
        
    return categoria
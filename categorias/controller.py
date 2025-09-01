from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy import select
from categorias.models import CategoriaModel
from categorias.schemas import CategoriaIn, CategoriaOut
from contrib.repository.dependencias import DatabaseDependency

router = APIRouter()

@router.post(
    '/',
    summary="Create nova categoria",
    status_code=status.HTTP_201_CREATED, 
    response_model=CategoriaOut,  
)

async def post(
    db_session: DatabaseDependency,
    Categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:   
    categoria_out = CategoriaOut(id=uuid4(), **Categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    
    db_session.add(categoria_model)
    await db_session.commit()
    
    return categoria_out

@router.get(
    '/',
    summary="consultar todas as categorias",
    status_code=status.HTTP_200_OK, 
    response_model=list[CategoriaOut],  
)

async def query(
    db_session: DatabaseDependency) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalar().all()
    
    return categorias

@router.get(
    '/{id}',
    summary="consulta uma categoria pelo id",
    status_code=status.HTTP_200_OK, 
    response_model=CategoriaOut,  
)

async def query(id:UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalar().first()
    
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='categoria nao encontrada no id:{id}')
        
    return categoria
from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy import select
from atleta.models import AtletaModel
from atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from categorias.models import CategoriaModel
from centro_treinamento.models import CentroTrinamentoModel
from contrib.repository.dependencias import DatabaseDependency

router = APIRouter()

@router.post(
    '/',
    summary="Create novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=   AtletaOut 
)

async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaIn = Body(...)
):
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))).scalar().first()
    
    if not categoria:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='categoria nao encontrada no id:{id}')     
    
    centro_treinamento = (await db_session.execute(select(CentroTrinamentoModel).filter_by(nome=atleta_in.centro_treinamento.nome))).scalar().first()
    
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='centro de treinamento nao encontrada no id:{id}')     
    
    
    try:
        
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
    
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
    
        db_session.add(atleta_model)
        await db_session.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='ocorreu um erro ao inserir os dados no banco'
        )     
                
    return atleta_out

@router.get(
    '/',
    summary="consultar todos os atleta",
    status_code=status.HTTP_200_OK, 
    response_model=list[AtletaOut],  
)

async def query(
    db_session: DatabaseDependency) -> list[AtletaOut]:
    atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalar().all()
    
    return [AtletaOut.model_validate(atleta) for atleta in atletas]
 
@router.get(
    '/{id}',
    summary="consulta um atleta pelo id",
    status_code=status.HTTP_200_OK, 
    response_model=AtletaOut,  
)

async def query(id:UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalar().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Atleta nao encontrada no id:{id}')
        
    return atleta

@router.patch(
    '/{id}',
    summary="editar um atleta pelo id",
    status_code=status.HTTP_200_OK, 
    response_model=AtletaOut,  
)

async def query(id:UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalar().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Atleta nao encontrada no id:{id}')
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_up.item():
        setattr(atleta, key, value)
    
    await db_session.comit()
    await db_session.refresh(atleta)   
     
    return atleta

@router.delete(
    '/{id}',
    summary="deletar um atleta pelo id",
    status_code=status.HTTP_204_NO_CONTENT, 
)

async def query(id:UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalar().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Atleta nao encontrada no id:{id}')
    
    await db_session.delete(atleta)
    await db_session.commit()     
from pydantic import BaseModel, Field, PositiveFloat
from typing import Annotated, Optional
from categorias.schemas import CategoriaIn
from centro_treinamento.schemas import CentroTreinamentoAtleta
from contrib.schemas import BaseSchema, OutMixin

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", example="João Silva", max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", example="123.456.789-00", min_length=11, max_length=14)]
    idade: Annotated[int, Field(description="Idade do atleta", example=25)]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta em kg", example=75.5)]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta em metros", example=1.70)]
    sexo: Annotated[str, Field(description="Sexo do atleta", example="M", max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description='catgoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta,Field(description='centro de treinamento do atleta')]
 
class AtletaIn(Atleta):
    pass 
    
class AtletaOut(AtletaIn, OutMixin):
    pass

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description="Nome do atleta", example="João Silva", max_length=50)]
    idade: Annotated[Optional[int], Field(None, description="Idade do atleta", example=25)]
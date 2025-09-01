
from contrib.models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer



class CentroTrinamentoModel(BaseModel):
    __tablename__ = "centro_treinamento"
    
    pk_id = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50),unique=True, nullable=False)
    endereco: Mapped[str] = mapped_column(String(100), nullable=False)
    proprietario: Mapped[str] = mapped_column(String(50), nullable=False)
    atleta: Mapped['AtletaModel'] = relationship(back_populates="centro_treinamento")
    
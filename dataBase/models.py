from sqlalchemy import Column, Integer, String
from database import Base, engine

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)
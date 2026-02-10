from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./arqbanco.db"

maq = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
LocalConecao = sessionmaker(autocommit=False, autoflush=False, bind=maq)

Base = declarative_base()

class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    senha = Column(String)   # Aqui agora vai umz Hash gigante
    cpf = Column(String)
    nascimento = Column(String)
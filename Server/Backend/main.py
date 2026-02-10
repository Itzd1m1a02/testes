from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os

from database import maq, LocalConecao, UsuarioDB, Base

app = FastAPI()

basedir= os.path.abspath(os.path.dirname(__file__))
frontdir= os.path.join(basedir, '../Frontend') 

#Se nao tive, cria
Base.metadata.create_all(bind=maq)

def get_db():
    db = LocalConecao()
    try:
        yield db
    finally:
        db.close()

# PERMISSÃO (CORS): Necessário para o seu HTML falar com o Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, aqui iria apenas o endereço do seu site
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginSchema(BaseModel):
    email: str
    senha: str

app.mount("/static", StaticFiles(directory=frontdir), name="static") 

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(frontdir, "Login.html")) 



@app.post("/login")
def realizar_login(dados: LoginSchema, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == dados.email).first()
    if not usuario:
        return {"status": 404, "mensagem": "Quem cargas d'água é esse? Cadastre-se primeiro!"}
    if usuario.senha != dados.senha:
        return {"status": 401, "mensagem": "Desconfio mas nao posso provar... A senha esta errada"}
    return {"status": 200, "mensagem": "Ola, bem-vindo de volta"}

class CadastroSchema(BaseModel):
    email: str
    senha: str
    cpf: str
    nascimento: str

@app.post("/cadastro")
def processar_cadastro(dados: CadastroSchema, db: Session = Depends(get_db)):
    usuariojatem = db.query(UsuarioDB).filter(UsuarioDB.email == dados.email).first()
    if usuariojatem:
        return {"status": 400, "mensagem": "Eita, esse email ja ta em uso. Tente outro!"}
    
    novo_ze_ruela = UsuarioDB(
        email=dados.email,
        senha=dados.senha, #salva sha depois
        cpf=dados.cpf,
        nascimento=dados.nascimento
    )
    db.add(novo_ze_ruela)
    db.commit()
    db.refresh(novo_ze_ruela)
    print(f"Novo usuário add: {novo_ze_ruela.email}")
    return {"status": 201, "mensagem": "Cadastro realizado com sucesso! Agora é só fazer login, vai la ser feliz"}


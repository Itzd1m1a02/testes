from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

baseSO = os.path.abspath(os.path.dirname(__file__))
frontend_path = os.path.join(baseSO, "../Frontend")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginSchema(BaseModel):
    email: str
    senha: str

app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/L")
async def read_root():
    return FileResponse(os.path.join(frontend_path, "Login.html"))
@app.get("/C")
async def read_cadastro():
    return FileResponse(os.path.join(frontend_path, "Cadastro.html"))

@app.post("/login")
async def realizar_login(dados: LoginSchema):
    print(dados)
    print(f"E-mail recebido: {dados.email}")

    if dados.email == "joaozinho@email.com" and dados.senha == "123":
        return {"status": 200, "mensagem": "Login efetuado com sucesso!"}
    
    return {"status": 401, "mensagem": "Usuário ou senha incorretos."} 
@app.post("/cadastro")
async def realizar_cadastro(dados: LoginSchema):
    print(dados)
    print(f"E-mail recebido: {dados.email}")

    if dados.email and dados.senha:
        return {"status": 200, "mensagem": "Cadastro realizado com sucesso!"}
    
    return {"status": 400, "mensagem": "Dados de cadastro inválidos."}


from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

basedir= os.path.abspath(os.path.dirname(__file__))
frontdir= os.path.join(basedir, '../Frontend') 

# PERMISSÃO (CORS): Necessário para o seu HTML falar com o Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, aqui iria apenas o endereço do seu site
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definimos a estrutura que o JSON deve ter
class LoginSchema(BaseModel):
    email: str
    senha: str

app.mount("/static", StaticFiles(directory=frontdir), name="static") 

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(frontdir, "Login.html")) 



@app.post("/login")
def realizar_login(dados: LoginSchema):
    # O JSON chega aqui já convertido em objeto 'dados'
    print(dados) # Imprime o objeto completo
    print(f"E-mail recebido: {dados.email}")
    
    # Simulação de verificação
    if dados.email == "joaozinho@email.com" and dados.senha == "123":
        return {"status": 200, "mensagem": "Login efetuado com sucesso!"}
    
    return {"status": 401, "mensagem": "Usuário ou senha incorretos."}

class CadastroSchema(BaseModel):
    email: str
    senha: str
    cpf: str
    nascimento: str

@app.post("/cadastro")
def processar_cadastro(dados: CadastroSchema):
    print(f"Novo cadastro: {dados.email}, CPF: {dados.cpf}")
    return {"status": 200, "mensagem": "Cadastro realizado com sucesso!"}


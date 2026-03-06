from fastapi import FastAPI, HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel, EmailStr # EmailStr valida se o formato é de email real
import auth_engine as a
import database as db

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="SafePass API")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class UserCredentials(BaseModel):
    email: EmailStr # Se quiser validar mesmo, use EmailStr (precisa instalar: pip install pydantic[email])
    password: str

@app.post("/register", status_code=201) # 201 é o código HTTP para "Created"
@limiter.limit("5/minute")
def register(request: Request, user: UserCredentials):
    # O Pydantic já transformou o JSON em objeto, acessamos com user.email
    password_hash = a.hash_password(user.password)
    sucesso = db.salvar_usuario(user.email, password_hash)

    if not sucesso:
        # 400 indica que a requisição do cliente foi ruim (usuário já existe)
        raise HTTPException(status_code=400, detail="Usuário já cadastrado ou dados inválidos.")
    
    return {"message": "Usuário cadastrado com sucesso!"}

@app.post("/login", status_code=200)
@limiter.limit("5/minute")
def login(request: Request, user: UserCredentials):
    hash_salvo = db.buscar_usuario(user.email)

    if not hash_salvo:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    # IMPORTANTE: Passamos a senha BRUTA (user.password) e o HASH DO BANCO
    if a.verify_password(user.password, hash_salvo):
        return {
            "status": "success", 
            "message": "Login realizado!",
            "token": "fake-jwt-token-para-estudo" 
        }
    else:
        # 401 é o código padrão para falha de autenticação
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
    
@app.get("/buscar", status_code=200)
@limiter.limit("5/minute")
def buscar_email(request: Request, email: EmailStr):
    if db.verificar_email(email):
        return {
            "status": "sucess",
            "message": "Email encontrado com sucesso",
            "token": "fake-jwt-token-para-estudo"
        }
import jwt
import bcrypt
import os
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")

def criar_token_jwt(dados: dict):
    expiracao = datetime.utcnow() + timedelta(hours=2)
    dados.update({"exp": expiracao})
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)

def verificar_senha(senha, senha_hash):
    return bcrypt.checkpw(senha.encode(), senha_hash.encode())

def gerar_senha_hash(senha):
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

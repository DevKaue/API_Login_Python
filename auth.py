import jwt
import bcrypt
import os
from datetime import datetime, timedelta

from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

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

#Fazendo a validação do Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verificar_token(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
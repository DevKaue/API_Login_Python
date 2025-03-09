from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import requests
from sqlalchemy.orm import Session
from database import SessionLocal
from dataBase.models import Usuario
from Schemas.schemas import UsuarioCreate, UsuarioResponse, LoginSchema, UsuarioBase
from auth import criar_token_jwt, verificar_senha, gerar_senha_hash, verificar_token

router = APIRouter()

# Dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(login_data: LoginSchema, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == login_data.email).first()
    if not usuario or not verificar_senha(login_data.senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")

    token = criar_token_jwt({"sub": usuario.email})
    return {"token": token}

@router.post("/validate_token")
def validate_token(token: str, db: Session = Depends(get_db)):
    try:
        payload = verificar_token(token)
        email = payload["sub"]
        user = db.query(Usuario).filter(Usuario.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return {"valid": True, "user_id": user.id}

    except HTTPException:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    except Exception as e:
       raise HTTPException(status_code=500, detail="Erro ao validar o token")

@router.post("/auth/registrar", response_model=UsuarioResponse)
def registrar(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(status_code=400, detail="Usuário já existe.")

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=gerar_senha_hash(usuario.senha)
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.get("/GetUsuarios", response_model=list[UsuarioResponse],
            dependencies=[Depends(verificar_token)])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@router.put("/UpdateUsuariosById/{id}", response_model=UsuarioResponse,
            dependencies=[Depends(verificar_token)])
def atualizar_usuario(id: int, usuario_update: UsuarioBase, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    usuario.nome = usuario_update.nome
    usuario.email = usuario_update.email
    #Retirada da obrigatoriedade da senha
    #usuario.senha = gerar_senha_hash(usuario_update.senha)

    db.commit()
    db.refresh(usuario)
    return usuario

@router.delete("/DeleteUsuariosById/{id}", dependencies=[Depends(verificar_token)])
def deletar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    db.delete(usuario)
    db.commit()
    return {"message": "Usuário deletado com sucesso."}

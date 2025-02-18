from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from dataBase.models import Usuario, Base
from dataBase.schemas import UsuarioCreate, UsuarioResponse, LoginSchema
from auth import criar_token_jwt, verificar_senha, gerar_senha_hash

router = APIRouter()

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)


# Dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


@router.post("/auth/login")
def login(login_data: LoginSchema, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == login_data.email).first()
    if not usuario or not verificar_senha(login_data.senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")

    token = criar_token_jwt({"sub": usuario.email})
    return {"token": token}


@router.get("/GetUsuarios", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


@router.put("/GetUsuariosById/{id}", response_model=UsuarioResponse)
def atualizar_usuario(id: int, usuario_update: UsuarioCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    usuario.nome = usuario_update.nome
    usuario.email = usuario_update.email
    usuario.senha = gerar_senha_hash(usuario_update.senha)

    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/DeleteUsuariosById/{id}")
def deletar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    db.delete(usuario)
    db.commit()
    return {"message": "Usuário deletado com sucesso."}

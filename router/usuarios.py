from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import models
from schemas import schemas
from config.db import SessionLocal
import bcrypt

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#obtener un usuario por id
@router.get("/{usuario_id}", response_model=schemas.Usuario)
def get_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id_usr == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return db_usuario


#obtener un usuario por nombre
@router.get("/nombre/{nombre_usr}", response_model=schemas.Usuario)
def get_usuario(nombre_usr: str, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.nombre == nombre_usr).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return db_usuario

#obtener un usuario por nombre de usuario
@router.get("/nombre/{nombre_usr}", response_model=schemas.Usuario)
def get_usuario(nombre_usr: str, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.username == nombre_usr).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return db_usuario

# buscar usuario por nombre de usuario y password
@router.post("/login", response_model=schemas.Usuario)
def login(usuario: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.username == usuario.username).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    if not bcrypt.checkpw(usuario.password.encode('utf-8'), db_usuario.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Invalid password")
    return db_usuario



@router.post("/", response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(usuario.password.encode('utf-8'), bcrypt.gensalt())
    usuario.password = hashed_password.decode('utf-8')
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.get("/", response_model=List[schemas.Usuario])
def get_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()


@router.get("/", response_model=List[schemas.Usuario])
def get_usuarios(db: Session = Depends(get_db)):
    db_usuarios = db.query(models.Usuario).all()
    for usuario in db_usuarios:
        # Si id_rol es None, asignar un valor por defecto
        if usuario.id_rol is None:
            usuario.id_rol = 1  # o cualquier valor por defecto
    return db_usuarios


@router.put("/{usuario_id}", response_model=schemas.Usuario)
def update_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id_usr == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")

    for key, value in usuario.dict().items():
        setattr(db_usuario, key, value)

    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.delete("/{usuario_id}", response_model=schemas.Usuario)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id_usr == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")

    db.delete(db_usuario)
    db.commit()
    return db_usuario

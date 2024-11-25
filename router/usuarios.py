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

 
#cambia el estado del usuario de activo o inactivo pasando parametro usuario_id y el estado true o false
@router.put("/estado/{usuario_id}", response_model=schemas.Usuario)
def update_estado_usuario(usuario_id: int, estado: bool, db: Session = Depends(get_db)):
    # Fetch the user by ID
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id_usr == usuario_id).first()
    
    # If the user does not exist, raise a 404 error
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    
    # Update the user's active status
    db_usuario.activo = estado
    db.commit()
    db.refresh(db_usuario)
    
    # Return the updated user
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
@router.post("/login/user/pass", response_model=schemas.Usuario)
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

#actualiza un usuario por id 
@router.put("/{usuario_id}", response_model=schemas.Usuario)
def update_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id_usr == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    
    # Actualizar los campos del usuario
    for key, value in usuario.dict().items():
        if key == "password" and value:  # Solo encriptar si la contraseña no está vacía
            hashed_password = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
            setattr(db_usuario, key, hashed_password.decode('utf-8'))
        elif key != "password":  # Para otros campos, simplemente actualízalos
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


#obtine el rol de un usuario
@router.get("/rol/{usuario_id}", response_model=schemas.Rol)
def get_rol(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id_usr == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    db_rol = db.query(models.Rol).filter(models.Rol.id_rol == db_usuario.id_rol).first()
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol not found")
    return db_rol
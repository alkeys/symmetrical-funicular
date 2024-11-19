from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import models
from schemas import schemas
from config.db import SessionLocal
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.Log])
def get_logs(db: Session = Depends(get_db)):
    return db.query(models.Log).all()


#obtener todos los log por por id usuario 
@router.get("/usuario/{usuario_id}", response_model=List[schemas.Log])
def get_logs_by_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_logs = db.query(models.Log).filter(models.Log.id_usr == usuario_id).all()
    if db_logs is None:
        raise HTTPException(status_code=404, detail="Logs not found")
    return db_logs

#obtener todos los log por por id usuario que tengan la clave de User login en description
@router.get("/usuario/{usuario_id}/login", response_model=List[schemas.Log])
def get_logs_by_usuario_login(usuario_id: int, db: Session = Depends(get_db)):
    db_logs = db.query(models.Log).filter(models.Log.id_usr == usuario_id).filter(models.Log.descripcion == "User login").all()
    if db_logs is None:
        raise HTTPException(status_code=404, detail="Logs not found")
    return db_logs

#obtener todos los log por por id usuario que tengan la clave de User logout en description
@router.get("/usuario/{usuario_id}/logout", response_model=List[schemas.Log])
def get_logs_by_usuario_logout(usuario_id: int, db: Session = Depends(get_db)):
    db_logs = db.query(models.Log).filter(models.Log.id_usr == usuario_id).filter(models.Log.descripcion == "User logout").all()
    if db_logs is None:
        raise HTTPException(status_code=404, detail="Logs not found")
    return db_logs
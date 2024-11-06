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


@router.post("/", response_model=schemas.Rol)
def create_rol(rol: schemas.RolCreate, db: Session = Depends(get_db)):
    db_rol = models.Rol(**rol.dict())
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol


@router.get("/", response_model=List[schemas.Rol])
def get_roles(db: Session = Depends(get_db)):
    return db.query(models.Rol).all()


@router.get("/{rol_id}", response_model=schemas.Rol)
def get_rol(rol_id: int, db: Session = Depends(get_db)):
    db_rol = db.query(models.Rol).filter(models.Rol.id_rol == rol_id).first()
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol not found")
    return db_rol


@router.put("/{rol_id}", response_model=schemas.Rol)
def update_rol(rol_id: int, rol: schemas.RolCreate, db: Session = Depends(get_db)):
    db_rol = db.query(models.Rol).filter(models.Rol.id_rol == rol_id).first()
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol not found")

    for key, value in rol.dict().items():
        setattr(db_rol, key, value)

    db.commit()
    db.refresh(db_rol)
    return db_rol


@router.delete("/{rol_id}", response_model=schemas.Rol)
def delete_rol(rol_id: int, db: Session = Depends(get_db)):
    db_rol = db.query(models.Rol).filter(models.Rol.id_rol == rol_id).first()
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol not found")

    db.delete(db_rol)
    db.commit()
    return db_rol

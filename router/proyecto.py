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


@router.post("/", response_model=schemas.Proyecto)
def create_proyecto(proyecto: schemas.ProyectoCreate, db: Session = Depends(get_db)):
    db_proyecto = models.Proyecto(**proyecto.dict())
    db.add(db_proyecto)
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto


@router.get("/{proyecto_id}", response_model=schemas.Proyecto)
def get_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    db_proyecto = db.query(models.Proyecto).filter(models.Proyecto.id_proyecto == proyecto_id).first()
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto not found")
    return db_proyecto


@router.get("/", response_model=List[schemas.Proyecto])
def get_proyectos(db: Session = Depends(get_db)):
    return db.query(models.Proyecto).all()


@router.put("/{proyecto_id}", response_model=schemas.Proyecto)
def update_proyecto(proyecto_id: int, proyecto: schemas.ProyectoCreate, db: Session = Depends(get_db)):
    db_proyecto = db.query(models.Proyecto).filter(models.Proyecto.id_proyecto == proyecto_id).first()
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto not found")

    for key, value in proyecto.dict().items():
        setattr(db_proyecto, key, value)

    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto


@router.delete("/{proyecto_id}", response_model=schemas.Proyecto)
def delete_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    db_proyecto = db.query(models.Proyecto).filter(models.Proyecto.id_proyecto == proyecto_id).first()
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto not found")

    db.delete(db_proyecto)
    db.commit()
    return db_proyecto

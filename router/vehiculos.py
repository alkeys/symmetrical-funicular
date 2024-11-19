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


@router.post("/", response_model=schemas.Vehiculo)
def create_vehiculo(vehiculo: schemas.VehiculoCreate, db: Session = Depends(get_db)):
    db_vehiculo = models.Vehiculo(**vehiculo.dict())
    db.add(db_vehiculo)
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo


@router.get("/", response_model=List[schemas.Vehiculo])
def get_vehiculos(db: Session = Depends(get_db)):
    return db.query(models.Vehiculo).all()


@router.get("/{vehiculo_id}", response_model=schemas.Vehiculo)
def get_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    db_vehiculo = db.query(models.Vehiculos).filter(models.Vehiculos.id_vehiculo == vehiculo_id).first()
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehiculo not found")
    return db_vehiculo


@router.put("/{vehiculo_id}", response_model=schemas.Vehiculo)
def update_vehiculo(vehiculo_id: int, vehiculo: schemas.VehiculoCreate, db: Session = Depends(get_db)):
    db_vehiculo = db.query(models.Vehiculos).filter(models.Vehiculos.id_vehiculo == vehiculo_id).first()
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehiculo not found")

    for key, value in vehiculo.dict().items():
        setattr(db_vehiculo, key, value)

    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo


@router.delete("/{vehiculo_id}", response_model=schemas.Vehiculo)
def delete_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    db_vehiculo = db.query(models.Vehiculos).filter(models.Vehiculos.id_vehiculo == vehiculo_id).first()
    if db_vehiculo is None:
        raise HTTPException(status_code=404, detail="Vehiculo not found")

    db.delete(db_vehiculo)
    db.commit()
    return db_vehiculo

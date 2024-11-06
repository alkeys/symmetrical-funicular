from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import models
from schemas import schemas
from config.db import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()  # Crear una sesión local correctamente
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Gasolinera)
def create_gasolineras(gasolineras: schemas.GasolineraCreate, db: Session = Depends(get_db)):
    db_gasolineras = models.Gasolinera(**gasolineras.dict())

    db.add(db_gasolineras)
    db.commit()
    db.refresh(db_gasolineras)
    return db_gasolineras


@router.get("/", response_model=List[schemas.Gasolinera])
def get_gasolineras(db: Session = Depends(get_db)):
    return db.query(models.Gasolinera).all()


@router.get("/{gasolineras_id}", response_model=schemas.Gasolinera)
def get_gasolineras_by_id(gasolineras_id: int, db: Session = Depends(get_db)):
    db_gasolineras = db.query(models.Gasolinera).filter(models.Gasolinera.id_gasolinera == gasolineras_id).first()
    if db_gasolineras is None:
        raise HTTPException(status_code=404, detail="Gasolinera not found")
    return db_gasolineras


@router.put("/{gasolineras_id}", response_model=schemas.Gasolinera)
def update_gasolineras(gasolineras_id: int, gasolineras: schemas.GasolineraCreate, db: Session = Depends(get_db)):
    db_gasolineras = db.query(models.Gasolinera).filter(models.Gasolinera.id_gasolinera == gasolineras_id).first()
    if db_gasolineras is None:
        raise HTTPException(status_code=404, detail="Gasolinera not found")

    for key, value in gasolineras.dict().items():
        setattr(db_gasolineras, key, value)

    db.commit()
    db.refresh(db_gasolineras)
    return db_gasolineras


@router.delete("/{gasolineras_id}", response_model=schemas.Gasolinera)
def delete_gasolineras(gasolineras_id: int, db: Session = Depends(get_db)):
    db_gasolineras = db.query(models.Gasolinera).filter(models.Gasolinera.id_gasolinera == gasolineras_id).first()
    if db_gasolineras is None:
        raise HTTPException(status_code=404, detail="Gasolinera not found")

    db.delete(db_gasolineras)
    db.commit()
    return db_gasolineras

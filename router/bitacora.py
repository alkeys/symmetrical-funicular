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


@router.post("/", response_model=schemas.Bitacora)
def create_bitacora(bitacora: schemas.BitacoraCreate, db: Session = Depends(get_db)):
    db_bitacora = models.Bitacora(**bitacora.dict())
    db.add(db_bitacora)
    db.commit()
    db.refresh(db_bitacora)
    return db_bitacora


@router.get("/", response_model=List[schemas.Bitacora])
def get_bitacoras(db: Session = Depends(get_db)):
    return db.query(models.Bitacora).all()


@router.get("/{bitacora_id}", response_model=schemas.Bitacora)
def get_bitacora(bitacora_id: int, db: Session = Depends(get_db)):
    db_bitacora = db.query(models.Bitacora).filter(models.Bitacora.id_bitacora == bitacora_id).first()
    if db_bitacora is None:
        raise HTTPException(status_code=404, detail="Bitacora not found")
    return db_bitacora


@router.put("/{bitacora_id}", response_model=schemas.Bitacora)
def update_bitacora(bitacora_id: int, bitacora: schemas.BitacoraCreate, db: Session = Depends(get_db)):
    db_bitacora = db.query(models.Bitacora).filter(models.Bitacora.id_bitacora == bitacora_id).first()
    if db_bitacora is None:
        raise HTTPException(status_code=404, detail="Bitacora not found")

    for key, value in bitacora.dict().items():
        setattr(db_bitacora, key, value)

    db.commit()
    db.refresh(db_bitacora)
    return db_bitacora


@router.delete("/{bitacora_id}", response_model=schemas.Bitacora)
def delete_bitacora(bitacora_id: int, db: Session = Depends(get_db)):
    db_bitacora = db.query(models.Bitacora).filter(models.Bitacora.id_bitacora == bitacora_id).first()
    if db_bitacora is None:
        raise HTTPException(status_code=404, detail="Bitacora not found")

    db.delete(db_bitacora)
    db.commit()
    return db_bitacora

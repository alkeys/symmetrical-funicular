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


@router.post("/", response_model=schemas.Log)
def create_log(log: schemas.LogCreate, db: Session = Depends(get_db)):
    db_log = models.Log(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


@router.get("/", response_model=List[schemas.Log])
def get_logs(db: Session = Depends(get_db)):
    return db.query(models.Log).all()


@router.get("/{log_id}", response_model=schemas.Log)
def get_log(log_id: int, db: Session = Depends(get_db)):
    db_log = db.query(models.Log).filter(models.Log.id_log == log_id).first()
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return db_log


@router.put("/{log_id}", response_model=schemas.Log)
def update_log(log_id: int, log: schemas.LogCreate, db: Session = Depends(get_db)):
    db_log = db.query(models.Log).filter(models.Log.id_log == log_id).first()
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")

    for key, value in log.dict().items():
        setattr(db_log, key, value)

    db.commit()
    db.refresh(db_log)
    return db_log


@router.delete("/{log_id}", response_model=schemas.Log)
def delete_log(log_id: int, db: Session = Depends(get_db)):
    db_log = db.query(models.Log).filter(models.Log.id_log == log_id).first()
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")

    db.delete(db_log)
    db.commit()
    return db_log

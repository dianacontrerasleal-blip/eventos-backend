from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db

app = FastAPI(title="Sistema de Gestión de Eventos API")

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Sistema de Gestión de Eventos Backend"}

# CRUD Eventos
@app.post("/eventos/", response_model=schemas.Evento)
def create_evento(evento: schemas.EventoCreate, db: Session = Depends(get_db)):
    new_evento = models.Evento(**evento.model_dump())
    db.add(new_evento)
    db.commit()
    db.refresh(new_evento)
    return new_evento

@app.get("/eventos/", response_model=List[schemas.Evento])
def read_eventos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Evento).offset(skip).limit(limit).all()

@app.get("/eventos/{evento_id}", response_model=schemas.Evento)
def read_evento(evento_id: int, db: Session = Depends(get_db)):
    db_evento = db.query(models.Evento).filter(models.Evento.id == evento_id).first()
    if db_evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return db_evento

@app.put("/eventos/{evento_id}", response_model=schemas.Evento)
def update_evento(evento_id: int, evento: schemas.EventoCreate, db: Session = Depends(get_db)):
    db_evento = db.query(models.Evento).filter(models.Evento.id == evento_id).first()
    if db_evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    for key, value in evento.model_dump().items():
        setattr(db_evento, key, value)
    db.commit()
    db.refresh(db_evento)
    return db_evento

@app.delete("/eventos/{evento_id}")
def delete_evento(evento_id: int, db: Session = Depends(get_db)):
    db_evento = db.query(models.Evento).filter(models.Evento.id == evento_id).first()
    if db_evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    db.delete(db_evento)
    db.commit()
    return {"ok": True}

# CRUD Boletos
@app.post("/boletos/", response_model=schemas.Boleto)
def create_boleto(boleto: schemas.BoletoCreate, db: Session = Depends(get_db)):
    new_boleto = models.Boleto(**boleto.model_dump())
    db.add(new_boleto)
    db.commit()
    db.refresh(new_boleto)
    return new_boleto

@app.get("/boletos/", response_model=List[schemas.Boleto])
def read_boletos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Boleto).offset(skip).limit(limit).all()

@app.get("/boletos/{boleto_id}", response_model=schemas.Boleto)
def read_boleto(boleto_id: int, db: Session = Depends(get_db)):
    db_boleto = db.query(models.Boleto).filter(models.Boleto.id == boleto_id).first()
    if db_boleto is None:
        raise HTTPException(status_code=404, detail="Boleto no encontrado")
    return db_boleto

@app.put("/boletos/{boleto_id}", response_model=schemas.Boleto)
def update_boleto(boleto_id: int, boleto: schemas.BoletoCreate, db: Session = Depends(get_db)):
    db_boleto = db.query(models.Boleto).filter(models.Boleto.id == boleto_id).first()
    if db_boleto is None:
        raise HTTPException(status_code=404, detail="Boleto no encontrado")
    for key, value in boleto.model_dump().items():
        setattr(db_boleto, key, value)
    db.commit()
    db.refresh(db_boleto)
    return db_boleto

@app.delete("/boletos/{boleto_id}")
def delete_boleto(boleto_id: int, db: Session = Depends(get_db)):
    db_boleto = db.query(models.Boleto).filter(models.Boleto.id == boleto_id).first()
    if db_boleto is None:
        raise HTTPException(status_code=404, detail="Boleto no encontrado")
    db.delete(db_boleto)
    db.commit()
    return {"ok": True}

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, schemas
from app.database import get_db

app = FastAPI(title="Sistema de Gestión de Eventos API")

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Sistema de Gestión de Eventos Backend"}

# CRUD Usuarios
@app.post("/usuarios/", response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    new_user = models.Usuario(**usuario.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/usuarios/", response_model=List[schemas.Usuario])
def read_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

@app.get("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@app.put("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def update_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for key, value in usuario.model_dump().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/usuarios/{usuario_id}")
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(db_user)
    db.commit()
    return {"ok": True}

# CRUD Eventos
@app.post("/eventos/", response_model=schemas.Evento)
def create_evento(evento: schemas.EventoCreate, db: Session = Depends(get_db)):
    new_evento = models.Evento(**evento.model_dump())
    db.add(new_evento)
    db.commit()
    db.refresh(new_evento)
    return new_evento

@app.get("/eventos/", response_model=List[schemas.Evento])
def read_eventos(skip: int = 0, limit: int = 100, ubicacion: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Evento)
    if ubicacion:
        query = query.filter(models.Evento.ubicacion.ilike(f"%{ubicacion}%"))
    return query.offset(skip).limit(limit).all()

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
    # Business Logic: Verify event exists and capacity is not full
    evento = db.query(models.Evento).filter(models.Evento.id == boleto.evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    # Check sold tickets count
    sold_tickets = db.query(models.Boleto).filter(models.Boleto.evento_id == boleto.evento_id).count()
    if sold_tickets >= evento.capacidad:
        raise HTTPException(status_code=400, detail="Capacidad máxima del evento alcanzada")
        
    usuario = db.query(models.Usuario).filter(models.Usuario.id == boleto.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

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
        
    # Check new event capacity if changed
    if boleto.evento_id != db_boleto.evento_id:
        evento = db.query(models.Evento).filter(models.Evento.id == boleto.evento_id).first()
        if not evento:
            raise HTTPException(status_code=404, detail="Nuevo evento no encontrado")
        sold_tickets = db.query(models.Boleto).filter(models.Boleto.evento_id == boleto.evento_id).count()
        if sold_tickets >= evento.capacidad:
            raise HTTPException(status_code=400, detail="Capacidad máxima del nuevo evento alcanzada")
            
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

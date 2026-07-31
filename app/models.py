from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class Evento(Base):
    __tablename__ = "eventos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    ubicacion = Column(String)
    capacidad = Column(Integer)

class Boleto(Base):
    __tablename__ = "boletos"

    id = Column(Integer, primary_key=True, index=True)
    evento_id = Column(Integer, index=True)
    nombre_comprador = Column(String, index=True)
    pagado = Column(Boolean, default=False)

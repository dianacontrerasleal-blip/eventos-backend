from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    
    boletos = relationship("Boleto", back_populates="usuario")

class Evento(Base):
    __tablename__ = "eventos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    ubicacion = Column(String)
    capacidad = Column(Integer)
    
    boletos = relationship("Boleto", back_populates="evento")

class Boleto(Base):
    __tablename__ = "boletos"

    id = Column(Integer, primary_key=True, index=True)
    evento_id = Column(Integer, ForeignKey("eventos.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    pagado = Column(Boolean, default=False)
    
    evento = relationship("Evento", back_populates="boletos")
    usuario = relationship("Usuario", back_populates="boletos")

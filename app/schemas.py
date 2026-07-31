from pydantic import BaseModel
from typing import Optional

class EventoBase(BaseModel):
    nombre: str
    ubicacion: str
    capacidad: int

class EventoCreate(EventoBase):
    pass

class Evento(EventoBase):
    id: int

    class Config:
        from_attributes = True

class BoletoBase(BaseModel):
    evento_id: int
    nombre_comprador: str
    pagado: bool = False

class BoletoCreate(BoletoBase):
    pass

class Boleto(BoletoBase):
    id: int

    class Config:
        from_attributes = True

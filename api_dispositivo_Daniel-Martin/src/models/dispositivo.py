from datetime import date
from sqlmodel import Field, SQLModel
from pydantic import BaseModel

class Dispositivo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, max_length=50)
    fecha_compra: date | None = Field(nullable=True)

# dto classes
class DispositivoCreate(BaseModel):
    nombre: str
    # fecha de estreno posterior a la fecha actual con Annotated
    fecha_compra: date | None = None

class DispositivoUpdate(BaseModel):
    nombre: str | None = None
    fecha_compra: date | None = None

class DispositivoResponse(BaseModel):
    id: int
    nombre: str
    fecha_compra: date | None = None

# mapping functions
def map_dispositivo_to_response(dispositivo: Dispositivo) -> DispositivoResponse:
    return DispositivoResponse(
        id=dispositivo.id,
        nombre=dispositivo.nombre,
        fecha_compra=dispositivo.fecha_compra
    )

def map_create_to_dispositivo(dispositivo_create: DispositivoCreate) -> Dispositivo:
    return Dispositivo(
        nombre=dispositivo_create.nombre,
        fecha_compra=dispositivo_create.fecha_compra
    )

def map_update_to_dispositivo(dispositivo: Dispositivo, dispositivo_update: DispositivoUpdate) -> Dispositivo:
    if dispositivo_update.nombre is not None:
        dispositivo.nombre = dispositivo_update.nombre
    if dispositivo_update.fecha_compra is not None:
        dispositivo.fecha_compra = dispositivo_update.fecha_compra
    return dispositivo
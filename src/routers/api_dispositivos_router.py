from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from sqlmodel import Session
from models.dispositivo import Dispositivo, DispositivoCreate, DispositivoResponse, map_dispositivo_to_response, map_create_to_dispositivo

from data.dispositivo_repository import DispositivoRepository
from data.db import init_db, get_session

router = APIRouter(prefix="/api/dispositivos", tags=["dispositivos"])

SessionDep = Annotated[Session, Depends(get_session)]

# Rutas de la API para gestionar dispositivos

@router.get("/", response_model=list[DispositivoResponse])
async def lista_dispositivos(session: SessionDep):
    repo = DispositivoRepository(session)
    dispositivos = repo.get_all_dispositivos()
    return [map_dispositivo_to_response(dispositivo) for dispositivo in dispositivos]   
@router.post("/", response_model=DispositivoResponse)
async def nuevo_dispositivo(dispositivo_create: DispositivoCreate, session: SessionDep):
    repo = DispositivoRepository(session)
    dispositivo = map_create_to_dispositivo(dispositivo_create)
    dispositivo_creado = repo.create_dispositivo(dispositivo)
    return map_dispositivo_to_response(dispositivo_creado)


@router.get("/{dispositivo_id}", response_model=DispositivoResponse)
async def dispositivo_por_id(dispositivo_id: int, session: SessionDep):
    repo = DispositivoRepository(session)
    dispositivo_encontrado = repo.get_dispositivo(dispositivo_id)
    if not dispositivo_encontrado:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return map_dispositivo_to_response(dispositivo_encontrado)
@router.delete("/{dispositivo_id}", status_code=204)
async def borrar_dispositivo(dispositivo_id: int, session: SessionDep):
    repo = DispositivoRepository(session)
    dispositivo_encontrado = repo.get_dispositivo(dispositivo_id)
    if not dispositivo_encontrado:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    repo.delete_dispositivo(dispositivo_id)
    return None


@router.patch("/{dispositivo_id}", response_model=DispositivoResponse)
async def cambia_dispositivo(dispositivo_id: int, dispositivo: Dispositivo, session: SessionDep):
    repo = DispositivoRepository(session)
    dispositivo_encontrado = repo.get_dispositivo(dispositivo_id)
    if not dispositivo_encontrado:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    dispositivo_data = dispositivo.model_dump(exclude_unset=True)
    dispositivo_encontrado.sqlmodel_update(dispositivo_data)
    repo.update_dispositivo(dispositivo_encontrado.id, dispositivo_data)
    return map_dispositivo_to_response(dispositivo_encontrado)

@router.put("/", response_model=DispositivoResponse)
async def cambia_dispositivo(dispositivo: Dispositivo, session: SessionDep):
    repo = DispositivoRepository(session)
    dispositivo_encontrado = repo.get_dispositivo(dispositivo.id)
    if not dispositivo_encontrado:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    dispositivo_data = dispositivo.model_dump()
    dispositivo_encontrado.sqlmodel_update(dispositivo_data)
    repo.update_dispositivo(dispositivo_encontrado.id, dispositivo_data)
    return map_dispositivo_to_response(dispositivo_encontrado)
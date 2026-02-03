from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

from models.dispositivo import Dispositivo, DispositivoCreate,DispositivoResponse, map_dispositivo_to_response, map_create_to_dispositivo
from data.db import init_db, get_session
from data.dispositivo_repository import DispositivoRepository


import uvicorn


@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    yield


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)



@app.get("/dispositivos", response_model=list[DispositivoResponse])
def lista_dispositivos(session: SessionDep):
    repo = DispositivoRepository(session)
    dispositivos = repo.get_all_dispositivos()
    return [map_dispositivo_to_response(dispositivo) for dispositivo in dispositivos]

@app.post("/dispositivos", response_model=DispositivoResponse)
def nuevo_dispositivo(dispositivo_create: DispositivoCreate, session: SessionDep):
    repo = DispositivoRepository(session)
    dispositivo = map_create_to_dispositivo(dispositivo_create)
    dispositivo_creado = repo.create_dispositivo(dispositivo)
    return map_dispositivo_to_response(dispositivo_creado)


@app.get("/dispositivos/{dispositivo_id}", response_model=DispositivoResponse)
def dispositivo_por_id(dispositivo_id: int, session: SessionDep):
    repo = DispositivoRepository(session)
    dispositivo_encontrado = repo.get_dispositivo(dispositivo_id)
    if not dispositivo_encontrado:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return map_dispositivo_to_response(dispositivo_encontrado)

@app.delete("/dispositivos/{dispositivo_id}", status_code=204)
def borrar_dispositivo(dispositivo_id: int, session: SessionDep):
    repo = DispositivoRepository(session)
    dispositivo_encontrado = repo.get_dispositivo(dispositivo_id)
    if not dispositivo_encontrado:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    repo.delete_dispositivo(dispositivo_id)
    return None


@app.patch("/dispositivos/{dispositivo_id}", response_model=DispositivoResponse)
def cambia_dispositivo(dispositivo_id: int, dispositivo: Dispositivo, session: SessionDep):
    repo = DispositivoRepository(session)
    dispositivo_encontrado = repo.get_dispositivo(dispositivo_id)
    if not dispositivo_encontrado:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    dispositivo_data = dispositivo.model_dump(exclude_unset=True)
    dispositivo_encontrado.sqlmodel_update(dispositivo_data)
    repo.update_dispositivo(dispositivo_encontrado.id, dispositivo_data)
    return dispositivo_encontrado

@app.put("/dispositivos", response_model=DispositivoResponse)
def cambia_dispositivo(dispositivo: Dispositivo, session: SessionDep):
    repo = DispositivoRepository(session)
    dispositivo_encontrado = repo.get_dispositivo(dispositivo.id)
    if not dispositivo_encontrado:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    dispositivo_data = dispositivo.model_dump()
    dispositivo_encontrado.sqlmodel_update(dispositivo_data)
    repo.update_dispositivo(dispositivo_encontrado.id, dispositivo_data)
    return dispositivo_encontrado


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)
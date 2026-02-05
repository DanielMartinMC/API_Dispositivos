from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select
import os
from models.dispositivo import Dispositivo, DispositivoCreate, DispositivoResponse, map_dispositivo_to_response, map_create_to_dispositivo
from data.db import init_db, get_session
from data.dispositivo_repository import DispositivoRepository
from routers.api_dispositivos_router import router as api_dispositivos_router


import uvicorn


@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    yield


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)

script_dir = os.path.dirname(__file__)

app.mount("/static", StaticFiles(directory=os.path.join(script_dir, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(script_dir, "templates"))

app.include_router(api_dispositivos_router)

# Ruta para la página principal
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})   

@app.get("/dispositivos", response_class=HTMLResponse)
async def ver_dispositivos(request: Request, session: SessionDep):
    repo = DispositivoRepository(session)
    dispositivos = repo.get_all_dispositivos()
    return templates.TemplateResponse("dispositivos/dispositivos.html", {"request": request, "dispositivos": dispositivos})

@app.get("/dispositivos/new", response_class=HTMLResponse)
async def nuevo_dispositivo_form(request: Request):

    """Formulario para añadir un dispositivo nuevo"""
    return templates.TemplateResponse("dispositivos/dispositivo_form.html", {
        "request": request,
        "dispositivo": Dispositivo()
    })

@app.post("/dispositivos/new", response_class=HTMLResponse)
async def crear_dispositivo(request: Request, session: SessionDep):
    """Crear un nuevo dispositivo desde el formulario"""
    form_data = await request.form()
    nombre = form_data.get("nombre")
    fecha_compra = form_data.get("fecha_compra")
    marca = form_data.get("marca")
    modelo = form_data.get("modelo") or None

    dispositivo_create = DispositivoCreate(
        nombre=nombre,
        fecha_compra=fecha_compra,
        marca=marca,
        modelo=modelo
    )
    repo = DispositivoRepository(session)
    dispositivo = map_create_to_dispositivo(dispositivo_create)
    repo.create_dispositivo(dispositivo)

    return RedirectResponse(url="/dispositivos", status_code=303)

@app.get("/dispositivos/{dispositivo_id}", response_class=HTMLResponse)
async def dispositivo_por_id(dispositivo_id: int, request: Request, session: SessionDep):
    repo = DispositivoRepository(session)
    dispositivo_encontrado = repo.get_dispositivo(dispositivo_id)
    if not dispositivo_encontrado:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    dispositivo_response = map_dispositivo_to_response(dispositivo_encontrado)
    return templates.TemplateResponse("dispositivos/dispositivo_detalle.html", {"request": request, "dispositivo": dispositivo_response})



if __name__ == "__main__":
    # Ejecutar desde la raíz del proyecto: uvicorn src.main:app --reload
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)
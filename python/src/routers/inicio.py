from fastapi import APIRouter, status
from typing import Dict

from src.modelos.informacion import Informacion

router_inicio=APIRouter(tags=["Inicio"])


@router_inicio.get("/", status_code=status.HTTP_200_OK, summary="Devuelve informacion de la API")
async def inicio()->Informacion:

	"""
    Devuelve un modelo Informacion con la informacion de la API.

    ## Respuesta

    200 (OK): Si se obtiene el mensaje de informacion correctamente

    - **Mensaje**: El mensaje de bienvenida (str).
    - **Version**: La version de la API (str).
    - **Descripcion**: La descripcion de la finalidad de la API (str).
    - **Documentacion**: La direccion de la documentacion de la API (str).
    """

	return Informacion(mensaje="¡Bienvenido a la REST API Partidos ATM con FastAPI!",
			         version="1.0.0",
			         descripcion="Esta API proporciona operaciones básicas para obtener los datos de los partidos del Club Atletico de Madrid. Todos los datos de los partidos y usuarios se guardan en una base de datos PostgreSQL.",
			         documentacion="/docs")

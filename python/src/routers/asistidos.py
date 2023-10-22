from fastapi import APIRouter, status, Depends, HTTPException
from typing import List, Dict
import uuid

from src.etl.src.database.conexion import Conexion
from src.etl.src.database.sesion import crearSesion

from src.modelos.token import Payload
from src.modelos.asistido import Asistido, AsistidoBBDD
from src.modelos.asistido_utils import obtenerObjetosAsistido

from src.autenticacion.auth_utils import decodificarToken

router_asistidos=APIRouter(prefix="/asistidos", tags=["Asistidos"])

@router_asistidos.get("", status_code=status.HTTP_200_OK, summary="Devuelve los partidos asistidos del usuario")
async def obtenerAsistidos(payload:Payload=Depends(decodificarToken), con:Conexion=Depends(crearSesion))->List[Asistido]:

	"""
	Devuelve el diccionario de los partidos asistidos del usuario.

	## Respuesta

	200 (OK): Si se obtienen los partidos asistidos del usuario correctamente

	- **Asistido**: El id del partido asistido (str).
	- **Fecha**: La fecha del partido asistido (str).
	- **Competicion**: La competicion del partido asistido (str).
	- **Rival**: El rival del partido asistido (str).
	- **Marcador**: El marcador del partido asistido (str).
	- **Resultado**: El resultado del partido asistido (str).
	- **Lugar**: El lugar del partido asistido (str).
	- **Comentarios**: Los comentarios del partido asistido (str).

	401 (UNAUTHORIZED): Si los datos no son correctos

	- **Mensaje**: El mensaje de la excepcion (str).

	404 (NOT FOUND): Si no se obtienen los partidos asistidos del usuario correctamente

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	asistidos=con.obtenerAsistidos(payload.sub)

	con.cerrarConexion()

	if asistidos is None:

		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asistidos no existentes")

	return obtenerObjetosAsistido(asistidos)

@router_asistidos.post("", status_code=status.HTTP_201_CREATED, summary="Crea un partido asistido")
async def crearAsistido(asistido:AsistidoBBDD, payload:Payload=Depends(decodificarToken), con:Conexion=Depends(crearSesion))->Dict:

	"""
	Crea un partido asistido y lo inserta en la BBDD.

	Devuelve un mensaje y el diccionario que representa el partido asistido creado.

	## Respuesta

	201 (CREATED): Si se crea el partido asistido correctamente

	- **Mensaje**: El mensaje de creacion correcto del partido asistido (str).

	400 (BAD REQUEST): Si no se crea el partido asistido correctamente

	- **Mensaje**: El mensaje de la excepcion (str).

	401 (UNAUTHORIZED): Si los datos no son correctos

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	if not con.existe_partido(asistido.id_partido):

		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Partido no existente")

	if con.existe_asistido(asistido.id_partido, payload.sub):

		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Asistido existente")

	con.insertarAsistido(uuid.uuid4().hex, asistido.id_partido, payload.sub, asistido.comentarios)

	con.aumentarAsistido(payload.sub)

	con.cerrarConexion()

	return {"mensaje":"Partido asistido creado correctamente"}
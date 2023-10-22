from fastapi import APIRouter, status, Depends, HTTPException
from typing import List, Dict

from src.etl.src.database.conexion import Conexion
from src.etl.src.database.sesion import crearSesion

from src.modelos.token import Payload

from src.autenticacion.auth_utils import decodificarToken

router_asistidos=APIRouter(prefix="/asistidos", tags=["Asistidos"])

@router_asistidos.get("", status_code=status.HTTP_200_OK, summary="Devuelve los partidos asistidos del usuario")
async def obtenerAsistidos(payload:Payload=Depends(decodificarToken), con:Conexion=Depends(crearSesion))->List[Dict]:

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

	401 (UNAUTHORIZED): Si los datos no son correctos

	- **Mensaje**: El mensaje de la excepcion (str).

	404 (NOT FOUND): Si no se obtienen los partidos asistidos del usuario correctamente

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	asistidos=con.obtenerAsistidos(payload.sub)

	con.cerrarConexion()

	if asistidos is None:

		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asistidos no existentes")

	return asistidos
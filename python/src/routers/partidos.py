from fastapi import APIRouter, status, Depends, Query
from typing import List, Dict

from src.etl.src.database.conexion import Conexion
from src.etl.src.database.sesion import crearSesion

from src.modelos.partido import Partido
from src.modelos.partido_utils import obtenerObjetosPartido

router_partidos=APIRouter(prefix="/partidos", tags=["Partidos"])


@router_partidos.get("", status_code=status.HTTP_200_OK, summary="Devuelve los partidos existentes")
async def obtenerPartidos(todo:bool=Query(False, description="Bool para obtener todos los registros"),
							saltar:int=Query(0, description="Numero de elementos para saltar", min=0),
                			limite:int=Query(20, description="Numero de elementos a obtener", min=1, max=100),
                			con:Conexion=Depends(crearSesion))->List[Partido]:

	"""
	Devuelve los diccionarios asociados a los partidos disponibles en la BBDD.

	## Parametros Query

	- **Todo**: El booleano para obtener todos los registros (bool).
	- **Saltar**: El numero de registros que quieres saltar (int).
	- **Limite**: El numero de registros limite que quieres obtener (int).

	## Respuesta

	200 (OK): Si se obtienen los partidos correctamente

	- **Id_partido**: El id del partido (int).
	- **Fecha**: La fecha del partido (str).
	- **Hora**: La hora del partido (str).
	- **Competicion**: La competicion del partido (str).
	- **Ronda**: La ronda de la competicion del partido (str).
	- **Lugar**: El lugar del partido (str).
	- **Rival**: El rival del ATM en el partido (str).
	- **Marcador**: El marcador del partido (str).
	- **Resultado**: El resultado del partido (str).
	- **Posesion**: La posesion del ATM en el partido (int).
	- **Publico**: El publico asistente al partido (int).
	- **Capitan**: El capitan del ATM en el partido (str).
	- **Arbitro**: El arbitro del partido (str).

	404 (NOT FOUND): Si no se obtienen los partidos correctamente

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	if todo:

		partidos=con.obtenerPartidos()

	else:

		partidos=con.obtenerPartidosRango(limite, saltar)

	con.cerrarConexion()

	return obtenerObjetosPartido(partidos)
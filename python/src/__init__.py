from fastapi import FastAPI
import time

from .metadata.confmetadata import *
from .routers.inicio import router_inicio
from .routers.partidos import router_partidos
from .routers.usuarios import router_usuarios

from .etl.src import ETLtemporada, ETLdesde
from .etl.src.database.conexion import Conexion
from .etl.src.temporada import Temporada

# Funcion para obtener la data de los partidos
def obtenerData()->None:

	con=Conexion()

	if con.tabla_vacia():

		print("Obtencion total de los datos")
		
		ETLdesde()

	else:

		fecha_mas_reciente=con.fecha_mas_reciente()

		temporada=Temporada.desde_fecha(fecha_mas_reciente)

		if Temporada.es_temporada_actual(fecha_mas_reciente):

			print("Obtencion de los datos de la temporada actual")

		else:

			print(f"Obtencion de los datos desde la temporada {temporada}")
	
		ETLdesde(temporada.ano1)

	con.cerrarConexion()

# Funcion para conectarte y obtener la data
def conectarObtenerData()->None:

	try:

		obtenerData()

	except AttributeError as e:

		print("Reconectando...")

		time.sleep(5)

		conectarObtenerData()

# Funcion para crear la app
def crearApp():

	conectarObtenerData()

	app=FastAPI(title=TITULO,
				description=DESCRIPCION,
				version=VERSION,
				contact=CONTACTO,
				license_info=LICENCIA)

	app.include_router(router_inicio)
	app.include_router(router_partidos)
	app.include_router(router_usuarios)

	return app
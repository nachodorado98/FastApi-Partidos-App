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

def main()->None:

	obtenerData()
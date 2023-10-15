import datetime
import time

from .etl import ETL
from .temporada import Temporada
from .excepciones import PaginaError, TablaError, TemporadaError

# Funcion para la ETL de una temporada
def ETLtemporada(anno:int)->None:

	etl=ETL(anno)

	print(etl.temporada)

	try:

		etl.pipelineETL()

	except PaginaError:

		print("Error en la pagina")

	except TablaError:

		print("Error en la tabla")

	except TemporadaError:

		print("Error en la temporada")

# Funcion para la ETL de todas las temporadas desde el año indicado
def ETLdesde(anno:int=1988)->None:

	for temporada in Temporada.generarTemporadas(anno):

		ETLtemporada(temporada.ano1)

		time.sleep(3)
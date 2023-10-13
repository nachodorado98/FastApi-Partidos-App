import datetime
import time

from .etl.src import crearETL
from .etl.src.excepciones import PaginaError, TablaError

def main():

	anno_actual=datetime.datetime.now().year

	for anno in range(1988, anno_actual+1):

		etl=crearETL(anno)

		print(etl.temporada)

		try:

			etl.pipelineETL()

		except PaginaError:

			print("Error en la pagina")

		except TablaError:

			print("Error en la tabla")

		time.sleep(5)
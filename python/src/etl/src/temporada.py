import datetime
from typing import List, Type

from .excepciones import TemporadaError

class Temporada:

	def __init__(self, ano_inicial:int)->None:

		self.__comprobarAnoInicial(ano_inicial)

		self.ano1=ano_inicial
		self.ano2=self.ano1+1
		self.anos=[self.ano1, self.ano2]

		self.temporada=self.__generarTemporada()

	# Metodo para comprobar el año inicial
	def __comprobarAnoInicial(self, ano_inicial:int)->None:

		ano_actual=datetime.datetime.now().year

		if ano_inicial>ano_actual:

			raise TemporadaError(ano_inicial)

	# Metodo para generar una temporada
	def __generarTemporada(self)->str:

		return f"{self.ano1}-{self.ano2}"

	# Metodo para generar las temporadas a partir de un año inicial
	@classmethod
	def generarTemporadas(cls:Type["Temporada"], ano_inicio:str)->List[Type["Temporada"]]:

		return [cls(ano) for ano in range(ano_inicio, datetime.datetime.now().year+1)]

	# Metodo para obtener la temporada por una fecha
	@classmethod
	def desde_fecha(cls:Type["Temporada"], fecha:datetime)->Type["Temporada"]:

		# La temporada sera la del año si es pasado julio o la del año anterior si es anterior o igual a julio
		return cls(fecha.year) if fecha.month>7 else cls(fecha.year-1)

	# Metodo para obtener la temporada actual
	@classmethod
	def temporada_actual(cls:Type["Temporada"])->Type["Temporada"]:

		return Temporada.desde_fecha(datetime.datetime.now())

	# Metodo para saber si es la temporada actual
	@staticmethod
	def es_temporada_actual(fecha:datetime)->bool:

		temporada_actual=Temporada.temporada_actual()

		if fecha.year not in temporada_actual.anos:

			return False

		elif fecha.year==temporada_actual.ano1 and fecha.month<=7:

			return False

		elif fecha.year==temporada_actual.ano2 and fecha.month>7:

			return False

		else:

			return True

	def __repr__(self)->str:

		return f"Temporada({self.temporada})"

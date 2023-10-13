import datetime
from typing import List, Type

class Temporada:

	def __init__(self, ano_inicial:int)->None:

		self.__comprobarAnoInicial(ano_inicial)

		self.ano1=ano_inicial
		self.ano2=self.ano1+1

		self.temporada=self.__generarTemporada()

	def __comprobarAnoInicial(self, ano_inicial:int)->None:

		ano_actual=datetime.datetime.now().year

		if ano_inicial>ano_actual:

			raise Exception("Error en el año inicial")

	def __generarTemporada(self)->str:

		return f"{self.ano1}-{self.ano2}"

	@classmethod
	def generarTemporadas(cls:Type["Temporada"], ano_inicio:str)->List[Type["Temporada"]]:

		return [cls(ano) for ano in range(ano_inicio, datetime.datetime.now().year+1)]

	def __repr__(self)->str:

		return f"Temporada({self.temporada})"

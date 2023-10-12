from bs4 import BeautifulSoup as bs4
import requests
from typing import Optional, List, Dict
import pandas as pd

from .excepciones import PaginaError, TablaError

class Scraper:

	def __init__(self, temporada:str)->None:

		self.temporada=temporada

		self.url=f"https://fbref.com/en/squads/db3b9613/{self.temporada}/Atletico-Madrid-Stats"

	# Metodo para obtener el HTML en forma de bs4 de la pagina
	def __realizarPeticion(self)->bs4:

		peticion=requests.get(self.url)

		if peticion.status_code!=200:

			print(peticion.status_code)
			
			raise PaginaError()

		return bs4(peticion.text,"html.parser")

	# Metodo para obtener la cabecera de la tabla
	def __obtenerCabecera(self, contenido:bs4)->List[str]:

		tabla=contenido.find(id="matchlogs_for")

		try:
	
			cabecera=tabla.find("thead").find("tr")

		except AttributeError as e:
			
			raise TablaError(self.temporada)
			
		return [columna.text for columna in cabecera.find_all("th")]

	# Metodo para obtener las filas de la tabla
	def __obtenerFilas(self, contenido:bs4)->List[bs4]:

		tabla=contenido.find(id="matchlogs_for")

		if tabla is None:

			raise TablaError(self.temporada)

		body=tabla.find("tbody")

		return body.find_all("tr")

	# Metodo para extraer los partidos
	def __extraerPartidos(self)->Optional[Dict]:

		contenido=self.__realizarPeticion()

		cabecera=self.__obtenerCabecera(contenido)

		filas=self.__obtenerFilas(contenido)

		# Funcion para extraer el contenido de las filas de la tabla
		def extraerData(fila:str)->List[str]:
		    
		    fecha=fila.find("th").text
		    
		    return [fecha]+[columna.text for columna in fila.find_all("td")]

		registros=list(map(extraerData, filas))

		return {"Cabecera":cabecera, "Registros":registros}

	# Metodo para obtener los partidos
	def obtenerPartidos(self)->pd.DataFrame:

		data=self.__extraerPartidos()

		return pd.DataFrame(data["Registros"], columns=data["Cabecera"])
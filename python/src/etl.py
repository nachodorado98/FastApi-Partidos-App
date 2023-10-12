import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from .scraper import Scraper
from .temporada import Temporada
from .excepciones import LimpiarError, AlmacenarError
from .config import COMPETICIONES, RONDAS, LUGARES, RESULTADOS

class ETL:

	def __init__(self, temporada:int)->None:

		self.temporada=Temporada(temporada)
		self.scraper=Scraper(self.temporada.temporada)
		self.tabla_cruda=None
		self.tabla_limpia=None

	# Metodo para extraer los partidos
	def extraer(self)->None:

		self.tabla_cruda=self.scraper.obtenerPartidos()

	# Metodo para limpiar los partidos
	def limpiar(self)->None:

		if self.tabla_cruda is None:

			raise LimpiarError()

		df=self.tabla_cruda.copy()

		df=df[["Date","Time","Comp","Round","Venue","Result","GF","GA","Opponent","Poss","Attendance","Captain","Referee"]]

		df.rename({"Date":"Fecha", "Time":"Hora", "Comp":"Competicion","Round":"Ronda", "Venue":"Lugar",
					"Result":"Resultado", "GF":"Goles Marcados", "GA":"Goles Recibidos", "Opponent":"Rival",
					"Poss":"Posesion", "Attendance":"Publico", "Captain":"Capitan", "Referee":"Arbitro"}, axis=1, inplace=True)

		df_jugados=df[df["Resultado"]!=""]

		df_jugados["Competicion"]=df_jugados["Competicion"].apply(lambda x: COMPETICIONES[x] if x in COMPETICIONES.keys() else x)

		# Funcion para limpiar la ronda
		def limpiarRonda(ronda:str)->str:
			
			if "Matchweek" in ronda:
				
				numero=ronda.split(" ")[1]
				
				return f"Jornada {numero}"
			
			elif "qualifying" in ronda:
				
				return "Fase previa"
			
			elif ronda in RONDAS.keys():
				
				return RONDAS[ronda]
			
			else:
				
				return ronda
			
		df_jugados["Ronda"]=df_jugados["Ronda"].apply(limpiarRonda)

		df_jugados["Lugar"]=df_jugados["Lugar"].apply(lambda x: LUGARES[x] if x in LUGARES.keys() else x)

		df_jugados["Resultado"]=df_jugados["Resultado"].apply(lambda x: RESULTADOS[x])

		df_jugados["Marcador"]=df_jugados["Goles Marcados"]+" - "+df_jugados["Goles Recibidos"]

		# Funcion para limpiar el equipo de la champions (eliminar abreviatura pais)
		def limpiarEquipoChampions(serie:pd.Series)->pd.Series:
			
			if serie["Competicion"] in ["Champions League", "Europa League"]:
				
				equipo_dividio=serie["Rival"].split(" ")[1:]
				
				equipo=" ".join(equipo_dividio)
				
				serie["Rival"]=equipo
				
			return serie

		df_jugados[["Competicion", "Rival"]]=df_jugados[["Competicion", "Rival"]].apply(limpiarEquipoChampions, axis=1)

		df_jugados["Posesion"]=df_jugados["Posesion"].replace("", "0")

		df_jugados["Posesion"]=df_jugados["Posesion"].astype(int)

		# Funcion para limpiar la cantidad de publico
		def limpiarPublico(cantidad:str)->int:

			try:
			
				cantidad_str=cantidad.replace(",", "")
			
				return int(cantidad_str)

			except ValueError:

				return 0

		df_jugados["Publico"]=df_jugados["Publico"].apply(limpiarPublico)

		self.tabla_limpia=df_jugados[["Fecha", "Hora", "Competicion", "Ronda", "Lugar", "Rival", "Marcador",
										"Resultado", "Posesion", "Publico", "Capitan", "Arbitro"]]

	# Metodo para almacenar los partidos
	def almacenar(self)->None:

		if self.tabla_limpia is None:

			raise AlmacenarError()

		df_final=self.tabla_limpia.copy()

		df_final.to_csv(f"Partidos_ATM_{self.temporada.temporada.replace('-','_')}.csv", index=False)
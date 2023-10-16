from typing import Dict, List

from .partido import Partido

# Funcion para obtener un objeto partido
def obtenerObjetoPartido(valores:Dict)->Partido:

	return Partido(id_partido=valores["id"],
					fecha=valores["fecha"].strftime("%d/%m/%Y"),
					hora=valores["hora"],
					competicion=valores["competicion"],
					ronda=valores["ronda"],
					lugar=valores["lugar"],
					rival=valores["rival"],
					marcador=valores["marcador"],
					resultado=valores["resultado"],
					posesion=valores["posesion"],
					publico=valores["publico"],
					capitan=valores["capitan"],
					arbitro=valores["arbitro"])

# Funcion para obtener varios objetos partido
def obtenerObjetosPartido(lista_valores:List[Dict])->List[Partido]:

	return [obtenerObjetoPartido(valor) for valor in lista_valores]
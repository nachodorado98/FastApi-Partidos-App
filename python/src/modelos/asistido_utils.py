from typing import Dict, List

from .asistido import Asistido

# Funcion para obtener un objeto asistido
def obtenerObjetoAsistido(valores:Dict)->Asistido:

	return Asistido(asistido=valores["asistido"],
					fecha=valores["fecha"].strftime("%d/%m/%Y"),
					competicion=valores["competicion"],
					rival=valores["rival"],
					marcador=valores["marcador"],
					resultado=valores["resultado"],
					lugar=valores["lugar"],
					comentarios=valores["comentarios"])

# Funcion para obtener varios objetos asistido
def obtenerObjetosAsistido(lista_valores:List[Dict])->List[Asistido]:

	return [obtenerObjetoAsistido(valor) for valor in lista_valores]
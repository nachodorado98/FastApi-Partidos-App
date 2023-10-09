from typing import List

from .temporada import Temporada

def crearTemporadas(ano:int)->List[Temporada]:

	return Temporada.generarTemporadas(ano)
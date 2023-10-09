from typing import List

from .temporada import Temporada
from .scraper import Scraper

def crearScraper(ano:int)->Scraper:

	temporada=Temporada(ano)

	return Scraper(temporada.temporada)
import pytest
from bs4 import BeautifulSoup as bs4
import pandas as pd

from src.scraper import Scraper
from src.excepciones import PaginaError, TablaError

def test_scraper_realizar_peticion_error():

	scraper=Scraper("2000-2001")

	with pytest.raises(PaginaError):

		scraper._Scraper__realizarPeticion()

def test_scraper_realizar_peticion(scraper):

	contenido=scraper._Scraper__realizarPeticion()

	assert isinstance(contenido, bs4)

def test_scraper_obtener_cabecera_error():

	scraper=Scraper("2001-2002")

	contenido=scraper._Scraper__realizarPeticion()

	with pytest.raises(TablaError):

		scraper._Scraper__obtenerCabecera(contenido)

def test_scraper_obtener_cabecera(scraper):

	contenido=scraper._Scraper__realizarPeticion()

	cabecera=scraper._Scraper__obtenerCabecera(contenido)

	assert len(cabecera)==19

def test_scraper_obtener_filas_error():

	scraper=Scraper("2001-2002")

	contenido=scraper._Scraper__realizarPeticion()

	with pytest.raises(TablaError):

		scraper._Scraper__obtenerFilas(contenido)

def test_scraper_obtener_filas(scraper):

	contenido=scraper._Scraper__realizarPeticion()

	filas=scraper._Scraper__obtenerFilas(contenido)

	assert len(filas)!=0

@pytest.mark.parametrize(["scraper_error", "error"],
	[
		(Scraper("2000-2001"), PaginaError),
		(Scraper("2001-2002"), TablaError)
	]
)
def test_scraper_obtener_registros_errores(scraper_error, error):

	with pytest.raises(error):

		scraper_error._Scraper__extraerPartidos()

def test_scraper_obtener_registros(scraper):

	registros=scraper._Scraper__extraerPartidos()

	assert "Cabecera" in registros
	assert "Registros" in registros

@pytest.mark.parametrize(["scraper_error", "error"],
	[
		(Scraper("2000-2001"), PaginaError),
		(Scraper("2001-2002"), TablaError)
	]
)
def test_scraper_obtener_partidos_errores(scraper_error, error):

	with pytest.raises(error):

		scraper_error.obtenerPartidos()

def test_scraper_obtener_partidos(scraper):

	df=scraper.obtenerPartidos()

	assert isinstance(df, pd.DataFrame)
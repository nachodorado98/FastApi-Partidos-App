import pytest
import pandas as pd
import os
import time

from src.scraper import Scraper
from src.temporada import Temporada
from src.etl import ETL
from src.excepciones import PaginaError, TablaError, LimpiarError, AlmacenarError

def test_crear_objeto_etl():

	etl=ETL(2023)

	assert isinstance(etl.temporada, Temporada)
	assert isinstance(etl.scraper, Scraper)
	assert etl.tabla_cruda is None
	assert etl.tabla_limpia is None

def test_etl_extraer_error_pagina():

	etl=ETL(2000)

	with pytest.raises(PaginaError):

		etl.extraer()

def test_etl_extraer_error_cabecera():

	etl=ETL(2001)

	with pytest.raises(TablaError):

		etl.extraer()

@pytest.mark.parametrize(["anno"],
	[(2023,),(2010,),(2005,),(2019,),(1999,)]
)
def test_etl_extraer(anno):

	etl=ETL(anno)

	etl.extraer()

	assert isinstance(etl.tabla_cruda, pd.DataFrame)

def test_etl_limpiar_error(etl):

	with pytest.raises(LimpiarError):

		etl.limpiar()

	assert etl.tabla_cruda is None

@pytest.mark.parametrize(["anno"],
	[(1990,),(1995,),(1999,),(2003,),(2007,),(2011,),(2014,),(2017,),(2018,),(2019,),(2020,),(2021,),(2022,),(2023,)]
)
def test_etl_limpiar(anno):

	etl=ETL(anno)

	etl.extraer()

	etl.limpiar()

	assert isinstance(etl.tabla_limpia, pd.DataFrame)

	time.sleep(5)

def test_etl_almacenar_error_sin_extraer(etl):

	with pytest.raises(AlmacenarError):

		etl.almacenar()

	assert etl.tabla_limpia is None

def test_etl_almacenar_error_sin_limpiar(etl):

	etl.extraer()

	with pytest.raises(AlmacenarError):

		etl.almacenar()

	assert etl.tabla_limpia is None

def test_etl_almacenar(etl):

	etl.extraer()

	etl.limpiar()

	etl.almacenar()

	temporada=etl.temporada.temporada

	archivo_csv=f"Partidos_ATM_{temporada.replace('-','_')}.csv"

	assert os.path.exists(archivo_csv)

	time.sleep(60)

	os.remove(archivo_csv)
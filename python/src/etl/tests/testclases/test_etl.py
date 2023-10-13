import pytest
import pandas as pd
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

		etl._ETL__extraer()

def test_etl_extraer_error_cabecera():

	etl=ETL(2001)

	with pytest.raises(TablaError):

		etl._ETL__extraer()

@pytest.mark.parametrize(["anno"],
	[(2023,),(2010,),(2005,),(2019,),(1999,)]
)
def test_etl_extraer(anno):

	etl=ETL(anno)

	etl._ETL__extraer()

	assert isinstance(etl.tabla_cruda, pd.DataFrame)

def test_etl_limpiar_error(etl):

	with pytest.raises(LimpiarError):

		etl._ETL__limpiar()

	assert etl.tabla_cruda is None

@pytest.mark.parametrize(["anno"],
	[(1990,),(1995,),(1999,),(2003,),(2007,),(2011,),(2014,),(2017,),(2018,),(2019,),(2020,),(2021,),(2022,),(2023,)]
)
def test_etl_limpiar(anno):

	etl=ETL(anno)

	etl._ETL__extraer()

	etl._ETL__limpiar()

	assert isinstance(etl.tabla_limpia, pd.DataFrame)

	time.sleep(5)

def test_etl_almacenar_error_sin_extraer(etl):

	with pytest.raises(AlmacenarError):

		etl._ETL__almacenar()

	assert etl.tabla_limpia is None

def test_etl_almacenar_error_sin_limpiar(etl):

	etl._ETL__extraer()

	with pytest.raises(AlmacenarError):

		etl._ETL__almacenar()

	assert etl.tabla_limpia is None

def test_etl_almacenar(etl, conexion):

	etl._ETL__extraer()

	etl._ETL__limpiar()

	etl._ETL__almacenar()

	conexion.c.execute("SELECT * FROM partidos")

	partidos=conexion.c.fetchall()

	assert len(partidos)!=0

	for partido in partidos:

		assert len(partido)==13
		assert partido["fecha"].year==etl.temporada.ano1 or partido["fecha"].year==etl.temporada.ano2

def test_etl_pipeline(etl, conexion):

	etl.pipelineETL()

	conexion.c.execute("SELECT * FROM partidos")

	partidos=conexion.c.fetchall()

	assert len(partidos)!=0

	for partido in partidos:

		assert len(partido)==13
		assert partido["fecha"].year==etl.temporada.ano1 or partido["fecha"].year==etl.temporada.ano2

	time.sleep(60)

@pytest.mark.parametrize(["veces"],
	[(1,),(4,),(2,),(3,)]
)
def test_etl_almacenar_varios(etl, conexion, veces):

	etl.pipelineETL()

	conexion.c.execute("SELECT * FROM partidos")

	cantidad_partidos=len(conexion.c.fetchall())

	for _ in range(veces):

		etl.pipelineETL()

	time.sleep(3)

	conexion.c.execute("SELECT * FROM partidos")

	cantidad_partidos_final=conexion.c.fetchall()

	assert len(cantidad_partidos_final)==cantidad_partidos*(veces+1)

def test_etl_almacenar_varios_diferentes(conexion):

	annos=[2019,2020,2021,2022,2023]

	for anno in annos:

		etl=ETL(anno)

		etl.pipelineETL()

		time.sleep(3)

	conexion.c.execute("SELECT * FROM partidos")

	partidos=conexion.c.fetchall()

	for partido in partidos:

		assert len(partido)==13
		assert partido["fecha"].year in annos+[annos[-1]+1]
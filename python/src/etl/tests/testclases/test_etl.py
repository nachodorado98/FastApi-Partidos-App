import pytest
import pandas as pd
import time
import datetime

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

def test_etl_sin_filtrar(etl):

	etl._ETL__extraer()

	etl._ETL__limpiar()

	df=etl.tabla_limpia.copy()

	df_filtrado=etl._ETL__filtrar(df, None)

	assert df.equals(df_filtrado)

@pytest.mark.parametrize(["anno", "mes", "dia"],
	[
		(2023,9,10),
		(2023,10,5),
		(2023,8,22),
		(2023,12,30),
		(2024,10,14),
		(2023,8,20)
	]
)
def test_etl_filtrar(etl, anno, mes, dia):

	fecha=datetime.datetime(anno, mes, dia)

	etl._ETL__extraer()

	etl._ETL__limpiar()

	df=etl.tabla_limpia.copy()

	df_filtrado=etl._ETL__filtrar(df, fecha)

	assert not df.equals(df_filtrado)
	assert df_filtrado[df_filtrado["Fecha"]<=fecha.strftime("%Y-%m-%d")].empty

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

@pytest.mark.parametrize(["fecha_corte"],
	[("2023-02-16",),("2022-09-30",),("2023-4-13",),("2022-12-31",),("2023-05-01",),]
)
def test_etl_almacenar_fecha_corte(conexion, fecha_corte):

	etl=ETL(2022)

	etl.pipelineETL()

	conexion.c.execute("SELECT * FROM partidos")

	cantidad_partidos_total=len(conexion.c.fetchall())

	conexion.c.execute("DELETE FROM partidos WHERE fecha>%s",(fecha_corte,))

	conexion.confirmar()

	conexion.c.execute("SELECT * FROM partidos")

	assert len(conexion.c.fetchall())<cantidad_partidos_total

	etl_2=ETL(2022)

	etl_2.pipelineETL()

	conexion.c.execute("SELECT * FROM partidos")

	assert len(conexion.c.fetchall())==cantidad_partidos_total

	time.sleep(10)

@pytest.mark.parametrize(["veces"],
	[(1,),(4,),(2,),(3,)]
)
def test_etl_almacenar_varios_repetidos(etl, conexion, veces):

	etl.pipelineETL()

	conexion.c.execute("SELECT * FROM partidos")

	cantidad_partidos=len(conexion.c.fetchall())

	for _ in range(veces):

		etl.pipelineETL()

	time.sleep(3)

	conexion.c.execute("SELECT * FROM partidos")

	cantidad_partidos_final=conexion.c.fetchall()

	assert len(cantidad_partidos_final)==cantidad_partidos
	assert not len(cantidad_partidos_final)==cantidad_partidos*(veces+1)
	assert len(cantidad_partidos_final)==cantidad_partidos

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

@pytest.mark.parametrize(["fecha_corte"],
	[("2023-09-16",),("2023-10-01",),("2023-08-15",)]
)
def test_etl_almacenar_varios_diferentes_fecha_corte(conexion, fecha_corte):

	annos=[2019,2020,2021,2022,2023]

	for anno in annos:

		etl=ETL(anno)

		etl.pipelineETL()

		time.sleep(3)

	conexion.c.execute("SELECT * FROM partidos")

	cantidad_partidos_total=len(conexion.c.fetchall())

	conexion.c.execute("DELETE FROM partidos WHERE fecha>%s",(fecha_corte,))

	conexion.confirmar()

	conexion.c.execute("SELECT * FROM partidos")

	assert len(conexion.c.fetchall())<cantidad_partidos_total

	etl_2=ETL(2023)

	etl_2.pipelineETL()

	conexion.c.execute("SELECT * FROM partidos")

	assert len(conexion.c.fetchall())==cantidad_partidos_total

	time.sleep(3)
import datetime

from src.modelos.partido import Partido
from src.modelos.partido_utils import obtenerObjetoPartido, obtenerObjetosPartido

def test_obtener_partido():

	partido={"id":1,"fecha":datetime.datetime(2019,6,22),"hora":"21:00","competicion":"Liga","ronda":"J1","lugar":"Local",
			"rival":"rival","marcador":"5-0","resultado":"Victoria","posesion":50,"publico":100000,"capitan":"Nacho",
			"arbitro":"cabron"}

	objeto=obtenerObjetoPartido(partido)

	assert isinstance(objeto, Partido)
	assert objeto.fecha=="22/06/2019"


def test_obtener_varios_partidos():

	partidos=[{"id":1,"fecha":datetime.datetime(2019,6,22),"hora":"21:00","competicion":"Liga","ronda":"J1","lugar":"Local",
			"rival":"rival","marcador":"5-0","resultado":"Victoria","posesion":50,"publico":100000,"capitan":"Nacho",
			"arbitro":"cabron"},
			{"id":2,"fecha":datetime.datetime(2019,6,22),"hora":"21:00","competicion":"Liga","ronda":"J1","lugar":"Local",
			"rival":"rival","marcador":"5-0","resultado":"Victoria","posesion":50,"publico":100000,"capitan":"Nacho",
			"arbitro":"cabron"},
			{"id":3,"fecha":datetime.datetime(2019,6,22),"hora":"21:00","competicion":"Liga","ronda":"J1","lugar":"Local",
			"rival":"rival","marcador":"5-0","resultado":"Victoria","posesion":50,"publico":100000,"capitan":"Nacho",
			"arbitro":"cabron"}]

	objetos=obtenerObjetosPartido(partidos)

	assert len(objetos)==3

	for objeto in objetos:

		assert isinstance(objeto, Partido)
		assert objeto.fecha=="22/06/2019"

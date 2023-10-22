import datetime

from src.modelos.asistido import Asistido
from src.modelos.asistido_utils import obtenerObjetoAsistido, obtenerObjetosAsistido

def test_obtener_asistido():

	asistido={"asistido":"1","fecha":datetime.datetime(2019,6,22),"competicion":"Liga","lugar":"Local", "rival":"rival",
			"marcador":"5-0","resultado":"Victoria","comentarios":"comentario"}

	objeto=obtenerObjetoAsistido(asistido)

	assert isinstance(objeto, Asistido)
	assert objeto.fecha=="22/06/2019"


def test_obtener_varios_asistidos():

	partidos=[{"asistido":"1","fecha":datetime.datetime(2019,6,22),"competicion":"Liga","lugar":"Local", "rival":"rival",
			"marcador":"5-0","resultado":"Victoria","comentarios":"comentario"},
			{"asistido":"1","fecha":datetime.datetime(2019,6,22),"competicion":"Liga","lugar":"Local", "rival":"rival",
			"marcador":"5-0","resultado":"Victoria","comentarios":"comentario"},
			{"asistido":"1","fecha":datetime.datetime(2019,6,22),"competicion":"Liga","lugar":"Local", "rival":"rival",
			"marcador":"5-0","resultado":"Victoria","comentarios":"comentario"}]

	objetos=obtenerObjetosAsistido(partidos)

	assert len(objetos)==3

	for objeto in objetos:

		assert isinstance(objeto, Asistido)
		assert objeto.fecha=="22/06/2019"

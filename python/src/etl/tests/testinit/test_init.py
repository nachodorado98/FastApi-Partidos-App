import pytest
import datetime
import time

from src import ETLtemporada, ETLdesde

@pytest.mark.parametrize(["anno"],
	[(1999,),(2019,),(2005,),(1990,)]
)
def test_etl_temporada(conexion, anno):

	ETLtemporada(anno)

	conexion.c.execute("""SELECT * FROM partidos""")

	partidos=conexion.c.fetchall()

	for partido in partidos:

		assert partido["fecha"].year in [anno, anno+1]

	time.sleep(3)

def test_etl_desde_inicio(conexion):

	time.sleep(30)

	ETLdesde()

	conexion.c.execute("""SELECT * FROM partidos ORDER BY fecha""")	

	partidos=conexion.c.fetchall()

	anno_actual=datetime.datetime.now().year

	assert partidos[0]["fecha"].year==1988
	assert partidos[-1]["fecha"].year in [anno_actual, anno_actual+1]

@pytest.mark.parametrize(["anno"],
	[(2019,),(2022,),(2015,)]
)
def test_etl_desde_anno(conexion, anno):

	ETLdesde(anno)

	conexion.c.execute("""SELECT * FROM partidos ORDER BY fecha""")

	partidos=conexion.c.fetchall()

	anno_actual=datetime.datetime.now().year

	assert partidos[0]["fecha"].year==anno
	assert partidos[-1]["fecha"].year in [anno_actual, anno_actual+1]

def test_etl_desde_anno_siguiente(conexion):

	anno_actual=datetime.datetime.now().year

	ETLdesde(anno_actual+1)

	conexion.c.execute("""SELECT * FROM partidos""")

	assert conexion.c.fetchall()==[]
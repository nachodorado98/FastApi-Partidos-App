import pytest
import datetime
import time

from src import obtenerData

def test_obtener_data_tabla_vacia(conexion):

	assert conexion.tabla_vacia()

	obtenerData()

	assert not conexion.tabla_vacia()

	conexion.c.execute("SELECT * FROM partidos ORDER BY fecha")

	partidos=conexion.c.fetchall()

	assert partidos[0]["fecha"].year==1988

	time.sleep(10)

@pytest.mark.parametrize(["fecha"],
	[("2022-06-22",),("2022-01-13",),("2021-09-15",),("2023-02-16",),("2023-10-01",),("2024-11-10",),(datetime.datetime.now().strftime("%Y-%m-%d"),)]
)
def test_obtener_data_temporadas(conexion_simple, fecha):

	assert not conexion_simple.tabla_vacia()

	conexion_simple.c.execute("SELECT * FROM partidos ORDER BY fecha")

	cantidad_partidos=len(conexion_simple.c.fetchall())

	conexion_simple.c.execute("DELETE FROM partidos WHERE fecha>%s",(fecha,))

	conexion_simple.confirmar()

	conexion_simple.c.execute("SELECT * FROM partidos ORDER BY fecha")

	partidos=conexion_simple.c.fetchall()

	cantidad_partidos_sin_borrar=len(partidos)

	cantidad_partidos_borrados=cantidad_partidos-cantidad_partidos_sin_borrar

	for partido in partidos:

		assert not partido["fecha"].strftime("%Y-%m-%d")>fecha

	obtenerData()

	conexion_simple.c.execute("SELECT * FROM partidos ORDER BY fecha")

	cantidad_partidos_nueva=len(conexion_simple.c.fetchall())

	assert cantidad_partidos_nueva==cantidad_partidos
	assert cantidad_partidos_nueva-cantidad_partidos_sin_borrar==cantidad_partidos_borrados


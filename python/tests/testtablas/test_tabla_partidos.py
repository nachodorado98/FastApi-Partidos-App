import pytest

def test_obtener_partidos(conexion_simple):

	partidos=conexion_simple.obtenerPartidos()

	for partido in partidos:

		assert len(partido)==13

	assert partidos[-1]["fecha"].year==1988

@pytest.mark.parametrize(["limite", "saltar"],
	[(5,0),(1,3),(4,1),(10,10)]
)
def test_obtener_partidos_rango(conexion_simple, limite, saltar):

	partidos=conexion_simple.obtenerPartidos()

	partidos_rango=conexion_simple.obtenerPartidosRango(limite, saltar)

	assert len(partidos_rango)==limite

	for partido in partidos[:saltar]:

		assert partido not in partidos_rango

def test_partido_no_existe(conexion_simple):

	assert not conexion_simple.existe_partido(0)

def test_partido_existe(conexion_simple):

	id_partido=conexion_simple.obtenerPartidos()[-1]["id"]

	assert conexion_simple.existe_partido(id_partido)
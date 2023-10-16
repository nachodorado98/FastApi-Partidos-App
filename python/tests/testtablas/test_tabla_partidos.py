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
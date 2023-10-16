import pytest

def test_obtener_partidos_todos(cliente, conexion_simple):

	cantidad_partidos=len(conexion_simple.obtenerPartidos())

	peticion=cliente.get("/partidos?todo=True")

	contenido=peticion.json()

	assert peticion.status_code==200
	assert len(contenido)==cantidad_partidos

@pytest.mark.parametrize(["saltar"],
	[(5,),(1,),(10,),(0,)]
)
def test_obtener_partidos_saltar(cliente, conexion_simple, saltar):

	peticion_todos=cliente.get("/partidos?todo=True")

	contenido_todos=peticion_todos.json()

	peticion=cliente.get(f"/partidos?saltar={saltar}")

	contenido=peticion.json()

	assert peticion.status_code==200
	assert len(contenido)==20

	for partido in contenido_todos[:saltar]:

		assert partido not in contenido

@pytest.mark.parametrize(["limite"],
	[(5,),(1,),(10,),(0,),(100,)]
)
def test_obtener_partidos_limite(cliente, conexion_simple, limite):

	peticion=cliente.get(f"/partidos?limite={limite}")

	contenido=peticion.json()

	assert peticion.status_code==200
	assert len(contenido)==limite

@pytest.mark.parametrize(["saltar", "limite"],
	[(5,2),(1,5),(10,0),(0,5)]
)
def test_obtener_partidos_saltar_limite(cliente, conexion_simple, saltar, limite):

	peticion_todos=cliente.get("/partidos?todo=True")

	contenido_todos=peticion_todos.json()

	peticion=cliente.get(f"/partidos?limite={limite}&saltar={saltar}")

	contenido=peticion.json()

	assert peticion.status_code==200
	assert len(contenido)==limite

	for partido in contenido_todos[:saltar]:

		assert partido not in contenido
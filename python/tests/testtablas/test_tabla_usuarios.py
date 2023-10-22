import pytest

def test_insertar_usuario(conexion_simple):

	conexion_simple.insertarUsuario("nacho98", "nacho", "1234")

	conexion_simple.c.execute("SELECT * FROM usuarios")

	usuarios=conexion_simple.c.fetchall()

	assert len(usuarios)==1

def test_insertar_usuarios(conexion_simple):

	conexion_simple.insertarUsuario("nacho98", "nacho", "1234")
	conexion_simple.insertarUsuario("nacho99", "nacho", "1234")
	conexion_simple.insertarUsuario("nacho989", "nacho", "1234")

	conexion_simple.c.execute("SELECT * FROM usuarios")

	assert len(conexion_simple.c.fetchall())==3

def test_usuario_no_existe(conexion_simple):

	assert not conexion_simple.existe_usuario("nacho98")

def test_usuario_existe(conexion_simple):

	assert not conexion_simple.existe_usuario("nacho98")

	conexion_simple.insertarUsuario("nacho98", "nacho", "1234")

	assert conexion_simple.existe_usuario("nacho98")

def test_obtener_usuarios_no_existen(conexion_simple):

	assert conexion_simple.obtenerUsuarios() is None

def test_obtener_usuarios_existen(conexion_simple):

	conexion_simple.insertarUsuario("nacho98", "nacho", "1234")
	conexion_simple.insertarUsuario("nacho99", "nacho", "1234")
	conexion_simple.insertarUsuario("nacho989", "nacho", "1234")

	usuarios=conexion_simple.obtenerUsuarios()

	assert len(usuarios)==3

	for usuario in usuarios:

		assert "usuario" in usuario

def test_obtener_contrasena_usuario_no_existe(conexion_simple):

	assert conexion_simple.obtenerContrasena("nacho98") is None

@pytest.mark.parametrize(["usuario"],
	[("nacho98",),("nacho99",),("nacho989",)]
)
def test_obtener_contrasena_usuario_existe(conexion_simple, usuario):

	conexion_simple.insertarUsuario("nacho98", "nacho", "1234")
	conexion_simple.insertarUsuario("nacho99", "nacho", "1234")
	conexion_simple.insertarUsuario("nacho989", "nacho", "1234")

	contrasena=conexion_simple.obtenerContrasena(usuario)

	assert contrasena=="1234"

def test_obtener_datos_usuario_no_existe(conexion_simple):

	assert conexion_simple.obtenerDatosUsuario("nacho98") is None

def test_obtener_datos_usuario_existe(conexion_simple):

	conexion_simple.insertarUsuario("nacho98", "nacho", "1234")

	datos=conexion_simple.obtenerDatosUsuario("nacho98")

	assert datos["usuario"]=="nacho98"
	assert datos["nombre"]=="nacho"
	assert datos["numero_partidos"]==0
	assert "contrasena" not in datos

def test_obtener_numeros_partidos_no_existe(conexion_simple):

	assert conexion_simple.obtenerNumeroPartidos("nacho98") is None

def test_obtener_numeros_partidos_existe(conexion_simple):

	conexion_simple.insertarUsuario("nacho98", "nacho", "1234")

	assert conexion_simple.obtenerNumeroPartidos("nacho98")==0

def test_aumentar_numeros_partidos(conexion_simple):

	conexion_simple.insertarUsuario("nacho98", "nacho", "1234")

	assert conexion_simple.obtenerNumeroPartidos("nacho98")==0

	conexion_simple.aumentarAsistido("nacho98")

	assert conexion_simple.obtenerNumeroPartidos("nacho98")==1

def test_aumentar_numeros_partidos_varias_veces(conexion_simple):

	conexion_simple.insertarUsuario("nacho98", "nacho", "1234")

	assert conexion_simple.obtenerNumeroPartidos("nacho98")==0

	for _ in range(5):

		conexion_simple.aumentarAsistido("nacho98")

	assert conexion_simple.obtenerNumeroPartidos("nacho98")==5	
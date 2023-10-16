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
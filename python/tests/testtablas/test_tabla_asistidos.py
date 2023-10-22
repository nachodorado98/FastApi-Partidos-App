def test_insertar_asistido(conexion_simple):

	conexion_simple.insertarUsuario("nacho98", "nacho", "1234")

	id_partido=conexion_simple.obtenerPartidos()[-1]["id"]

	conexion_simple.insertarAsistido("1", id_partido, "nacho98", "comentario")

	conexion_simple.c.execute("SELECT * FROM asistidos")

	assert len(conexion_simple.c.fetchall())==1

def test_insertar_varios_asistidos(conexion_simple):

	conexion_simple.insertarUsuario("nacho98", "nacho", "1234")

	id_partido=conexion_simple.obtenerPartidos()[-1]["id"]

	conexion_simple.insertarAsistido("1", id_partido, "nacho98", "comentario")
	conexion_simple.insertarAsistido("2", id_partido+1, "nacho98", "comentario")
	conexion_simple.insertarAsistido("3", id_partido+2, "nacho98", "comentario")

	conexion_simple.c.execute("SELECT * FROM asistidos")

	assert len(conexion_simple.c.fetchall())==3

def test_obtener_asistidos_no_existen_usuario_no_existe(conexion_simple):

	conexion_simple.insertarUsuario("nacho98", "nacho", "1234")

	assert conexion_simple.obtenerAsistidos("nacho98") is None

def test_obtener_asistidos_existen_usuario_no_existe(conexion_simple):

	conexion_simple.insertarUsuario("nacho98", "nacho", "1234")

	id_partido=conexion_simple.obtenerPartidos()[-1]["id"]

	conexion_simple.insertarAsistido("12345", id_partido, "nacho98", "comentario")

	assert conexion_simple.obtenerAsistidos("nacho9") is None

def test_obtener_asistidos_existen_usuario_existe(conexion_simple):

	conexion_simple.insertarUsuario("nacho98", "nacho", "1234")

	id_partido=conexion_simple.obtenerPartidos()[-1]["id"]

	conexion_simple.insertarAsistido("12345", id_partido, "nacho98", "comentario")
	conexion_simple.insertarAsistido("123451", id_partido+1, "nacho98", "comentario")
	conexion_simple.insertarAsistido("123452", id_partido+2, "nacho98", "comentario")

	conexion_simple.confirmar()

	asistidos=conexion_simple.obtenerAsistidos("nacho98")

	assert len(asistidos)==3

	for asistido in asistidos:

		assert "asistido" in asistido
		assert "fecha" in asistido
		assert "competicion" in asistido
		assert "rival" in asistido
		assert "marcador" in asistido
		assert "resultado" in asistido
		assert "lugar" in asistido
		assert "comentarios" in asistido

def test_asistido_no_existe(conexion_simple):

	conexion_simple.insertarUsuario("nacho98", "nacho", "1234")

	assert not conexion_simple.existe_asistido(1, "nacho98")

def test_asistido_existe(conexion_simple):

	conexion_simple.insertarUsuario("nacho98", "nacho", "1234")

	id_partido=conexion_simple.obtenerPartidos()[-1]["id"]

	conexion_simple.insertarAsistido("12345", id_partido, "nacho98", "comentario")

	assert conexion_simple.existe_asistido(id_partido, "nacho98")
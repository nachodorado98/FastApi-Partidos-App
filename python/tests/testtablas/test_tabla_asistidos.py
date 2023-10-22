def test_obtener_asistidos_no_existen_usuario_no_existe(conexion_simple):

	conexion_simple.insertarUsuario("nacho98", "nacho", "1234")

	assert conexion_simple.obtenerAsistidos("nacho98") is None

def test_obtener_asistidos_existen_usuario_no_existe(conexion_simple):

	conexion_simple.insertarUsuario("nacho98", "nacho", "1234")

	id_partido=conexion_simple.obtenerPartidos()[-1]["id"]

	conexion_simple.c.execute(f"INSERT INTO asistidos VALUES('12345', {id_partido}, 'nacho98', 'Comentario')")

	conexion_simple.confirmar()

	assert conexion_simple.obtenerAsistidos("nacho9") is None

def test_obtener_asistidos_existen_usuario_existe(conexion_simple):

	conexion_simple.insertarUsuario("nacho98", "nacho", "1234")

	id_partido=conexion_simple.obtenerPartidos()[-1]["id"]

	conexion_simple.c.execute(f"INSERT INTO asistidos VALUES('12345', {id_partido}, 'nacho98', 'Comentario')")
	conexion_simple.c.execute(f"INSERT INTO asistidos VALUES('123451', {id_partido+1}, 'nacho98', 'Comentario')")
	conexion_simple.c.execute(f"INSERT INTO asistidos VALUES('123452', {id_partido+2}, 'nacho98', 'Comentario')")

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
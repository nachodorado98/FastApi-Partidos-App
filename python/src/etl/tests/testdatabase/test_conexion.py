def test_conexion(conexion):

	conexion.c.execute("SELECT current_database();")

	assert conexion.c.fetchone()["current_database"]=="bbdd_partidos"

	conexion.c.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")

	tablas=[tabla["relname"] for tabla in conexion.c.fetchall()]

	assert "partidos" in tablas

def test_cerrar_conexion(conexion):

	assert not conexion.bbdd.closed

	conexion.cerrarConexion()

	assert conexion.bbdd.closed

def test_tabla_partidos_vacia(conexion):

	conexion.c.execute("SELECT * FROM partidos")

	assert conexion.c.fetchall()==[]
def test_insertar_partido(conexion):

	partido=["2019-06-22","21:00", "Champions", "Final", "Calderon", "ATM", "5-0", "Victoria", 70, 12345, "Nacho", "Arbitro"]

	conexion.insertarPartido(partido)

	conexion.c.execute("SELECT * FROM partidos")

	assert len(conexion.c.fetchall())==1

def test_tabla_vacia(conexion):

	assert conexion.tabla_vacia()

def test_tabla_no_vacia(conexion):

	partido=["2019-06-22","21:00", "Champions", "Final", "Calderon", "ATM", "5-0", "Victoria", 70, 12345, "Nacho", "Arbitro"]

	conexion.insertarPartido(partido)

	assert not conexion.tabla_vacia()

def test_fecha_mas_reciente_tabla_vacia(conexion):

	assert conexion.fecha_mas_reciente() is None

def test_fecha_mas_reciente(conexion):

	partidos=[["2019-06-22","21:00", "Champions", "Final", "Calderon", "ATM", "5-0", "Victoria", 70, 12345, "Nacho", "Arbitro"],
				["2018-06-22","21:00", "Champions", "Final", "Calderon", "ATM", "5-0", "Victoria", 70, 12345, "Nacho", "Arbitro"],
				["2022-06-22","21:00", "Champions", "Final", "Calderon", "ATM", "5-0", "Victoria", 70, 12345, "Nacho", "Arbitro"],
				["2005-06-22","21:00", "Champions", "Final", "Calderon", "ATM", "5-0", "Victoria", 70, 12345, "Nacho", "Arbitro"],
				["2010-06-22","21:00", "Champions", "Final", "Calderon", "ATM", "5-0", "Victoria", 70, 12345, "Nacho", "Arbitro"]]

	for partido in partidos:

		conexion.insertarPartido(partido)

	assert conexion.fecha_mas_reciente().strftime("%Y-%m-%d")=="2022-06-22"
def test_insertar_partido(conexion):

	partido=["2019-06-22","21:00", "Champions", "Final", "Calderon", "ATM", "5-0", "Victoria", 70, 12345, "Nacho", "Arbitro"]

	conexion.insertarPartido(partido)

	conexion.c.execute("SELECT * FROM partidos")

	assert len(conexion.c.fetchall())==1

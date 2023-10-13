import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional, Dict
import datetime

from .confconexion import *

# Clase para la conexion a la BBDD
class Conexion:

	def __init__(self)->None:

		try:
			
			self.bbdd=psycopg2.connect(host=HOST, user=USUARIO, password=CONTRASENA, port=PUERTO, database=BBDD)
			self.c=self.bbdd.cursor(cursor_factory=RealDictCursor)

		except psycopg2.OperationalError as e:

			print("Error en la conexion a la BBDD")
			print(e)

	# Metodo para cerrar la conexion a la BBDD
	def cerrarConexion(self)->None:

		self.c.close()
		self.bbdd.close()

	# Metodo para insertar un partido
	def insertarPartido(self, partido:List)->None:

		self.c.execute("""INSERT INTO partidos (fecha, hora, competicion, ronda, lugar, rival, marcador, resultado,
							posesion, publico, capitan, arbitro)
							VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
							tuple(partido))

		self.bbdd.commit()
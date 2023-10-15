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

	# Metodo para confirmar una accion
	def confirmar(self)->None:

		self.bbdd.commit()

	# Metodo para insertar un partido
	def insertarPartido(self, partido:List)->None:

		self.c.execute("""INSERT INTO partidos (fecha, hora, competicion, ronda, lugar, rival, marcador, resultado,
							posesion, publico, capitan, arbitro)
							VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
							tuple(partido))

		self.confirmar()

	# Metodo para saber si la tabla esta vacia
	def tabla_vacia(self)->bool:

		self.c.execute("""SELECT *
							FROM partidos""")

		partidos=self.c.fetchall()

		return True if partidos==[] else False

	# Metodo para obtener la fecha mas reciente
	def fecha_mas_reciente(self)->Optional[datetime.datetime]:

		self.c.execute("""SELECT MAX(fecha) AS fecha_mas_reciente
							FROM partidos""")

		return self.c.fetchone()["fecha_mas_reciente"]
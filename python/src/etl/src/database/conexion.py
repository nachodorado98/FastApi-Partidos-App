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

	# Metodo para obtener los partidos
	def obtenerPartidos(self)->List[Dict]:

		self.c.execute("""SELECT *
							FROM partidos
							ORDER BY fecha DESC""")

		return self.c.fetchall()

	# Metodo para obtener los partidos con limite y salto
	def obtenerPartidosRango(self, limite:int, saltar:int)->List[Dict]:

		self.c.execute(f"""SELECT *
							FROM partidos
							ORDER BY fecha DESC
							LIMIT {limite}
							OFFSET {saltar}""")

		return self.c.fetchall()

	# Metodo para insertar un usuario
	def insertarUsuario(self, usuario:str, nombre:str, contrasena:str)->None:

		self.c.execute("""INSERT INTO usuarios (usuario, nombre, contrasena)
							VALUES(%s, %s, %s)""",
							(usuario, nombre, contrasena))

		self.bbdd.commit()

	# Metodo para comprobar que un usuario existe
	def existe_usuario(self, usuario:str)->bool:

		self.c.execute("""SELECT *
							FROM usuarios
							WHERE usuario=%s""",
							(usuario,))

		return False if self.c.fetchone() is None else True

	# Metodo para obtener los usuarios
	def obtenerUsuarios(self)->Optional[List[Dict]]:

		self.c.execute("""SELECT usuario
							FROM usuarios""")

		usuarios=self.c.fetchall()

		return None if usuarios==[] else usuarios
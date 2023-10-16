from typing import Optional

from .conexion import Conexion

# Funcion para devolver el objeto de la conexion
def crearSesion()->Optional[Conexion]:

	con=Conexion()

	try: 

		yield con

	except:

		con.cerrarConexion()
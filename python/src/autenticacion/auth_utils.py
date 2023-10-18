from jose import jwt, JWTError
import datetime

from .confauth import CLAVE, ALGORITMO

# Funcion para generar el token unico del usuario
def generarToken(usuario:str, tiempo:int=30)->str:

	datos_token={"sub":usuario, "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=tiempo)}

	return jwt.encode(datos_token, key=CLAVE, algorithm=ALGORITMO)
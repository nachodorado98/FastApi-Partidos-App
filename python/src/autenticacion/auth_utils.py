from jose import jwt, JWTError
import datetime
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from .confauth import CLAVE, ALGORITMO

from src.etl.src.database.sesion import crearSesion
from src.etl.src.database.conexion import Conexion

from src.modelos.token import Payload

# Funcion para generar el token unico del usuario
def generarToken(usuario:str, tiempo:int=30)->str:

	datos_token={"sub":usuario, "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=tiempo)}

	return jwt.encode(datos_token, key=CLAVE, algorithm=ALGORITMO)

# Funcion para decodificar el token unico del usuario
def decodificarToken(token:str=Depends(OAuth2PasswordBearer("/tokens")), con:Conexion=Depends(crearSesion))->Payload:

	try:

		datos_token=jwt.decode(token, key=CLAVE, algorithms=[ALGORITMO])

		if not con.existe_usuario(datos_token["sub"]):

			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado", headers={"WWW-Authentication":"Bearer"})

		return Payload(**datos_token)

	except JWTError as e:

		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado", headers={"WWW-Authentication":"Bearer"})
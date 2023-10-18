from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.etl.src.database.sesion import crearSesion
from src.etl.src.database.conexion import Conexion

from src.utilidades.utils import comprobarHash 

from .auth_utils import generarToken

from src.modelos.token import Token


router_auth=APIRouter(prefix="/tokens", tags=["Autenticacion"])


@router_auth.post("", status_code=status.HTTP_200_OK, summary="Devuelve el token del usuario")
async def obtenerToken(form:OAuth2PasswordRequestForm=Depends(), con:Conexion=Depends(crearSesion))->Token:

	"""
	Devuelve el diccionario del token unico asociado a ese usuario.
	## Respuesta
	200 (OK): Si los datos son correctos
	- **Access_token**: El token del usuario (str).
	- **Token_type**: El tipo del token (str).
	401 (UNAUTHORIZED): Si los datos no son correctos
	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	if not con.existe_usuario(form.username):

		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No existe el usuario", headers={"WWW-Authentication":"Bearer"})

	hash_contrasena=con.obtenerContrasena(form.username)

	if not comprobarHash(form.password, hash_contrasena):

		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="La contraseña es erronea", headers={"WWW-Authentication":"Bearer"})		

	token=generarToken(form.username, 30)

	con.cerrarConexion()

	return Token(access_token=token, token_type="bearer")
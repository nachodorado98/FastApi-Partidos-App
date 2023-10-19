from fastapi import APIRouter, status, Depends, HTTPException
from typing import List, Dict

from src.etl.src.database.conexion import Conexion
from src.etl.src.database.sesion import crearSesion

from src.modelos.usuario import UsuarioBBDD, UsuarioPerfil
from src.modelos.usuario_utils import obtenerObjetoUsuarioPerfil
from src.modelos.token import Payload

from src.utilidades.utils import generarHash

from src.autenticacion.auth_utils import decodificarToken

router_usuarios=APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router_usuarios.post("", status_code=status.HTTP_201_CREATED, summary="Crea un usuario")
async def crearUsuario(usuario:UsuarioBBDD, con:Conexion=Depends(crearSesion))->Dict:

	"""
	Crea un usuario y lo inserta en la BBDD.

	Devuelve un mensaje y el diccionario que representa el usuario creado.

	## Respuesta

	201 (CREATED): Si se crea el usuario correctamente

	- **Mensaje**: El mensaje de creacion correcto del usuario (str).
	- **Usuario**: El usuario con el usuario y el nombre (Dict).

	400 (BAD REQUEST): Si no se crea el usuario correctamente

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	if con.existe_usuario(usuario.usuario):

		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario existente")

	con.insertarUsuario(usuario.usuario,
						usuario.nombre.title(),
						generarHash(usuario.contrasena))

	con.cerrarConexion()

	return {"mensaje":"Usuario creado correctamente",
			"usuario":{"usuario":usuario.usuario,
						"nombre":usuario.nombre.title()}}

@router_usuarios.get("", status_code=status.HTTP_200_OK, summary="Devuelve los usuarios existentes")
async def obtenerUsuarios(con:Conexion=Depends(crearSesion))->List[Dict]:

	"""
	Devuelve los diccionarios asociados a los usuarios disponibles en la BBDD.

	## Respuesta

	200 (OK): Si se obtienen los usuarios correctamente

	- **Usuario**: El usuario del usuario (str).

	404 (NOT FOUND): Si no se obtienen los usuarios correctamente

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	usuarios=con.obtenerUsuarios()

	con.cerrarConexion()

	if usuarios is None:

		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuarios no existentes")

	return usuarios

@router_usuarios.get("/me", status_code=status.HTTP_200_OK, summary="Devuelve los datos del usuario")
async def obtenerPerfil(payload:Payload=Depends(decodificarToken), con:Conexion=Depends(crearSesion))->UsuarioPerfil:

	"""
	Devuelve el diccionario de los datos del usuario.

	## Respuesta

	200 (OK): Si se obtienen los datos del usuario correctamente

	- **Usuario**: El nombre de usuario del usuario (str).
	- **Nombre**: El nombre del usuario (str).
	- **Numero_partidos**: El numero de partidos del usuario (int).

	401 (UNAUTHORIZED): Si los datos no son correctos

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	datos_usuario=con.obtenerDatosUsuario(payload.sub)

	return obtenerObjetoUsuarioPerfil(datos_usuario)
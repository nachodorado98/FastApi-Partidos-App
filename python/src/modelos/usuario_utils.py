from typing import Dict

from .usuario import UsuarioPerfil

# Funcion para obtener un objeto usuario perfil
def obtenerObjetoUsuarioPerfil(valores:Dict)->UsuarioPerfil:

	return UsuarioPerfil(usuario=valores["usuario"],
						nombre=valores["nombre"],
						numero_partidos=valores["numero_partidos"])
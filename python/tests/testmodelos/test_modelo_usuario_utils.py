from src.modelos.usuario import UsuarioPerfil
from src.modelos.usuario_utils import obtenerObjetoUsuarioPerfil

def test_obtener_usuario_perfil():

	usuario={"usuario":"nacho98","nombre":"Nacho","numero_partidos":1000}

	objeto=obtenerObjetoUsuarioPerfil(usuario)

	assert isinstance(objeto, UsuarioPerfil)
	assert objeto.usuario=="nacho98"
	assert objeto.nombre=="Nacho"
	assert objeto.numero_partidos==1000
import pytest

from src.modelos.usuario import UsuarioBBDD

@pytest.mark.parametrize(["contrasena"],
	[("1234567",),("123456789",),("12345",),("1234567 8",),("dsgfdgfdhfdhf d",),("fbfdg123456789vds",)]
)
def test_modelo_usuario_bbdd_contrasena_incorrecta(contrasena):

	usuario={"usuario":"nacho98","nombre":"Nacho","contrasena":contrasena}

	with pytest.raises(ValueError):

		UsuarioBBDD(**usuario)

@pytest.mark.parametrize(["contrasena"],
	[("12345678",),("12345fdfdg",),("12345fdfdhfg",),("1234567gfdhfdh8",),("contrasena1234",),("fbfdg12345678u9vds",)]
)
def test_modelo_usuario_bbdd_correcto(contrasena):

	usuario={"usuario":"nacho98","nombre":"Nacho","contrasena":contrasena}

	UsuarioBBDD(**usuario)
import pytest

def test_pagina_obtener_token_no_existe(cliente, conexion_simple):

	form=datos_form={"grant_type": "password", "username": "nacho98", "password": "1235", "scope": "", "client_id": "", "client_secret": ""}

	respuesta=cliente.post("/tokens", data=form)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido
	assert contenido["detail"]=="No existe el usuario"


@pytest.mark.parametrize(["contrasena"],
	[("1234567892",),("123456789",),("1234",),("12345678910",),("contrasena",)]
)
def test_pagina_obtener_token_contrasena_error(cliente, conexion_simple, contrasena):

	cliente.post("/usuarios", json={"usuario":"nacho98","nombre":"Nacho","contrasena":"contrasena1234"})

	form=datos_form={"grant_type": "password", "username": "nacho98", "password": contrasena, "scope": "", "client_id": "", "client_secret": ""}

	respuesta=cliente.post("/tokens", data=form)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido
	assert contenido["detail"]=="La contraseña es erronea"


def test_pagina_obtener_token_autorizado(cliente, conexion_simple):

	cliente.post("/usuarios", json={"usuario":"nacho98","nombre":"Nacho","contrasena":"contrasena1234"})

	datos_form={"grant_type": "password", "username": "nacho98", "password": "contrasena1234", "scope": "", "client_id": "", "client_secret": ""}

	respuesta=cliente.post("/tokens", data=datos_form)

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert "access_token" in contenido
	assert "token_type" in contenido
import pytest

@pytest.mark.parametrize(["contrasena"],
	[("1234567",),("123456789",),("12345",),("1234567 8",),("dsgfdgfdhfdhf d",),("fbfdg123456789vds",)]
)
def test_pagina_agregar_usuario_incorrecto(cliente, conexion_simple, contrasena):

	usuario={"usuario":"nacho98","nombre":"Nacho","contrasena":contrasena}

	respuesta=cliente.post("/usuarios", json=usuario)

	contenido=respuesta.json()

	assert respuesta.status_code==422
	assert not "mensaje" in contenido
	assert not "usuario" in contenido

	conexion_simple.c.execute("SELECT * FROM usuarios")

	assert len(conexion_simple.c.fetchall())==0


@pytest.mark.parametrize(["usuario"],
	[("nacho98",),("usuario",),("sfdsgfdg",),("amanditaa99",)]
)
def test_pagina_agregar_usuario_existente(cliente, conexion_simple, usuario):

	conexion_simple.insertarUsuario(usuario, "Nacho", "1234567gfdhg")

	conexion_simple.c.execute("SELECT * FROM usuarios")

	assert len(conexion_simple.c.fetchall())==1

	respuesta=cliente.post("/usuarios", json={"usuario":usuario,"nombre":"Nacho","contrasena":"contrasena1234"})

	contenido=respuesta.json()

	assert respuesta.status_code==400
	assert "detail" in contenido

	conexion_simple.c.execute("SELECT * FROM usuarios")

	assert len(conexion_simple.c.fetchall())==1

def test_pagina_agregar_usuario(cliente, conexion_simple):

	respuesta=cliente.post("/usuarios", json={"usuario":"nacho98","nombre":"Nacho","contrasena":"contrasena1234"})

	contenido=respuesta.json()

	assert respuesta.status_code==201
	assert "mensaje" in contenido
	assert "usuario" in contenido
	assert "usuario" in contenido["usuario"]
	assert "nombre" in contenido["usuario"]

	conexion_simple.c.execute("SELECT * FROM usuarios")

	assert len(conexion_simple.c.fetchall())==1

def test_pagina_agregar_varios_usuarios(cliente, conexion_simple):

	cliente.post("/usuarios", json={"usuario":"nacho98","nombre":"Nacho","contrasena":"contrasena1234"})
	cliente.post("/usuarios", json={"usuario":"nacho99","nombre":"Nacho","contrasena":"contrasena1234"})
	cliente.post("/usuarios", json={"usuario":"nacho989","nombre":"Nacho","contrasena":"contrasena1234"})
	cliente.post("/usuarios", json={"usuario":"nacho998","nombre":"Nacho","contrasena":"contrasena1234"})

	conexion_simple.c.execute("SELECT * FROM usuarios")

	assert len(conexion_simple.c.fetchall())==4

def test_pagina_obtener_usuarios_no_existentes(cliente, conexion_simple):

	respuesta=cliente.get("/usuarios")

	contenido=respuesta.json()

	assert respuesta.status_code==404
	assert "detail" in contenido

def test_pagina_obtener_usuarios_existentes(cliente, conexion_simple):

	cliente.post("/usuarios", json={"usuario":"nacho98","nombre":"Nacho","contrasena":"contrasena1234"})
	cliente.post("/usuarios", json={"usuario":"nacho99","nombre":"Nacho","contrasena":"contrasena1234"})
	cliente.post("/usuarios", json={"usuario":"nacho989","nombre":"Nacho","contrasena":"contrasena1234"})
	cliente.post("/usuarios", json={"usuario":"nacho998","nombre":"Nacho","contrasena":"contrasena1234"})

	respuesta=cliente.get("/usuarios")

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert len(contenido)==4

	for usuario in contenido:

		assert "usuario" in usuario

@pytest.mark.parametrize(["token"],
	[("token",), ("dgfdkjg89e5yujgfkjgdf",), ("nacho98",), ("amanditaa",), ("1234",)]
)
def test_pagina_obtener_datos_usuario_no_autenticado(cliente, token):

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.get("/usuarios/me", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido

@pytest.mark.parametrize(["usuario", "contrasena"],
	[
		("nacho98", "123456aa7891"),
		("nacho98", "qwertyuiop"),
		("amanda99", "1q2w3e4r5t6y7u"),
	]
)
def test_pagina_obtener_datos_usuario_autenticado(cliente, conexion_simple, usuario, contrasena):

	cliente.post("/usuarios", json={"usuario":usuario,"nombre":"Nacho","contrasena":contrasena})

	datos_form={"grant_type": "password", "username": usuario, "password": contrasena, "scope": "", "client_id": "", "client_secret": ""}

	contenido_token=cliente.post("/tokens", data=datos_form).json()

	token=contenido_token["access_token"]

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.get("/usuarios/me", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert "usuario" in contenido
	assert contenido["usuario"]==usuario
	assert "nombre" in contenido
	assert "numero_partidos" in contenido
	assert "contrasena" not in contenido
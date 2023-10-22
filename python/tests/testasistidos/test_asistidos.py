import pytest

@pytest.mark.parametrize(["token"],
	[("token",), ("dgfdkjg89e5yujgfkjgdf",), ("nacho98",), ("amanditaa",), ("1234",)]
)
def test_pagina_insertar_asistidos_no_autenticado(cliente, token):

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.post("/asistidos", json={"id_partido":1, "comentarios":"comentarios"}, headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido

def test_pagina_insertar_asistidos_no_existe_partido(cliente, header_autorizado):

	respuesta=cliente.post("/asistidos", json={"id_partido":0, "comentarios":"comentarios"}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==400
	assert "detail" in contenido

def test_pagina_insertar_asistidos_existente(conexion_simple, cliente, header_autorizado):

	id_partido=conexion_simple.obtenerPartidos()[-1]["id"]

	conexion_simple.insertarAsistido("12345", id_partido, "nacho98", "comentario")

	respuesta=cliente.post("/asistidos", json={"id_partido":id_partido, "comentarios":"comentarios"}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==400
	assert "detail" in contenido

def test_pagina_insertar_asistidos(conexion_simple, cliente, header_autorizado):

	id_partido=conexion_simple.obtenerPartidos()[-1]["id"]

	respuesta=cliente.post("/asistidos", json={"id_partido":id_partido, "comentarios":"comentarios"}, headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==201
	assert "mensaje" in contenido

def test_pagina_insertar_asistidos_varios(conexion_simple, cliente, header_autorizado):

	id_partido=conexion_simple.obtenerPartidos()[-1]["id"]

	cliente.post("/asistidos", json={"id_partido":id_partido, "comentarios":"comentarios"}, headers=header_autorizado)
	cliente.post("/asistidos", json={"id_partido":id_partido+1, "comentarios":"comentarios"}, headers=header_autorizado)
	cliente.post("/asistidos", json={"id_partido":id_partido+2, "comentarios":"comentarios"}, headers=header_autorizado)
	cliente.post("/asistidos", json={"id_partido":id_partido+3, "comentarios":"comentarios"}, headers=header_autorizado)

	assert conexion_simple.obtenerNumeroPartidos("nacho98")==4

@pytest.mark.parametrize(["token"],
	[("token",), ("dgfdkjg89e5yujgfkjgdf",), ("nacho98",), ("amanditaa",), ("1234",)]
)
def test_pagina_obtener_asistidos_no_autenticado(cliente, token):

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.get("/asistidos", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido

def test_pagina_obtener_asistidos_autenticado_no_existen(cliente, header_autorizado):

	respuesta=cliente.get("/asistidos", headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==404
	assert "detail" in contenido

def test_pagina_obtener_asistidos_autenticado_existen(conexion_simple, cliente, header_autorizado):

	id_partido=conexion_simple.obtenerPartidos()[-1]["id"]

	cliente.post("/asistidos", json={"id_partido":id_partido, "comentarios":"comentarios"}, headers=header_autorizado)
	cliente.post("/asistidos", json={"id_partido":id_partido+1, "comentarios":"comentarios"}, headers=header_autorizado)
	cliente.post("/asistidos", json={"id_partido":id_partido+2, "comentarios":"comentarios"}, headers=header_autorizado)
	cliente.post("/asistidos", json={"id_partido":id_partido+3, "comentarios":"comentarios"}, headers=header_autorizado)

	respuesta=cliente.get("/asistidos", headers=header_autorizado)

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert len(contenido)==4

	for asistido in contenido:

		"asistido" in asistido
		"fecha" in asistido
		"competicion" in asistido
		"rival" in asistido
		"marcador" in asistido
		"resultado" in asistido
		"lugar" in asistido
		"comentarios" in asistido
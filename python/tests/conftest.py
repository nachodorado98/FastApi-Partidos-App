import os
import sys
sys.path.append(os.path.abspath(".."))

import pytest
from fastapi.testclient import TestClient 

from src.etl.src.database.conexion import Conexion
from src import crearApp

@pytest.fixture
def conexion_simple():

	conexion=Conexion()

	conexion.c.execute("DELETE FROM usuarios")

	conexion.c.execute("DELETE FROM asistidos")

	conexion.bbdd.commit()

	yield conexion

@pytest.fixture
def conexion(conexion_simple):

	conexion_simple.c.execute("DELETE FROM partidos")

	conexion_simple.bbdd.commit()

	return conexion_simple

@pytest.fixture()
def app():

	app=crearApp()

	return app

@pytest.fixture()
def cliente(app):

	return TestClient(app)

@pytest.fixture()
def header_autorizado(cliente, conexion_simple):

	cliente.post("/usuarios", json={"usuario":"nacho98","nombre":"Nacho", "contrasena":"987654321"})

	datos_form={"grant_type": "password", "username": "nacho98", "password": "987654321", "scope": "", "client_id": "", "client_secret": ""}

	contenido_token=cliente.post("/tokens", data=datos_form).json()

	token=contenido_token["access_token"]

	return {"Authorization": f"Bearer {token}"}
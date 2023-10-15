import os
import sys
sys.path.append(os.path.abspath(".."))

import pytest
from fastapi.testclient import TestClient 

from src.etl.src.database.conexion import Conexion
from src import crearApp

@pytest.fixture
def conexion_simple():

	yield Conexion()

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

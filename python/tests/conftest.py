import os
import sys
sys.path.append(os.path.abspath(".."))

import pytest

from src.etl.src.database.conexion import Conexion

@pytest.fixture
def conexion_simple():

	yield Conexion()

@pytest.fixture
def conexion(conexion_simple):

	conexion_simple.c.execute("DELETE FROM partidos")

	conexion_simple.bbdd.commit()

	return conexion_simple

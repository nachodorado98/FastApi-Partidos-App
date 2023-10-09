import os
import sys
sys.path.append(os.path.abspath(".."))

import pytest

from src.temporada import Temporada

@pytest.fixture
def temporada():

	return Temporada(2023)
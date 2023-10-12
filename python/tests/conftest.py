import os
import sys
sys.path.append(os.path.abspath(".."))

import pytest

from src.temporada import Temporada
from src.scraper import Scraper
from src.etl import ETL

@pytest.fixture
def temporada():

	return Temporada(2023)

@pytest.fixture
def scraper():

	return Scraper("2019-2020")

@pytest.fixture
def etl():

	return ETL(2023)
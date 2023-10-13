import pytest
import datetime

from src.temporada import Temporada

@pytest.mark.parametrize(["numero"],
	[(1,),(3,),(2,),(10,),(5,),(100,),(22,),]
)
def test_crear_objeto_temporada_error(numero):

	ano_actual=datetime.datetime.now().year

	with pytest.raises(Exception):

		Temporada(ano_actual+numero)

@pytest.mark.parametrize(["numero"],
	[(0,),(1,),(3,),(2,),(10,),(5,),(100,),(22,),]
)
def test_crear_objeto_temporada(numero):

	ano_actual=datetime.datetime.now().year

	assert Temporada(ano_actual-numero)

@pytest.mark.parametrize(["ano"],
	[(2023,),(2019,),(1998,),(1999,)]
)
def test_generar_temporada(ano):

	temporada=Temporada(ano)

	assert temporada.ano1==ano
	assert temporada.ano2==ano+1
	assert temporada.temporada==f"{ano}-{ano+1}"


@pytest.mark.parametrize(["numero"],
	[(1,),(3,),(2,),(10,),(5,),(100,),(22,),]
)
def test_generar_temporadas_vacio(numero):

	ano_actual=datetime.datetime.now().year

	temporadas=Temporada.generarTemporadas(ano_actual+numero)

	assert temporadas==[]

@pytest.mark.parametrize(["ano"],
	[(2023,),(2019,),(1998,),(1999,), (datetime.datetime.now().year,)]
)
def test_generar_temporadas(ano):

	temporadas=Temporada.generarTemporadas(ano)

	assert temporadas[0].ano1==ano
	assert temporadas[-1].ano1==datetime.datetime.now().year
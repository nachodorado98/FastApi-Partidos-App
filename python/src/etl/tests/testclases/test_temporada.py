import pytest
import datetime

from src.temporada import Temporada
from src.excepciones import TemporadaError

@pytest.mark.parametrize(["numero"],
	[(1,),(3,),(2,),(10,),(5,),(100,),(22,),]
)
def test_crear_objeto_temporada_error(numero):

	ano_actual=datetime.datetime.now().year

	with pytest.raises(TemporadaError):

		Temporada(ano_actual+numero)

@pytest.mark.parametrize(["numero"],
	[(0,),(1,),(3,),(2,),(10,),(5,),(100,),(22,),]
)
def test_crear_objeto_temporada(numero):

	ano_actual=datetime.datetime.now().year

	assert Temporada(ano_actual-numero)

@pytest.mark.parametrize(["anno"],
	[(2023,),(2019,),(1998,),(1999,)]
)
def test_generar_temporada(anno):

	temporada=Temporada(anno)

	assert temporada.ano1==anno
	assert temporada.ano2==anno+1
	assert temporada.temporada==f"{anno}-{anno+1}"

@pytest.mark.parametrize(["numero"],
	[(1,),(3,),(2,),(10,),(5,),(100,),(22,),]
)
def test_generar_temporadas_vacio(numero):

	ano_actual=datetime.datetime.now().year

	temporadas=Temporada.generarTemporadas(ano_actual+numero)

	assert temporadas==[]

@pytest.mark.parametrize(["anno"],
	[(2023,),(2019,),(1998,),(1999,), (datetime.datetime.now().year,)]
)
def test_generar_temporadas(anno):

	temporadas=Temporada.generarTemporadas(anno)

	assert temporadas[0].ano1==anno
	assert temporadas[-1].ano1==datetime.datetime.now().year

@pytest.mark.parametrize(["anno", "mes", "dia", "anno1", "anno2"],
	[
		(2023, 6, 22, 2022, 2023),
		(2023, 8, 6, 2023, 2024),
		(2019, 3, 15, 2018, 2019),
		(2019, 11, 22, 2019, 2020),
		(1999, 1, 20, 1998, 1999)
	]
)
def test_obtener_temporada_desde_fecha(anno, mes, dia, anno1, anno2):

	fecha=datetime.datetime(anno, mes, dia)

	temporada=Temporada.desde_fecha(fecha)

	assert temporada.ano1==anno1
	assert temporada.ano2==anno2
	assert temporada.temporada==f"{anno1}-{anno2}"

def test_obtener_temporada_actual():

	temporada_actual=Temporada.temporada_actual()

	fecha_actual=datetime.datetime.now()

	anno_actual=fecha_actual.year

	mes_actual=fecha_actual.month

	if mes_actual>7:

		assert temporada_actual.ano1==anno_actual

	else:

		assert temporada_actual.ano1==anno_actual-1

@pytest.mark.parametrize(["anno", "mes", "dia"],
	[
		(2010,1,1),
		(1999,8,6),
		(2022,1,1),
		(2022,5,16),
		(2022,12,2),
		(2023,2,16),
		(2023,6,30),
		(2023,7,31)
	]
)
def test_no_es_temporada_actual(anno, mes, dia):

	fecha_datetime=datetime.datetime(anno, mes, dia)

	assert not Temporada.es_temporada_actual(fecha_datetime)

@pytest.mark.parametrize(["anno", "mes", "dia"],
	[
		(datetime.datetime.now().year,8,1),
		(datetime.datetime.now().year,10,10),
		(datetime.datetime.now().year,9,22),
		(datetime.datetime.now().year,12,31),
		(datetime.datetime.now().year+1,2,16),
		(datetime.datetime.now().year+1,6,22),
		(datetime.datetime.now().year+1,7,31)
	]
)
def test_es_temporada_actual(anno, mes, dia):

	fecha_datetime=datetime.datetime(anno, mes, dia)

	assert Temporada.es_temporada_actual(fecha_datetime)
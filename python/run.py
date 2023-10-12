from src import crearETL

etl=crearETL(2019)

etl.extraer()

etl.limpiar()

etl.almacenar()
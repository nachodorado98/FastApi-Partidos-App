class PaginaError(Exception):

	def __init__(self)->None:

		super().__init__("La pagina no esta accesible")

class TablaError(Exception):

	def __init__(self, temporada:str)->None:

		super().__init__(f"No hay tabla en la temporada {temporada}")

class LimpiarError(Exception):

	def __init__(self)->None:

		super().__init__("No hay tabla aún para limpiar")

class AlmacenarError(Exception):

	def __init__(self)->None:

		super().__init__("No hay tabla limpia para almacenar")
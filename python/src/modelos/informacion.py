from pydantic import BaseModel

class Informacion(BaseModel):

	mensaje:str
	version:str
	descripcion:str
	documentacion:str
from pydantic import BaseModel

class Asistido(BaseModel):

	asistido:str
	fecha:str
	competicion:str
	rival:str
	marcador:str
	resultado:str
	lugar:str
	comentarios:str

class AsistidoBBDD(BaseModel):

	id_partido:int
	comentarios:str
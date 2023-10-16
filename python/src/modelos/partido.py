from pydantic import BaseModel

class Partido(BaseModel):

	id_partido:int
	fecha:str
	hora:str
	competicion:str
	ronda:str
	lugar:str
	rival:str
	marcador:str
	resultado:str
	posesion:int
	publico:int
	capitan:str
	arbitro:str
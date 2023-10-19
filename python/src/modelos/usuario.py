from pydantic import BaseModel, validator

class Usuario(BaseModel):

	usuario:str
	nombre:str

class UsuarioBBDD(Usuario):

	contrasena:str

	# Metodo para validar la contraseña
	@validator("contrasena")
	def comprobarContrasena(cls, contrasena:str)->str:

		if len(contrasena)<8 or " " in contrasena or "123456789" in contrasena:

			raise ValueError("la contraseña no cumple los requisitos")

		return contrasena

	class Config:

		json_schema_extra={"example":{"usuario":"nacho98",
										"nombre":"Nacho",
										"contrasena":"123456789"}}

class UsuarioPerfil(Usuario):

	numero_partidos:int
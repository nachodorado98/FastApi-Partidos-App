from passlib.context import CryptContext

# Funcion para generar el hash de una contraseña
def generarHash(contrasena:str)->str:

	objeto_hash=CryptContext(schemes=["bcrypt"], deprecated="auto")

	return objeto_hash.hash(contrasena)

# Funcion para comprobar el hash y la contraseña
def comprobarHash(contrasena:str, contrasena_hash:str)->bool:

	objeto_hash=CryptContext(schemes=["bcrypt"], deprecated="auto")

	return objeto_hash.verify(contrasena, contrasena_hash)

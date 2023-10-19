from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):

	access_token:str
	token_type:str

class Payload(BaseModel):

	sub:str
	exp:datetime
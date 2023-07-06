from pydantic import BaseModel

'''
A schema for content of the token
Inheriting BaseModel from pydantic, because it has all the methods needed for a schema, i.e, to_json, validate etc. 
'''
class TokenMessage(BaseModel):
    iss: str
    sub: str
    iat: int
    exp: int

from typing import Optional

from pydantic import BaseModel

'''
A schema for content of the token
Inheriting BaseModel from pydantic, because it has all 
the methods needed for a schema, i.e, to_json, validate etc. 
'''
class Token(BaseModel):
    iss: Optional[str]
    sub: Optional[str]
    iat: Optional[int]
    exp: Optional[int]
    user_id: Optional[str]
    permissions: list[str]

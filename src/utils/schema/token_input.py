from pydantic import BaseModel

from models.role import Role
from models.user import User

'''
A schema for content of the token
'''
class TokenInput(BaseModel):
    user_data: User
    role: Role

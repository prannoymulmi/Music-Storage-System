from typing import Optional

from sqlmodel import Field
from sqlmodel import SQLModel

""" The database models, which the ORM uses to translate data into tables."""
class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role_name: str = Field(index=True)

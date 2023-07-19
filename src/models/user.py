from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime
from sqlmodel import Field
from sqlmodel import SQLModel

""" The database models, for user data which the ORM uses to translate data into tables."""
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False)
    password: str = Field(nullable=False)
    password_salt: str = Field(nullable=True)
    hash_method: str = Field(nullable=True)
    modified_timestamp: datetime = Field(
        sa_column=Column(DateTime,
                         onupdate=datetime.now(),
                         nullable=False,
                         default=datetime.utcnow()
                         )
    )
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    last_login_attempt: datetime = Field(default=datetime.utcnow())
    login_counter: int = Field(nullable=False, default=0)
    created_timestamp: datetime = Field(nullable=False,
                                        default=datetime.utcnow())
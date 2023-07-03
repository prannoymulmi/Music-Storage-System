from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlmodel import Field
from sqlmodel import SQLModel
from typing import Optional

""" The database models, which the ORM uses to translate data into tables."""
class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password: str = Field(nullable=False)
    password_salt: str = Field(nullable=True)
    hash_method: str = Field(nullable=False)
    test: bytes = Field(nullable=False)
    modified_timestamp: datetime = Field(
        sa_column=Column(DateTime,
                         onupdate=datetime.now(),
                         nullable=False,
                         default=datetime.utcnow()
                         )
    )
    last_login_attempt: datetime = Field(default=datetime.utcnow())
    login_counter: int = Field(nullable=False, default=0)
    created_timestamp: datetime = Field(nullable=False,
                                        default=datetime.utcnow())
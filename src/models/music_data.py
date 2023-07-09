from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime
from sqlmodel import Field
from sqlmodel import SQLModel

""" The database models, which the ORM uses to translate data into tables."""
class MusicData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    music_file: bytes = Field(nullable=True)
    music_file_name: str = Field(nullable=True)
    modified_timestamp: datetime = Field(
        sa_column=Column(DateTime,
                         onupdate=datetime.now(),
                         nullable=False,
                         default=datetime.utcnow()
                         )
    )
    checksum: str = Field(nullable=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_timestamp: datetime = Field(nullable=False,
                                        default=datetime.utcnow())
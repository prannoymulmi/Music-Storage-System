from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel


class MusicDataOutput(SQLModel):
    id: Optional[int]
    music_score: int
    music_file_name: str
    lyrics_file_name: str
    checksum: str
    user_id: Optional[int]
    modified_timestamp: str
    created_timestamp: str
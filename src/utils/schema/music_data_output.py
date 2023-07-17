from typing import Optional

from sqlmodel import SQLModel


class MusicDataOutput(SQLModel):
    id: Optional[int]
    music_score: Optional[int]
    music_file_name: Optional[str]
    lyrics_file_name: Optional[str]
    checksum: Optional[str]
    user_id: Optional[int]
    modified_timestamp: Optional[str]
    created_timestamp: Optional[str]
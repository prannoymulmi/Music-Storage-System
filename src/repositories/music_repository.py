from typing import Any

from sqlmodel import Session, select

from models.music_data import MusicData
from models.role import Role


class MusicRepository:

    # def get_role_by_id(self, session: Session, role_id: str) -> Any:
    #     statement = select(Role).where(
    #         Role.id == role_id)
    #     result = session.exec(statement)
    #     data = result.one()
    #     return data

    def create_and_add_new__music_data(self, session: Session, music_data: MusicData):
        session.add(music_data)
        session.commit()
        session.refresh(music_data)
        return music_data

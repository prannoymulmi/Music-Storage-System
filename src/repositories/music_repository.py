
from sqlmodel import Session, select, update

from models.music_data import MusicData
from models.user import User
from utils.schema.music_data_output import MusicDataOutput


class MusicRepository:

    # def get_role_by_id(self, session: Session, role_id: str) -> Any:
    #     statement = select(Role).where(
    #         Role.id == role_id)
    #     result = session.exec(statement)
    #     data = result.one()
    #     return data

    def get_music_data_by_user(self, session: Session,  user: User):
        statement = select(MusicData).where(
            MusicData.user_id == user.id)

        result = session.exec(statement)
        return result.all()

    def get_music_data_by_music_id(self, session: Session,  music_id: int):
        statement = select(MusicData).where(
            MusicData.id == music_id)

        result = session.exec(statement)
        return result.one()

    def update_music_data(self, session: Session, music_data: MusicDataOutput):
        statement = select(MusicData).where(
            MusicData.id == music_data.id)

        result = session.exec(statement)
        data = result.one()

        session.add(data)
        session.commit()
        session.refresh(data)

    def get_all_music_data(self, session: Session):
        statement = select(MusicData)

        result = session.exec(statement)
        return result.all()

    def create_and_add_new__music_data(self, session: Session, music_data: MusicData):
        session.add(music_data)
        session.commit()
        session.refresh(music_data)
        return music_data
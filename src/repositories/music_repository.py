
from sqlmodel import Session, select

from models.music_data import MusicData
from models.user import User


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

    def get_all_music_data(self, session: Session):
        statement = select(MusicData)

        result = session.exec(statement)
        return result.all()

    def create_and_add_new__music_data(self, session: Session, music_data: MusicData):
        session.add(music_data)
        session.commit()
        session.refresh(music_data)
        return music_data
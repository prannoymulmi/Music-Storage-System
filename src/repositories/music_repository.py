
from sqlmodel import Session, select

from models.music_data import MusicData
from models.user import User
from utils.encryption_utils import EncryptionUtils


class MusicRepository:

    def get_music_data_by_user(self, session: Session,  user: User):
        statement = select(MusicData).where(
            MusicData.user_id == user.id)

        result = session.exec(statement)
        return self.decrypt_list_all_music_data(result)

    def get_music_data_by_music_id(self, session: Session,  music_id: int):
        statement = select(MusicData).where(
            MusicData.id == music_id)

        result = session.exec(statement)
        decrypted_result = self.decrypt_music_data(result.one())
        return decrypted_result

    def update_music_data(self, session: Session, music_data: MusicData):

        statement = select(MusicData).where(
            MusicData.id == music_data.id)

        result = session.exec(statement)
        data = result.one()
        data.music_score = music_data.music_score
        data.music_file_name = EncryptionUtils.encrypt(music_data.music_file_name)
        data.music_file = bytes(EncryptionUtils.encrypt(music_data.music_file), "utf-8")
        data.lyrics = bytes(EncryptionUtils.encrypt(music_data.lyrics), "utf-8")
        data.lyrics_file_name = EncryptionUtils.encrypt(music_data.lyrics_file_name)
        data.checksum = music_data.checksum
        session.add(data)
        session.commit()
        session.refresh(data)

    def get_all_music_data(self, session: Session):
        statement = select(MusicData)

        result = session.exec(statement)
        return self.decrypt_list_all_music_data(result)

    def decrypt_list_all_music_data(self, result):
        decrypted_music_data: [MusicData] = []
        for decrypt_data in result.all():
            decrypted_music_data.append(self.decrypt_music_data_show_all(decrypt_data))
        return decrypted_music_data

    def create_and_add_new__music_data(self, session: Session, music_data: MusicData):
        encrypted_data = self.encrypt_music_data(music_data)
        session.add(encrypted_data)
        session.commit()
        session.refresh(encrypted_data)
        return encrypted_data

    def delete_data_by_id(self, session: Session, music_data_id: int):
        statement = select(MusicData).where(
            MusicData.id == music_data_id)

        result = session.exec(statement)
        data = result.one()
        session.delete(data)
        session.commit()

    def encrypt_music_data(self, music_data: MusicData):
        return MusicData(
            music_score=music_data.music_score,
            music_file_name=EncryptionUtils.encrypt(music_data.music_file_name),
            music_file=EncryptionUtils.encrypt(music_data.music_file),
            checksum=music_data.checksum,
            user_id=music_data.user_id,
            lyrics_file_name=EncryptionUtils.encrypt(music_data.lyrics_file_name),
            lyrics=EncryptionUtils.encrypt(music_data.lyrics),
            modified_timestamp=music_data.modified_timestamp,
            created_timestamp=music_data.created_timestamp,
            id=music_data.id
        )

    def decrypt_music_data(self, music_data: MusicData):
        return MusicData(
            music_score=music_data.music_score,
            music_file_name=EncryptionUtils.decrypt(music_data.music_file_name),
            music_file=EncryptionUtils.decrypt(music_data.music_file),
            checksum=music_data.checksum,
            user_id=music_data.user_id,
            lyrics_file_name=EncryptionUtils.decrypt(music_data.lyrics_file_name),
            lyrics=EncryptionUtils.decrypt(music_data.lyrics),
            modified_timestamp=music_data.modified_timestamp,
            created_timestamp=music_data.created_timestamp,
            id=music_data.id
        )

    def decrypt_music_data_show_all(self, music_data: MusicData):
        return MusicData(
            music_score=music_data.music_score,
            music_file_name=EncryptionUtils.decrypt(music_data.music_file_name),
            checksum=music_data.checksum,
            user_id=music_data.user_id,
            lyrics_file_name=EncryptionUtils.decrypt(music_data.lyrics_file_name),
            modified_timestamp=music_data.modified_timestamp,
            created_timestamp=music_data.created_timestamp,
            id=music_data.id
        )

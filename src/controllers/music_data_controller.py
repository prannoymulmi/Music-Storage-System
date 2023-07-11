from exceptions.user_denied_exception import UserDeniedError
from factories.config_factory import ConfigFactory
from factories.repository_factory import RepositoryFactory
from models.music_data import MusicData
from models.role import Role
from models.user import User
from repositories.music_repository import MusicRepository
from repositories.role_repository import RoleRepository
from utils.configLoader import ConfigLoader
from utils.decorator_utils import check_token_and_role
from utils.music_utils import MusicUtils
from utils.schema.music_data_output import MusicDataOutput


class MusicDataController:
    __repo_factory: RepositoryFactory = None
    __music_repo: MusicRepository = None
    __role_repo: RoleRepository = None
    __music_utils: MusicUtils = None

    def __init__(self) -> None:
        super().__init__()
        loader: ConfigLoader = ConfigFactory().create_object('config_loader')
        self.__session = loader.load_config()
        self.__repo_factory = RepositoryFactory()
        self.__music_repo = self.__repo_factory.create_object("music_repo")
        self.__role_repo = self.__repo_factory.create_object("role_repo")
        self.__music_utils = MusicUtils.instance()

    def add_music_data(
            self,
            music_file_path: str,
            music_score: int,
            lyrics_file_path,
            user: User):
        music_file: bytes = self.__music_utils.get_file_from_path(music_file_path)
        lyrics_file: bytes = self.__music_utils.get_file_from_path(lyrics_file_path)
        combined_check_sum: str = self.__music_utils.calculate_check_sum(music_file + lyrics_file)
        music_file_name: str = self.__music_utils.get_file_name_from_path(music_file_path)
        lyrics_file_name: str = self.__music_utils.get_file_name_from_path(lyrics_file_path)
        music_data = MusicData(user_id=user.id,
                               music_file_name=music_file_name,
                               music_file=music_file,
                               music_score=music_score,
                               checksum=combined_check_sum,
                               lyrics_file_name=lyrics_file_name,
                               lyrics=lyrics_file
                               )
        self.__music_repo.create_and_add_new__music_data(self.__session, music_data)

    def update_music_data(self, user_data: User, music_data: MusicDataOutput):
        role: Role = self.__role_repo.get_role_by_id(self.__session, user_data.role_id)
        data: MusicData = self.__music_repo.get_music_data_by_music_id(self.__session, music_data.id)
        if role.role_name == "ADMIN":
            self.set_update_music_data(data, music_data)
            self.__music_repo.update_music_data(self.__session, data)
        elif data.user_id == user_data.id:
            self.set_update_music_data(data, music_data)
            self.__music_repo.update_music_data(self.__session, data)
        else:
            raise UserDeniedError("access_denied")


    def set_update_music_data(self, data, music_data):
        if music_data.music_score != data.music_score and music_data.music_score != 0:
            data.music_score = music_data.music_score
        if self.__music_utils.get_file_name_from_path(music_data.lyrics_file_name):
            data.lyrics_file_name = music_data.lyrics_file_name
            data.lyrics = self.__music_utils.get_file_from_path(music_data.lyrics_file_name)
        if self.__music_utils.get_file_name_from_path(music_data.music_file_name):
            data.music_file_name = self.__music_utils.get_file_name_from_path(music_data.music_file_name)
            data.music_file = self.__music_utils.get_file_from_path(music_data.music_file_name)
        data.checksum = self.__music_utils.calculate_check_sum(data.music_file + data.lyrics)

    def list_music_data(self, user: User) -> [MusicDataOutput]:
        # If user is admin then list all music otherwise only their own
        if user.role_id == 1:
            results = self.__music_repo.get_all_music_data(self.__session)
            return self.set_music_data_output(results)
        if user.role_id == 2:
            results = self.__music_repo.get_music_data_by_user(self.__session, user)
            return self.set_music_data_output(results)

    def set_music_data_output(self, results):
        result_output: [MusicDataOutput] = []
        format = "2020-06-18T14:55:28-05:00"
        for result in results:
            result_output.append(MusicDataOutput(
                id=result.id,
                music_score=result.music_score,
                music_file_name=result.music_file_name,
                checksum=result.checksum,
                user_id=result.user_id,
                lyrics_file_name=result.lyrics_file_name,
                modified_timestamp=result.modified_timestamp.strftime(format),
                created_timestamp=result.created_timestamp.strftime(format)
            ))
        return result_output

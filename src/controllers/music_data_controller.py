from factories.config_factory import ConfigFactory
from factories.repository_factory import RepositoryFactory
from models.music_data import MusicData
from models.user import User
from repositories.music_repository import MusicRepository
from repositories.user_repository import UserRepository
from utils.configLoader import ConfigLoader
from utils.decorator_utils import check_token_and_role
from utils.music_utils import MusicUtils


class MusicDataController:
    __repo_factory: RepositoryFactory = None
    __music_repo: MusicRepository = None
    __music_utils: MusicUtils = None

    def __init__(self) -> None:
        super().__init__()
        loader: ConfigLoader = ConfigFactory().create_object('config_loader')
        self.__session = loader.load_config()
        self.__repo_factory = RepositoryFactory()
        self.__music_repo = self.__repo_factory.create_object("music_repo")
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

    @check_token_and_role("ADMIN")
    def list_music_for_admin(self):
        pass

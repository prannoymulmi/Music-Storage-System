from factories.repository_factory import RepositoryFactory
from repositories.user_repository import UserRepository


class MusicDataController:
    __repo_factory: RepositoryFactory = None
    __user_repo: UserRepository = None
    def __init__(self) -> None:
        super().__init__()

    def add_music_data(
            self,
            music_file_path: str,
            music_score: int,
            lyrics_file_path,
            user_name: str):
        music_repo = self.__repo_factory.create_object("music_repo")

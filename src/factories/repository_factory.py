from repositories.music_repository import MusicRepository
from repositories.role_repository import RoleRepository
from repositories.user_repository import UserRepository
from .abstract_factory import AbstractFactory


class RepositoryFactory(AbstractFactory):
    "The Factory Class for Repository"
    @staticmethod
    def create_object(some_property):
        "A static method to get a concrete product"
        if some_property == 'user_repo':
            return UserRepository()
        if some_property == 'role_repo':
            return RoleRepository()
        if some_property == 'music_repo':
            return MusicRepository()
        return None
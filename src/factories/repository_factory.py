from repositories.user_repository import UserRepository
from .abstract_factory import AbstractFactory


class RepositoryFactory(AbstractFactory):
    "The Factory Class for controller"
    @staticmethod
    def create_object(some_property):
        "A static method to get a concrete product"
        if some_property == 'user_repo':
            return UserRepository()
        return None
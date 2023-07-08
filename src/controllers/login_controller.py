from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from factories.config_factory import ConfigFactory
from factories.repository_factory import RepositoryFactory
from models.role import Role
from models.user import User
from repositories.role_repository import RoleRepository
from repositories.user_repository import UserRepository
from utils.decorator_utils import encode_and_store_jwt, test
from utils.schema.token_input import TokenInput


class LoginController:
    __session = None
    __repo_factory = None
    def __init__(self) -> None:
        super().__init__()
        loader = ConfigFactory().create_object('config_loader')
        self.__session = loader.load_config()
        self.__repo_factory = RepositoryFactory()

    @encode_and_store_jwt
    def login(self, username, password, session):

        user_repo: UserRepository = self.__repo_factory.create_object("user_repo")
        role_repo: RoleRepository = self.__repo_factory.create_object("role_repo")

        user: User = user_repo.get_user_id(self.__session, username)
        role: Role = role_repo.get_role_by_id(self.__session, user.role_id)

        token_input = TokenInput(user_data=user, role=role)

        if self.verify_hashed_password(user.password, password):
            return token_input
        return "access_denied"

    @test
    def add_new_user(self, username: str, password: str, role: str):
        user_repo: UserRepository = self.__repo_factory.create_object("user_repo")
        user_repo.create_user_or_else_return_none(self.__session, username, password, role)
        print("hello")

    def verify_hashed_password(self, hashed_password, password):
        ph = PasswordHasher()
        try:
            return ph.verify(hashed_password, password)
        except VerifyMismatchError:
            return False

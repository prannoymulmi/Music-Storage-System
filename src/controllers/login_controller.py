from datetime import datetime

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from exceptions.user_denied_exception import UserDeniedError
from exceptions.user_not_found import UserNotFound
from factories.config_factory import ConfigFactory
from factories.repository_factory import RepositoryFactory
from models.role import Role
from models.role_names import RoleNames
from models.user import User
from repositories.role_repository import RoleRepository
from repositories.user_repository import UserRepository
from utils.decorator_utils import encode_and_store_jwt, check_token_and_role
from utils.schema.token_input import TokenInput


class LoginController:
    __session = None
    __repo_factory: RepositoryFactory = None
    __user_repo: UserRepository = None
    __role_repo: RoleRepository = None

    def __init__(self) -> None:
        super().__init__()
        loader = ConfigFactory().create_object('config_loader')
        self.__session = loader.load_config()
        self.__repo_factory = RepositoryFactory()
        self.__user_repo = self.__repo_factory.create_object("user_repo")
        self.__role_repo = self.__repo_factory.create_object("role_repo")

    @encode_and_store_jwt
    def login(self, username, password):
        try:
            user: User = self.__user_repo.get_user_by_username(self.__session, username)
            if self.verify_hashed_password(user.password, password):
                self.reset_login_counter(user)
                role: Role = self.__role_repo.get_role_by_id(self.__session, user.role_id)
                token_input = TokenInput(user_data=user, role=role)
                return token_input
            else:
                self.increase_login_counter(user)
                return "access_denied"
        except UserNotFound:
            return "access_denied"

    @check_token_and_role(role="ADMIN")
    def add_new_user(self, username: str, password: str, role: str):
        values = [member.value for member in RoleNames]
        if role not in values:
            raise UserDeniedError("role does not exist")
        user_repo: UserRepository = self.__repo_factory.create_object("user_repo")
        user_repo.create_user_or_else_return_none(self.__session, username, password, role)

    def verify_hashed_password(self, hashed_password, password):
        ph = PasswordHasher()
        try:
            return ph.verify(hashed_password, password)
        except VerifyMismatchError:
            return False

    def increase_login_counter(self, user: User):
        old_counter = user.login_counter
        user.login_counter = old_counter + 1
        user.last_login_attempt = datetime.utcnow()
        self.__user_repo.update_user(self.__session, user)

    def reset_login_counter(self, user: User):
        user.login_counter = 0
        user.last_login_attempt = datetime.utcnow()
        self.__user_repo.update_user(self.__session, user)
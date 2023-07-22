import os
from datetime import datetime

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from argon2.profiles import RFC_9106_HIGH_MEMORY

from exceptions.jwt_decode_error import JWTDecodeError
from exceptions.user_denied_exception import UserDeniedError
from exceptions.user_not_found import UserNotFound
from exceptions.weak_password import WeakPasswordError
from factories.config_factory import ConfigFactory
from factories.repository_factory import RepositoryFactory
from models.role import Role
from models.role_names import RoleNames
from models.user import User
from repositories.role_repository import RoleRepository
from repositories.user_repository import UserRepository
from utils.decorator_utils import encode_and_store_jwt, check_token_and_role
from utils.encryption_utils import EncryptionUtils
from utils.jwt_utils import JWTUtils
from utils.password_utils import PasswordUtil
from utils.schema.token import Token
from utils.schema.token_input import TokenInput

"""
A Controller which is responsible to handle all the actions related to login and adding users.
"""


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
            time_delta = (datetime.utcnow().timestamp() - user.last_login_attempt.timestamp()) / 60
            if user.login_counter > 5 and time_delta <= 10:
                raise UserDeniedError("User is blocked")
            if self.verify_hashed_password(user.password, password):
                self.reset_login_counter(user)
                role: Role = self.__role_repo.get_role_by_id(self.__session, user.role_id)
                token_input = TokenInput(user_data=user, role=role)
                return token_input
            else:
                self.increase_login_counter(user)
                raise UserDeniedError("access_denied")
        except UserNotFound:
            raise UserDeniedError("Username or password is wrong")

    def get_details_for_token(self):
        try:
            token_encrypted = os.environ.get("music_app_token")
            token = EncryptionUtils.decrypt(token_encrypted)
            token_decoded: Token = JWTUtils.decode_jwt(token)
            user: User = self.__user_repo.get_user_by_user_id(self.__session, int(token_decoded.user_id))
            role: Role = self.__role_repo.get_role_by_id(self.__session, user.role_id)
            token_input = TokenInput(user_data=user, role=role)
            return token_input
        except JWTDecodeError:
            raise UserDeniedError("Credentials expired")
        except Exception:
            ''' If the token is expired or has been the user will be be denied access'''
            raise UserDeniedError("access_denied")

    @check_token_and_role(role=["ADMIN"])
    def add_new_user(self, username: str, password: str, role: str):
        # Check
        values = [member.value for member in RoleNames]
        if role not in values:
            raise UserDeniedError("role does not exist")
        if PasswordUtil.is_password_compromised_password_in_have_i_been_pawned(password):
            raise WeakPasswordError("Error: Have I been pawned says the password is compromised")
        if PasswordUtil.is_password_policy_non_compliant(password):
            raise WeakPasswordError(
                "Password is non complaint, must have at least two capital, two small, two digits, and two special "
                "characters (-+_!@#%^&*.,?)")
        user_repo: UserRepository = self.__repo_factory.create_object("user_repo")
        user_repo.create_user_or_else_return_none(self.__session, username, password, role)

    def verify_hashed_password(self, hashed_password, password):
        ph = PasswordHasher().from_parameters(RFC_9106_HIGH_MEMORY)
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

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from factories.repository_factory import RepositoryFactory
from models.role import Role
from models.user import User
from repositories.role_repository import RoleRepository
from repositories.user_repository import UserRepository
from utils.decorator_utils import encode_and_store_jwt
from utils.schema.token_input import TokenInput


class LoginController:

    def __init__(self) -> None:
        super().__init__()

    @encode_and_store_jwt
    def login(self, username, password, session):
        repo_factory = RepositoryFactory()
        user_repo: UserRepository = repo_factory.create_object("user_repo")
        role_repo: RoleRepository = repo_factory.create_object("role_repo")

        user: User = user_repo.get_user_id(session, username)
        role: Role = role_repo.get_role_by_id(session, user.role_id)

        token_input = TokenInput(user_data=user, role=role)

        if self.verify_hashed_password(user.password, password):
            return token_input
        return "access_denied"

    def verify_hashed_password(self, hashed_password, password):
        ph = PasswordHasher()
        try:
            return ph.verify(hashed_password, password)
        except VerifyMismatchError:
            return False

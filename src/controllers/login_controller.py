from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from factories.repository_factory import RepositoryFactory
from models.user import User
from repositories.user_repository import UserRepository
from utils.decorator_utils import encode_and_store_jwt


class LoginController:

    def __init__(self) -> None:
        super().__init__()

    @encode_and_store_jwt
    def login(self, username, password, session):
        repo_factory = RepositoryFactory()
        user_repo: UserRepository = repo_factory.create_object("user_repo")
        user: User = user_repo.get_user_id(session, username)
        if self.verify_hashed_password(user.password, password):
            return "logged in"
        return "access_denied"

    def verify_hashed_password(self, hashed_password, password):
        ph = PasswordHasher()
        try:
            return ph.verify(hashed_password, password)
        except VerifyMismatchError:
            return False

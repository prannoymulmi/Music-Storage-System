from factories.repository_factory import RepositoryFactory
from models.user import User
from repositories.user_repository import UserRepository


class LoginController:

    def __init__(self) -> None:
        super().__init__()

    def login(self, username, password, session):
        repo_factory = RepositoryFactory()
        user_repo: UserRepository = repo_factory.create_object("user_repo")
        user: User = user_repo.get_user_id(session, username)
        if user.password == password:
            return "logged in"
        return "access_denied"

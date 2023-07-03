from factories.repository_factory import RepositoryFactory
from repositories.user_repository import UserRepository


class LoginController:

    def __init__(self) -> None:
        super().__init__()

    def login(self, username, password, session):
        repo_factory = RepositoryFactory()
        user_repo: UserRepository = repo_factory.create_object("user_repo")
        user = user_repo.get_user_id(session, username)
        print(user)
        return "logged in"
from factories.repository_factory import RepositoryFactory
from repositories.user_repository import UserRepository
from src.factories.controller_factory import ControllerFactory


def test_create_object_when_user_repo_then_return_user_repository():
    rf = RepositoryFactory()
    result = rf.create_object("user_repo")
    assert isinstance(result, UserRepository)


def test_create_object_when_unknown_repository_then_return_none():
    rf = RepositoryFactory()
    result = rf.create_object("unknown")
    assert result is None

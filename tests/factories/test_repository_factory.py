from factories.repository_factory import RepositoryFactory
from repositories.music_repository import MusicRepository
from repositories.user_repository import UserRepository


def test_create_object_when_user_repo_then_return_user_repository():
    rf = RepositoryFactory()
    result = rf.create_object("user_repo")
    assert isinstance(result, UserRepository)


def test_create_object_when_unknown_repository_then_return_none():
    rf = RepositoryFactory()
    result = rf.create_object("unknown")
    assert result is None


def test_create_object_when_music_repo_then_return_music_repository():
    rf = RepositoryFactory()
    result = rf.create_object("music_repo")
    assert isinstance(result, MusicRepository)

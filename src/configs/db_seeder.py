from factories.repository_factory import RepositoryFactory
from models.role import Role
from models.role_names import RoleNames
from repositories.role_repository import RoleRepository
from repositories.user_repository import UserRepository

'''
For testing purposes the DB will will have an admin user whose credentials can be changed here.
Without the initial User no other users can be created. Generally the database would not be local
and would be hosted in a secure server but for the purpose of testing this function is necessary.
'''
def seed_database(session_from_config):
    role_repo: RoleRepository = RepositoryFactory().create_object("role_repo")

    try:
        role_repo.get_role_by_id(session_from_config, "1")
    except Exception:
        role_admin = Role(role_name=RoleNames.admin.value)
        role_normal_user = Role(role_name=RoleNames.normal_user.value)

        role_repo.create_and_add_role(session_from_config, role_admin)
        role_repo.create_and_add_role(session_from_config, role_normal_user)

        user_repo: UserRepository = RepositoryFactory().create_object("user_repo")
        user_repo.create_user_or_else_return_none(session_from_config, "PLEASE_CHANGE_USERNAME", "PLEASE_CHANGE_PASS",
                                                  role_admin.role_name)

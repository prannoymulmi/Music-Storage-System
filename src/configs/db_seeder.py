import random
import string

from rich import print

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
def seed_database(session_from_config) -> bool:
    role_repo: RoleRepository = RepositoryFactory().create_object("role_repo")
    try:
        role_repo.get_role_by_id(session_from_config, "1")
        return False
    except Exception:
        role_admin = Role(role_name=RoleNames.admin.value)
        role_normal_user = Role(role_name=RoleNames.normal_user.value)

        role_repo.create_and_add_role(session_from_config, role_admin)
        role_repo.create_and_add_role(session_from_config, role_normal_user)

        user_repo: UserRepository = RepositoryFactory().create_object("user_repo")
        password = generate_password()
        print("[bold red]Please Copy the use the user and password as the initial admin user[bold red]")
        print(f"[bold green]Initial user name: admin and password: {password} [bold green]")
        user_repo.create_user_or_else_return_none(session_from_config, "admin", password,
                                                  role_admin.role_name)
        return True


"""
Generates random Password for the initial run
"""


def generate_password():
    special_chars = '!@#%^&*()_-+=<>?'
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits

    # Generate 2 random characters from each category
    """
    Bandit false positive, because this is not used for cryptography but to generate random password 
    """
    password_chars = (
        random.choices(special_chars, k=2) +  # nosec
        random.choices(uppercase_letters, k=2) + # nosec
        random.choices(digits, k=2) + # nosec
        random.choices(lowercase_letters, k=2) # nosec
    )

    # Fill the remaining characters with random choices from all categories
    """Bandit false positive, same as above"""
    remaining_length = 20 - len(password_chars) # nosec
    password_chars += random.choices(special_chars + uppercase_letters + lowercase_letters, k=remaining_length) # nosec
    # Shuffle the characters to create a random password
    random.shuffle(password_chars)

    # Join the characters into a string
    password = ''.join(password_chars)
    return password

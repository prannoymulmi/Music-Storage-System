from typing import Any

from argon2 import PasswordHasher
from argon2.profiles import RFC_9106_HIGH_MEMORY
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from exceptions.user_denied_exception import UserDeniedError
from exceptions.user_not_found import UserNotFound
from models.role import Role
from models.user import User


class UserRepository:
    """ Get User Data based on name"""

    def get_user_by_username(self, session: Session, username: str) -> Any:
        statement = select(User).where(
            User.username == username)
        result = session.exec(statement)
        try:
            data = result.one()
            return data
        except NoResultFound:
            raise UserNotFound("User is not found")

    def get_user_by_user_id(self, session: Session, user_id: int) -> Any:
        statement = select(User).where(
            User.id == user_id)
        result = session.exec(statement)
        try:
            data = result.one()
            return data
        except NoResultFound:
            raise UserNotFound("User is not found")


    def update_user(self, session, user):
        session.add(user)
        session.commit()
        session.refresh(user)

    def create_user_or_else_return_none(self: str,
                                        session: Session,
                                        username: str,
                                        password: str,
                                        role_name: str
                                        ) -> Any:
        # does nothing if a user already exists
        if self.check_if_user_exists(username, session):
            raise UserDeniedError("Error: cannot add user")

        # the staff is then saved in the database using the orm
        statement = select(Role).where(
            Role.role_name == role_name)

        result = session.exec(statement)
        data: Role = result.one()
        # hashes the password into argon2id with random salt
        # Using the first recommendation per RFC 9106 with high memory.
        ph = PasswordHasher().from_parameters(RFC_9106_HIGH_MEMORY)

        hashed_password = ph.hash(password)

        db_user = User(username=username,
                       password=hashed_password,
                       test="Adasd",
                       password_salt=hashed_password.split("p=4$")[1].split("$")[0],
                       hash_method="ARGON2ID",
                       role_id=data.id
                       )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    def check_if_user_exists(self, username, session):
        # the staff is then saved in the database using the orm
        statement = select(User).where(
            User.username == username)

        result = session.exec(statement)
        try:
            result.one()
            return True
        except NoResultFound:
            return False

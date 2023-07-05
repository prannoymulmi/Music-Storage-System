from typing import Any

from argon2 import PasswordHasher
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from models.role import Role
from models.user import User


class UserRepository:
    """ Get User Data based on name"""

    def get_user_id(self, session: Session, username: str) -> Any:
        self.create_user_or_else_return_none(session, username, "test", "ADMIN")
        statement = select(User).where(
            User.username == username)
        result = session.exec(statement)
        data = result.one()
        return data

    def create_user_or_else_return_none(self: str,
                                        session: Session,
                                        username: str,
                                        password: str,
                                        role_name: str
                                        ) -> Any:
        # does nothing if a staff already exists
        if self.check_if_user_exists(username, session):
            return

        # the staff is then saved in the database using the orm
        statement = select(Role).where(
            Role.role_name == role_name)

        result = session.exec(statement)
        data: Role = result.one()
        print(data)
        # hashes the password into argon2id with random salt
        ph = PasswordHasher()
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
            data: User = result.one()
            return True
        except NoResultFound:
            return False
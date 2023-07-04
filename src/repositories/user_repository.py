from typing import Any

from argon2 import PasswordHasher
from sqlmodel import Session, select

from models.user import User


class UserRepository:
    """ Get User Data based on name"""

    def get_user_id(self, session: Session, username: str) -> Any:
        #self.create_user_or_else_return_none(session, username, "test")
        statement = select(User).where(
            User.username == username)
        result = session.exec(statement)
        data = result.one()
        return data

    def create_user_or_else_return_none(self: str,
                                        session: Session,
                                        username: str,
                                        password: str
                                        ) -> Any:
        # does nothing if a staff already exists

        # hashes the password into argon2id with random salt
        ph = PasswordHasher()
        hashed_password = ph.hash(password)

        db_user = User(username=username,
                       password=hashed_password,
                       test="Adasd",
                       password_salt=hashed_password.split("p=4$")[1],
                       hash_method="ARGON2ID"
                       )
        # the staff is then saved in the database using the orm
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

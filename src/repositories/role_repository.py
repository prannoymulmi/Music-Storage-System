from typing import Any

from sqlmodel import Session, select

from models.role import Role

""" Using the repository pattern to create an abstraction between the model and database 
logic separating the persistence concerns for role database."""
class RoleRepository:
    """ Get User Data based on name"""

    def get_role_by_id(self, session: Session, role_id: int) -> Any:
        statement = select(Role).where(
            Role.id == role_id)
        result = session.exec(statement)
        data = result.one()
        return data

    def create_and_add_role(self, session: Session, role: Role):
        session.add(role)
        session.commit()
        session.refresh(role)
        return role

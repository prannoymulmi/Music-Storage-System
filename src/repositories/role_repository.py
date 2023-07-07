from typing import Any

from sqlmodel import Session, select

from models.role import Role


class RoleRepository:
    """ Get User Data based on name"""

    def get_role_by_id(self, session: Session, role_id: str) -> Any:
        statement = select(Role).where(
            Role.id == role_id)
        result = session.exec(statement)
        data = result.one()
        return data

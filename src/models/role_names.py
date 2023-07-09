from enum import Enum


class RoleNames(str, Enum):
    admin = "ADMIN"
    normal_user = "NORMAL_USER"
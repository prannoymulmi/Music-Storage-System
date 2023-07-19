from enum import Enum

""" Enums for Roles to check if the inputted roles are valid."""
class RoleNames(str, Enum):
    admin = "ADMIN"
    normal_user = "NORMAL_USER"
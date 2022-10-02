"""
User Enums

Using the enums defined here is a clear and consistent way to use the same abbreviations and full names everywhere.
"""

from enum import Enum


class UserRoleEnum(Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    USER = "user"
    WEB = "web"
    ANDROID = "android"
    IOS = "ios"

    @property
    def full(self):  # pragma: no cover
        lookup = {
            "admin": "Administrator",
            "editor": "Editor",
            "user": "User",
            "web": "Web Application",
            "android": "Android Application",
            "ios": "iOS Application",
        }
        return lookup[self.value]


class UserStatusEnum(Enum):
    ACTIVE = "active"
    PENDING = "pending"

    @property
    def full(self):  # pragma: no cover
        lookup = {
            "active": "Active",
            "pending": "Pending",
        }
        return lookup[self.value]
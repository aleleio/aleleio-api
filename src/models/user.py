from datetime import datetime
import uuid

from pony.orm import *

from src.models.user_enums import UserRoleEnum, UserStatusEnum


def define_entities_user(db):

    class User(db.Entity):
        role_user = UserRoleEnum.USER.value
        status_pending = UserStatusEnum.PENDING.value

        created = Required(datetime, default=datetime.utcnow)
        created_by = Required(int)  # user_id, may also be user:web_application
        login = Required(str, unique=True)
        fullname = Optional(str)
        hashed_password = Required(str)
        api_key = Required(str, default=lambda: str(uuid.uuid4()), unique=True)
        role = Required(str, default=role_user)
        status = Required(str, default=status_pending)
        protected = Required(bool, default=False)

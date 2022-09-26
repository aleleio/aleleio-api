from datetime import datetime
import uuid

from pony.orm import *

from src.models.user_enums import UserRoleEnum, UserStatusEnum


def define_entities_user(udb):

    class User(udb.Entity):
        created = Required(datetime, default=datetime.utcnow)
        created_by = Required(int)  # user_id
        login = Required(str, unique=True)
        fullname = Optional(str)
        hashed_password = Required(str)
        api_key = Required(str, default=lambda: str(uuid.uuid4()), unique=True)
        role = Required(str, default=UserRoleEnum.USER.value)
        status = Required(str, default=UserStatusEnum.PENDING.value)
        protected = Required(bool, default=False)

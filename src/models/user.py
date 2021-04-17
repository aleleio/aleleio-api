from datetime import datetime
import uuid

from pony.orm import *

from src.models import UserRoleEnum, UserStatusEnum

db_users = Database()


class User(db_users.Entity):
    created = Required(datetime, default=datetime.utcnow)
    created_by = Required(int)  # user_id, may also be user:web_application
    login = Required(str, unique=True)
    fullname = Optional(str)
    hashed_password = Required(str)
    api_key = Required(str, default=lambda: str(uuid.uuid4()), unique=True)
    role = Required(str, default=UserRoleEnum.USER)
    status = Required(str, default=UserStatusEnum.PENDING)
    protected = Required(bool, default=False)

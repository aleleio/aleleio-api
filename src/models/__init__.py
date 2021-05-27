"""
Importing all models in models/__init__ allows to import from src.models directly.
"""

from .game import *  # db_games database object comes from here
from .meta import *
from .user import *  # db_users database object comes from here
from .game_enums import *
from .user_enums import *
from .schema import *

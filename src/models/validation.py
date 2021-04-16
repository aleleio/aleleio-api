"""
Pydantic Models for Validation

FastAPI uses type hints together with pydantics models to validate the API inputs, generate helpful error responses
and create useful documentation.
"""
from typing import Optional

from pydantic.main import BaseModel

from src.models import GameTypeEnum, GroupSizeEnum, GameLengthEnum, GroupNeedEnum


class BasicFilter(BaseModel):
    game_type: Optional[GameTypeEnum]
    group_size: Optional[GroupSizeEnum]
    game_length: Optional[GameLengthEnum]


class GroupNeedsFilter(BaseModel):
    main: Optional[GroupNeedEnum]
    aux1: Optional[GroupNeedEnum]
    aux2: Optional[GroupNeedEnum]


class GameQuery(BaseModel):
    basic: Optional[BasicFilter] = None
    group_needs: Optional[GroupNeedsFilter] = None
    limit: Optional[int]

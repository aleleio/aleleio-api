"""
Pydantic Models for Validation

FastAPI uses type hints together with pydantics models to validate the API inputs, generate helpful error responses
and create useful documentation.
"""
from typing import Optional

from pydantic.main import BaseModel

from src.models import GameTypeEnum, GroupSizeEnum, GameLengthEnum, GroupNeedEnum


class GameQuery(BaseModel):
    # Basic Query
    game_type: Optional[GameTypeEnum]
    group_size: Optional[GroupSizeEnum]
    game_length: Optional[GameLengthEnum]
    # Group Needs Query
    main: Optional[GroupNeedEnum]
    aux1: Optional[GroupNeedEnum]
    aux2: Optional[GroupNeedEnum]
    # Additional Options
    limit: Optional[int]

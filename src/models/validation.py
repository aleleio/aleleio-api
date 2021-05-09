"""
Pydantic Models for Validation

FastAPI uses type hints together with pydantics models to validate the API inputs, generate helpful error responses
and create useful documentation.
"""
from typing import Optional, List

from pydantic.fields import Field
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


class GroupNeedCreation(BaseModel):
    slug: GroupNeedEnum = Field(..., min_length=1)
    score: int = Field(..., ge=0, lt=100)


class PostRequestGame(BaseModel):
    names: List[str] = Field(..., min_items=1, min_length=1)
    descriptions: List[str] = Field(..., min_items=1, min_length=1)
    game_types: List[GameTypeEnum] = Field(..., min_items=1)
    game_lengths: List[GameLengthEnum] = Field(..., min_items=1)
    group_sizes: List[GroupSizeEnum] = Field(..., min_items=1)
    group_needs: List[GroupNeedCreation] = list()  # optional, but needs to be iterable
    materials: List[str] = list()  # optional, but needs to be iterable
    prior_prep: str = Field(None, min_length=1)
    exhausting: bool = False
    touching: bool = False
    scalable: bool = False
    digital: bool = False

    class Config:
        extra = 'forbid'  # forbid additional attributes

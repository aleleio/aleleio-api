"""
Pydantic Models for Validation

FastAPI uses type hints together with pydantics models to validate the API inputs, generate helpful error responses
and create useful documentation.
"""
import datetime
from typing import Optional, List, Type

from pydantic.fields import Field
from pydantic.main import BaseModel, create_model

from src.models import GameTypeEnum, GroupSizeEnum, GameLengthEnum, GroupNeedEnum, Game


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


class GameOut(BaseModel):
    id: int
    names: List[create_model('names', slug=(str, ...), full=(str, ...))] = Field(..., min_items=1)
    descriptions: List[create_model('descriptions', text=(str, ...))] = Field(..., min_items=1)
    game_types: List[create_model('game_types', slug=(str, ...), full=(str, ...))] = Field(..., min_items=1)
    game_lengths: List[create_model('game_lengths', slug=(str, ...), full=(str, ...))] = Field(..., min_items=1)
    group_sizes: List[create_model('group_sizes', slug=(str, ...), full=(str, ...))] = Field(..., min_items=1)
    group_needs: List[create_model('group_needs', slug=(str, ...), full=(str, ...), value=(int, ...))]
    materials: List[create_model('materials', slug=(str, ...), full=(str, ...))]
    prior_prep: str
    exhausting: bool
    touching: bool
    scalable: bool
    digital: bool
    # Meta
    meta: create_model('meta', timestamp=(datetime.datetime, ...), author_id=(int, ...))
    license: create_model('license', name=(str, ...), url=(str, ...), owner=(str, ...), owner_url=(str, ...)) = Field(...)
    references: List[create_model('references', slug=(str, ...), full=(str, ...), url=(str, ...))]

    class Config:
        extra = 'forbid'


class GameInGroupNeed(BaseModel):
    slug: GroupNeedEnum = Field(..., min_length=1)
    score: int = Field(..., ge=0, le=5)


class GameIn(BaseModel):
    """Used for Game creation
    """
    names: List[str]
    descriptions: List[str]
    game_types: List[GameTypeEnum]
    game_lengths: List[GameLengthEnum]
    group_sizes: List[GroupSizeEnum]
    group_needs: List[GameInGroupNeed] = list()  # optional, but needs to be iterable
    materials: List[str] = list()  # optional, but needs to be iterable
    prior_prep: str = Field(None, min_length=1)
    exhausting: bool = False
    touching: bool = False
    scalable: bool = False
    digital: bool = False
    # Meta
    license: create_model('license',
                          name="CC BY-SA 4.0",
                          url="https://creativecommons.org/licenses/by-sa/4.0/",
                          owner="European Youth Parliament",
                          owner_url="https://eyp.org/",
                          )

    class Config:
        extra = 'forbid'  # forbid additional attributes
        schema_extra = {
            "example": {
                    "names": ["Alele Kita Bonga", "Alele Kita Conga"],
                    "descriptions": ["This call and response song is about the worship of watermelons (or fish?). Position yourself in a big circle and have participants repeat these lyrics after you:..."],
                    "game_types": ["ice", "ener"],
                    "group_sizes": ["large", "multiple", "event"],
                    "game_lengths": ["short"],
                    "group_needs": [{"slug": "energy", "score": 4}],
                    "scalable": "true",
                }
            }


class CollectionIn(BaseModel):
    games: List[Type[Game]]
    full: str
    slug: Optional[str]


class ReferenceIn(BaseModel):
    game_slug: str
    full: str
    url: Optional[str]



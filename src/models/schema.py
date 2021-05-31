"""
Pydantic Schemas for Validation

FastAPI uses type hints together with pydantics models to validate the API inputs, generate helpful error responses
and create useful documentation.
"""
import datetime
from typing import Optional, Type, Any

from pydantic import validator
from pydantic.fields import Field
from pydantic.main import BaseModel, create_model

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


class GameORM(BaseModel):
    id: int
    names: list[Any]
    descriptions: list[Any]
    game_types: list[Any]
    game_lengths: list[Any]
    group_sizes: list[Any]
    group_need_scores: list[Any] = Field(list(), alias='group_needs')
    materials: list[Any]
    prior_prep: str
    exhausting: bool
    touching: bool
    scalable: bool
    digital: bool
    meta: Any
    license: Any
    references: list[Any]

    @validator('names', 'descriptions', 'game_types', 'game_lengths', 'group_sizes', 'group_need_scores', 'materials', 'references', pre=True, allow_reuse=True)
    def pony_set_to_list(cls, values):
        return [v.to_dict(with_lazy=True) for v in values]

    @validator('meta', 'license', pre=True, allow_reuse=True)
    def pony_entity_to_dict(cls, value):
        return value.to_dict()

    class Config:
        orm_mode = True


class GameOut(BaseModel):
    id: int
    names: list[create_model('names', slug=(str, ...), full=(str, ...))]
    descriptions: list[create_model('descriptions', text=(str, ...))]
    game_types: list[create_model('game_types', slug=(str, ...), full=(str, ...))]
    game_lengths: list[create_model('game_lengths', slug=(str, ...), full=(str, ...))]
    group_sizes: list[create_model('group_sizes', slug=(str, ...), full=(str, ...))]
    group_needs: list[create_model('group_needs', slug=(str, ...), full=(str, ...), value=(int, ...))]
    materials: list[create_model('materials', slug=(str, ...), full=(str, ...))]
    prior_prep: str
    exhausting: bool
    touching: bool
    scalable: bool
    digital: bool
    # Meta
    meta: create_model('meta', timestamp=(datetime.datetime, ...), author_id=(int, ...))
    license: create_model('license', name=(str, ...), url=(str, ...), owner=(str, ...), owner_url=(str, ...))
    references: list[create_model('references', slug=(str, ...), full=(str, ...), url=(str, ...))]

    class Config:
        extra = 'forbid'


class GameInGroupNeed(BaseModel):
    slug: GroupNeedEnum = Field(..., min_length=1)
    score: int = Field(..., ge=0, le=5)


class GameIn(BaseModel):
    """Used for Game creation
    """
    names: list[str]
    descriptions: list[str]
    game_types: list[GameTypeEnum]
    game_lengths: list[GameLengthEnum]
    group_sizes: list[GroupSizeEnum]
    group_needs: list[GameInGroupNeed] = list()  # optional, but needs to be iterable
    materials: list[str] = list()  # optional, but needs to be iterable
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


class GameInPatch(GameIn):
    game_types: list[GameTypeEnum] = None


class CollectionIn(BaseModel):
    games: list[Any]  # list[Type[Game]]
    full: str
    slug: Optional[str]


class ReferenceOut(BaseModel):
    games: list[Any]
    timestamp: datetime.datetime
    slug: str
    full: str
    url: str

    @validator('games', pre=True)
    def pony_set_to_list(cls, values):
        return [v.to_dict(with_lazy=True, only='id') for v in values]

    class Config:
        orm_mode = True


class ReferenceIn(BaseModel):
    game_slug: str
    full: str
    url: Optional[str]

"""
Pydantic Models for Validation

FastAPI uses type hints together with pydantics models to validate the API inputs, generate helpful error responses
and create useful documentation.
"""
from typing import Optional, List

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


class GameOut(BaseModel):
    id: int
    names: List[create_model('names', slug=(str, ...), full=(str, ...))] = Field(..., min_items=1)
    descriptions: List[create_model('descriptions', text=(str, ...))] = Field(..., min_items=1)
    game_types: List[create_model('game_types', slug=(str, ...), full=(str, ...))] = Field(..., min_items=1)
    game_lengths: List[create_model('game_lengths', slug=(str, ...), full=(str, ...))] = Field(..., min_items=1)
    group_sizes: List[create_model('group_sizes', slug=(str, ...), full=(str, ...))] = Field(..., min_items=1)
    group_needs: List[create_model('group_needs', slug=(str, ...), full=(str, ...), value=(int, ...))]
    materials: List[str]
    prior_prep: str
    exhausting: bool
    touching: bool
    scalable: bool
    digital: bool

    # class Config:
    #     extra = 'forbid'


class GameInGroupNeed(BaseModel):
    slug: GroupNeedEnum = Field(..., min_length=1)
    score: int = Field(..., ge=0, le=5)


class GameIn(BaseModel):
    names: List[str] = Field(..., min_items=1, min_length=1)
    descriptions: List[str] = Field(..., min_items=1, min_length=1)
    game_types: List[GameTypeEnum] = Field(..., min_items=1)
    game_lengths: List[GameLengthEnum] = Field(..., min_items=1)
    group_sizes: List[GroupSizeEnum] = Field(..., min_items=1)
    group_needs: List[GameInGroupNeed] = list()  # optional, but needs to be iterable
    materials: List[str] = list()  # optional, but needs to be iterable
    prior_prep: str = Field(None, min_length=1)
    exhausting: bool = False
    touching: bool = False
    scalable: bool = False
    digital: bool = False
    license: str = "CC BY-SA 4.0"
    license_url: str = "https://creativecommons.org/licenses/by-sa/4.0/"
    license_owner: str = "European Youth Parliament"
    license_owner_url: str = "https://eyp.org/"

class Config:
        extra = 'forbid'  # forbid additional attributes
        schema_extra = {
            "example": {
                    "names": ["Alele Kita Bonga", "Alele Kita Conga"],
                    "descriptions": ["This call and response song is about the worship of watermelons (or fish?). Position yourself in a big circle and have participants repeat these lyrics after you:..."],
                    "game_types": ["ice", "ener"],
                    "group_sizes": ["large", "multiple", "event"],
                    "game_lengths": ["short"],
                    "group_needs": [{"slug": "energy", "score": 80}],
                    "scalable": "true",
                }
            }

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class GameType(Enum):
    ICE = "ice"
    ENER = "ener"
    TRUST = "trust"
    PROB = "prob"
    NAME = "name"
    BRAIN = "brain"
    SONG = "song"
    RACE = "race"
    GTK = "gtk"

    @property
    def full(self):
        lookup = {
            "ice": "Ice Breaker",
            "ener": "Energizer",
            "trust": "Trust Game",
            "prob": "Problem Solver",
            "name": "Name Game",
            "brain": "Brainstorming Activity",
            "song": "Song",
            "race": "Race",
            "gtk": "Getting-to-Know Game",
        }
        return lookup[self.value]


class GameLength(Enum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"

    @property
    def full(self):
        lookup = {
            "short": "<10 minutes",
            "medium": "10-30 minutes",
            "long": "30-120 minutes",
        }
        return lookup[self.value]


class GroupSize(Enum):
    SMALL = "small"
    LARGE = "large"
    MULTIPLE = "multiple"
    EVENT = "event"

    @property
    def full(self):
        lookup = {
            "small": "2-7 people",
            "large": "13-16 people",
            "multiple": "15-40 people",
            "event": "50-300 people",
        }
        return lookup[self.value]


class GroupNeeds(Enum):
    NAMES = "names"
    ENERGY = "ener"
    HONESTY = "hon"
    STRATEGY = "strat"
    INSPIRATION = "insp"
    IDENTITY = "id"

    @property
    def full(self):
        lookup = {
            "names": "First Steps",
            "ener": "Group Energy",
            "hon": "Foster Honesty & Trust",
            "strat": "Practice Strategy & Co-operation",
            "insp": "Inspiration",
            "why": "Team \'Why\'",
            "id": "Group Identity",
        }
        return lookup[self.value]


class BasicFilter(BaseModel):
    game_type: Optional[GameType]
    group_size: Optional[GroupSize]
    game_length: Optional[GameLength]


class GroupNeedsFilter(BaseModel):
    main: Optional[GroupNeeds]
    aux1: Optional[GroupNeeds]
    aux2: Optional[GroupNeeds]


class GameQuery(BaseModel):
    basic: Optional[BasicFilter] = None
    group_needs: Optional[GroupNeedsFilter] = None
    limit: Optional[int]

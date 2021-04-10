from enum import Enum
from typing import Optional

from pydantic import BaseModel


class GameType(Enum):
    ICE = ("ice", "Ice Breaker")
    ENER = ("ener", "Energizer")
    TRUST = ("trust", "Trust Game")
    PROB = ("prob", "Problem Solver")
    NAME = ("name", "Name Game")
    BRAIN = ("brain", "Brainstorming Activity")
    SONG = ("song", "Song")
    RACE = ("race", "Race")
    GTK = ("gtk", "Getting-to-Know Game")

    def __init__(self, short, full):
        self.short = short
        self.full = full


class GameLength(Enum):
    SHORT = ("short", "<10 minutes")
    MEDIUM = ("medium", "10-30 minutes")
    LONG = ("long", "30-120 minutes")

    def __init__(self, short, full):
        self.short = short
        self.full = full


class GroupSize(Enum):
    SMALL = ("small", "2-7 people")
    LARGE = ("large", "13-16 people")
    MULTIPLE = ("multiple", "15-40 people")
    EVENT = ("event", "50-300 people")

    def __init__(self, short, full):
        self.short = short
        self.full = full


class GroupNeeds(Enum):
    NAMES = ("names", "First Steps")
    ENERGY = ("ener", "Group Energy")
    HONESTY = ("hon", "Foster Honesty & Trust")
    STRATEGY = ("strat", "Practice Strategy & Co-operation")
    INSPIRATION = ("insp", "Inspiration")
    WHY = ("why", "Team \'Why\'")
    IDENTITY = ("id", "Group Identity")

    def __init__(self, short, full):
        self.short = short
        self.full = full


class BasicFilter(BaseModel):
    game_type: Optional[str]
    group_size: Optional[str]
    game_length: Optional[str]


class GroupNeedsFilter(BaseModel):
    main: Optional[str]
    aux1: Optional[str]
    aux2: Optional[str]


class GameQuery(BaseModel):
    basic: Optional[BasicFilter] = None
    group_needs: Optional[GroupNeedsFilter] = None
    limit: Optional[int]

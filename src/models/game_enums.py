"""
Game Enums

Using the enums defined here is a clear and consistent way to use the same abbreviations and full names everywhere.

Enums are also stored in the database (e.g. GameTypeEnum -> GameType.slug, GameType.full) but a central definition is
useful, when they are not linked or to initialize the database.
"""

from enum import Enum


class GameTypeEnum(str, Enum):
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


class GameLengthEnum(str, Enum):
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


class GroupSizeEnum(str, Enum):
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


class GroupNeedEnum(str, Enum):
    FIRST = "first"
    ENERGY = "energy"
    HONESTY = "honesty"
    STRATEGY = "strategy"
    INSPIRATION = "inspiration"
    WHY = "why"
    GROUPID = "groupid"

    @property
    def full(self):
        lookup = {
            "first": "First Steps",
            "energy": "Group Energy",
            "honesty": "Foster Honesty & Trust",
            "strategy": "Practice Strategy & Co-operation",
            "inspiration": "Inspiration",
            "why": "Team \"Why\"",
            "groupid": "Group Identity",
        }
        return lookup[self.value]

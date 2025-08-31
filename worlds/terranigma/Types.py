# Terranigma Types.py - custom data types and classes
# Based on the skeleton structure but customized for Terranigma

from enum import IntEnum
from typing import NamedTuple, Optional
from BaseClasses import Location, Item, ItemClassification

# Custom Location and Item classes for Terranigma
class TerranigmaLocation(Location):
    game = "Terranigma"

class TerranigmaItem(Item):
    game = "Terranigma"

# Data structures for items and locations
class ItemData(NamedTuple):
    ap_code: Optional[int]
    classification: ItemClassification
    count: Optional[int] = 1

class LocData(NamedTuple):
    ap_code: Optional[int]
    region: Optional[str]

# Enums for different game progression stages
class ProgressionStage(IntEnum):
    UNDERWORLD = 1
    SURFACE_WORLD = 2
    ANCIENT_CIVILIZATION = 3
    MEDIEVAL_CIVILIZATION = 4
    MODERN_CIVILIZATION = 5
    FINAL_AREAS = 6

# Mapping for progression stages (if needed for options)
progression_stage_to_name = {
    ProgressionStage.UNDERWORLD: "Underworld",
    ProgressionStage.SURFACE_WORLD: "Surface World",
    ProgressionStage.ANCIENT_CIVILIZATION: "Ancient Times",
    ProgressionStage.MEDIEVAL_CIVILIZATION: "Medieval Times",
    ProgressionStage.MODERN_CIVILIZATION: "Modern Times",
    ProgressionStage.FINAL_AREAS: "Final Areas"
}

# Item type categories for organization
class TerranigmaItemType(IntEnum):
    KEY_ITEM = 1
    WEAPON = 2
    ARMOR = 3
    CONSUMABLE = 4
    GEMS = 5
    TRAP = 6
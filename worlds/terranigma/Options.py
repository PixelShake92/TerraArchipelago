# Terranigma Options.py - player customization options

from typing import List, Dict, Any
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Choice, OptionGroup, Toggle, Range

def create_option_groups() -> List[OptionGroup]:
    """Create organized option groups for the web interface"""
    option_group_list: List[OptionGroup] = []
    for name, options in terranigma_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))
    return option_group_list

class StartingRegion(Choice):
    """
    Determines which region you'll start with access to.
    Crysta is the normal start. Other options provide early access to later areas.
    """
    display_name = "Starting Region"
    option_crysta = 0
    option_lumina = 1
    option_louran = 2
    option_loire = 3
    option_freedom = 4
    default = 0

class KeyItemPlacement(Choice):
    """
    Controls how key progression items are distributed.
    Early: More key items available in early locations.
    Balanced: Key items distributed evenly throughout progression.
    Late: Key items more likely to be in later locations.
    """
    display_name = "Key Item Placement"
    option_early = 0
    option_balanced = 1
    option_late = 2
    default = 1

class EquipmentScaling(Toggle):
    """
    When enabled, equipment power scales with game progression.
    Later equipment will generally be more powerful.
    """
    display_name = "Scale Equipment Power"

class ShopRandomization(Toggle):
    """
    When enabled, shop contents will be randomized and included as locations.
    This significantly increases the number of available checks.
    """
    display_name = "Randomize Shops"

class MagicRandomization(Toggle):
    """
    When enabled, magic spells will be randomized as items instead of learned normally.
    """
    display_name = "Randomize Magic"

class BossDifficulty(Choice):
    """
    Adjusts boss difficulty scaling.
    Normal: Vanilla boss difficulty.
    Buffed: Bosses have increased stats.
    Random: Boss stats randomized.
    """
    display_name = "Boss Difficulty"
    option_normal = 0
    option_buffed = 1
    option_random = 2
    default = 0

class TrapChance(Range):
    """
    Determines the chance for any junk item to become a trap.
    Set it to 0 for no traps.
    """
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 10

class SpeedTrapWeight(Range):
    """
    The weight of speed traps in the trap pool.
    Speed traps temporarily slow down Ark's movement.
    """
    display_name = "Speed Trap Weight"
    range_start = 0
    range_end = 100
    default = 33

class DamageTrapWeight(Range):
    """
    The weight of damage traps in the trap pool.
    Damage traps temporarily reduce Ark's attack power.
    """
    display_name = "Damage Trap Weight"
    range_start = 0
    range_end = 100
    default = 33

class ConfusionTrapWeight(Range):
    """
    The weight of confusion traps in the trap pool.
    Confusion traps temporarily reverse movement controls.
    """
    display_name = "Confusion Trap Weight"
    range_start = 0
    range_end = 100
    default = 34

@dataclass
class TerranigmaOptions(PerGameCommonOptions):
    starting_region: StartingRegion
    key_item_placement: KeyItemPlacement
    equipment_scaling: EquipmentScaling
    shop_randomization: ShopRandomization
    magic_randomization: MagicRandomization
    boss_difficulty: BossDifficulty
    trap_chance: TrapChance
    speed_trap_weight: SpeedTrapWeight
    damage_trap_weight: DamageTrapWeight
    confusion_trap_weight: ConfusionTrapWeight

# Organization of options into groups for the web interface
terranigma_option_groups: Dict[str, List[Any]] = {
    "General Options": [
        StartingRegion, KeyItemPlacement, EquipmentScaling
    ],
    "Randomization Options": [
        ShopRandomization, MagicRandomization, BossDifficulty
    ],
    "Trap Options": [
        TrapChance, SpeedTrapWeight, DamageTrapWeight, ConfusionTrapWeight
    ]
}
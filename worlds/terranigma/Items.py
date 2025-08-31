# Terranigma Items.py - defines all items in the game for Archipelago
# Based on actual Terranigma Randomizer data

import logging
from BaseClasses import Item, ItemClassification
from .Types import ItemData, TerranigmaItem
from .Locations import get_total_locations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from . import TerranigmaWorld

# Base ID for all Terranigma items - choose a unique range
BASE_ID = 700000

# Item type flags (similar to Kirby Super Star approach)
PROGRESSION_FLAG = 0x000  # 700000-700255
WEAPON_FLAG = 0x100       # 700256-700511  
ARMOR_FLAG = 0x200        # 700512-700767
CONSUMABLE_FLAG = 0x300   # 700768-701023
GEM_FLAG = 0x400          # 701024-701279
TRAP_FLAG = 0x500         # 701280-701535

def create_itempool(world: "TerranigmaWorld") -> List[Item]:
    """Create the complete item pool for Terranigma"""
    itempool: List[Item] = []
    
    # Add all progression items
    for item_name, item_data in progression_items.items():
        if item_name == "Starstone":
            # Add 5 Starstones as required by the logic
            for i in range(5):
                itempool.append(create_item(world, item_name))
        else:
            itempool.append(create_item(world, item_name))
    
    # Add useful items (equipment and consumables)
    for item_name in useful_items.keys():
        itempool.append(create_item(world, item_name))
    
    # Create and place victory item
    victory = create_item(world, "Victory")
    world.multiworld.get_location("Dark Gaia Defeated", world.player).place_locked_item(victory)
    
    # Fill remaining slots with filler items and traps
    total_locations = get_total_locations(world) - 1  # -1 for victory
    items_needed = total_locations - len(itempool)
    
    if items_needed > 0:
        itempool += create_junk_items(world, items_needed)
    
    return itempool

def create_item(world: "TerranigmaWorld", name: str) -> Item:
    """Create a single item"""
    data = item_table[name]
    return TerranigmaItem(name, data.classification, data.ap_code, world.player)

def create_junk_items(world: "TerranigmaWorld", count: int) -> List[Item]:
    """Create junk items and traps to fill remaining slots"""
    trap_chance = world.options.trap_chance.value
    junk_pool: List[Item] = []
    junk_list: Dict[str, int] = {}
    trap_list: Dict[str, int] = {}
    
    # Build junk item list
    for name in item_table.keys():
        ic = item_table[name].classification
        if ic == ItemClassification.filler:
            junk_list[name] = junk_weights.get(name, 1)
        elif trap_chance > 0 and ic == ItemClassification.trap:
            if name == "Speed Trap":
                trap_list[name] = world.options.speed_trap_weight.value
            elif name == "Damage Trap":
                trap_list[name] = world.options.damage_trap_weight.value
            elif name == "Confusion Trap":
                trap_list[name] = world.options.confusion_trap_weight.value
    
    # Create the items
    for i in range(count):
        if trap_chance > 0 and world.random.randint(1, 100) <= trap_chance and trap_list:
            item_name = world.random.choices(list(trap_list.keys()), weights=list(trap_list.values()), k=1)[0]
            junk_pool.append(world.create_item(item_name))
        else:
            if junk_list:
                item_name = world.random.choices(list(junk_list.keys()), weights=list(junk_list.values()), k=1)[0]
                junk_pool.append(world.create_item(item_name))
    
    return junk_pool

# PROGRESSION ITEMS - Items required to progress through the game
# Based on PROGRESSION_KEY_ITEMS from the Terranigma Randomizer
# Range: BASE_ID + PROGRESSION_FLAG + index (700000-700255)
progression_items = {
    # Chapter 1 key items
    "Sleepless Seal": ItemData(BASE_ID + PROGRESSION_FLAG + 0, ItemClassification.progression),
    "Crystal Thread": ItemData(BASE_ID + PROGRESSION_FLAG + 1, ItemClassification.progression),
    "ElleCape": ItemData(BASE_ID + PROGRESSION_FLAG + 2, ItemClassification.progression),
    "Sharp Claws": ItemData(BASE_ID + PROGRESSION_FLAG + 3, ItemClassification.progression),
    
    # Chapter 2 key items
    "Giant Leaves": ItemData(BASE_ID + PROGRESSION_FLAG + 10, ItemClassification.progression),
    "Ra Dewdrop": ItemData(BASE_ID + PROGRESSION_FLAG + 11, ItemClassification.progression),
    "RocSpear": ItemData(BASE_ID + PROGRESSION_FLAG + 12, ItemClassification.progression),
    "Snowgrass Leaf": ItemData(BASE_ID + PROGRESSION_FLAG + 13, ItemClassification.progression),
    
    # Chapter 3 key items
    "Red Scarf": ItemData(BASE_ID + PROGRESSION_FLAG + 20, ItemClassification.progression),
    "Holy Seal": ItemData(BASE_ID + PROGRESSION_FLAG + 21, ItemClassification.progression),
    "Mushroom": ItemData(BASE_ID + PROGRESSION_FLAG + 22, ItemClassification.progression),
    "Protect Bell": ItemData(BASE_ID + PROGRESSION_FLAG + 23, ItemClassification.progression),
    "Dog Whistle": ItemData(BASE_ID + PROGRESSION_FLAG + 24, ItemClassification.progression),
    "Ruby": ItemData(BASE_ID + PROGRESSION_FLAG + 25, ItemClassification.progression),
    "Sapphire": ItemData(BASE_ID + PROGRESSION_FLAG + 26, ItemClassification.progression),
    "Black Opal": ItemData(BASE_ID + PROGRESSION_FLAG + 27, ItemClassification.progression),
    "Topaz": ItemData(BASE_ID + PROGRESSION_FLAG + 28, ItemClassification.progression),
    "Tower Key": ItemData(BASE_ID + PROGRESSION_FLAG + 29, ItemClassification.progression),
    "Speed Shoes": ItemData(BASE_ID + PROGRESSION_FLAG + 30, ItemClassification.progression),
    "Engagement Ring": ItemData(BASE_ID + PROGRESSION_FLAG + 31, ItemClassification.progression),
    "Magic Anchor": ItemData(BASE_ID + PROGRESSION_FLAG + 32, ItemClassification.progression),
    "Air Herb": ItemData(BASE_ID + PROGRESSION_FLAG + 33, ItemClassification.progression),
    "Sewer Key": ItemData(BASE_ID + PROGRESSION_FLAG + 34, ItemClassification.progression),
    "Transceiver": ItemData(BASE_ID + PROGRESSION_FLAG + 35, ItemClassification.progression),
    
    # Chapter 4 key items
    "Starstone": ItemData(BASE_ID + PROGRESSION_FLAG + 40, ItemClassification.progression_skip_balancing, 5),
    "Time Bomb": ItemData(BASE_ID + PROGRESSION_FLAG + 41, ItemClassification.progression),
    "Jail Key": ItemData(BASE_ID + PROGRESSION_FLAG + 42, ItemClassification.progression),
    "Ginseng": ItemData(BASE_ID + PROGRESSION_FLAG + 43, ItemClassification.progression),
    
    # Victory condition
    "Victory": ItemData(BASE_ID + PROGRESSION_FLAG + 255, ItemClassification.progression)
}

# WEAPONS - Range: BASE_ID + WEAPON_FLAG + index (700256-700511)
weapon_items = {
    "HexRod": ItemData(BASE_ID + WEAPON_FLAG + 0, ItemClassification.useful),
    "CrySpear": ItemData(BASE_ID + WEAPON_FLAG + 1, ItemClassification.useful),
    "RaSpear": ItemData(BASE_ID + WEAPON_FLAG + 2, ItemClassification.useful),
    "Sticker": ItemData(BASE_ID + WEAPON_FLAG + 3, ItemClassification.useful),
    "Neo Fang": ItemData(BASE_ID + WEAPON_FLAG + 4, ItemClassification.useful),
    "Icepick": ItemData(BASE_ID + WEAPON_FLAG + 5, ItemClassification.useful),
    "BrnzPike": ItemData(BASE_ID + WEAPON_FLAG + 10, ItemClassification.useful),
    "LightRod": ItemData(BASE_ID + WEAPON_FLAG + 11, ItemClassification.useful),
    "SlverPike": ItemData(BASE_ID + WEAPON_FLAG + 12, ItemClassification.useful),
    "FirePike": ItemData(BASE_ID + WEAPON_FLAG + 13, ItemClassification.useful),
    "Trident": ItemData(BASE_ID + WEAPON_FLAG + 14, ItemClassification.useful),
    "SoulWand": ItemData(BASE_ID + WEAPON_FLAG + 15, ItemClassification.useful),
    "ThunPike": ItemData(BASE_ID + WEAPON_FLAG + 16, ItemClassification.useful),
    "SeaSpear": ItemData(BASE_ID + WEAPON_FLAG + 20, ItemClassification.useful),
    "GeoStaff": ItemData(BASE_ID + WEAPON_FLAG + 21, ItemClassification.useful),
    "DrgnPike": ItemData(BASE_ID + WEAPON_FLAG + 22, ItemClassification.useful),
    "3PartRod": ItemData(BASE_ID + WEAPON_FLAG + 23, ItemClassification.useful),
    "LghtPike": ItemData(BASE_ID + WEAPON_FLAG + 24, ItemClassification.useful),
    "Fauchard": ItemData(BASE_ID + WEAPON_FLAG + 25, ItemClassification.useful),
}

# ARMOR - Range: BASE_ID + ARMOR_FLAG + index (700512-700767)
armor_items = {
    "Tanned": ItemData(BASE_ID + ARMOR_FLAG + 0, ItemClassification.useful),
    "Leather": ItemData(BASE_ID + ARMOR_FLAG + 1, ItemClassification.useful),
    "SilkRobe": ItemData(BASE_ID + ARMOR_FLAG + 2, ItemClassification.useful),
    "Chain": ItemData(BASE_ID + ARMOR_FLAG + 10, ItemClassification.useful),
    "Bronze": ItemData(BASE_ID + ARMOR_FLAG + 11, ItemClassification.useful),
    "Iron": ItemData(BASE_ID + ARMOR_FLAG + 12, ItemClassification.useful),
    "Steel": ItemData(BASE_ID + ARMOR_FLAG + 20, ItemClassification.useful),
    "Silver": ItemData(BASE_ID + ARMOR_FLAG + 21, ItemClassification.useful),
    "Crystal": ItemData(BASE_ID + ARMOR_FLAG + 22, ItemClassification.useful),
    "KingArmr": ItemData(BASE_ID + ARMOR_FLAG + 30, ItemClassification.useful),
    "Gaia": ItemData(BASE_ID + ARMOR_FLAG + 31, ItemClassification.useful),
}

# CONSUMABLES - Range: BASE_ID + CONSUMABLE_FLAG + index (700768-701023)
consumable_items = {
    "M.Bulb": ItemData(BASE_ID + CONSUMABLE_FLAG + 0, ItemClassification.useful),
    "P. Cure": ItemData(BASE_ID + CONSUMABLE_FLAG + 1, ItemClassification.useful),
    "S. Bulb": ItemData(BASE_ID + CONSUMABLE_FLAG + 2, ItemClassification.useful),
    "Cure": ItemData(BASE_ID + CONSUMABLE_FLAG + 3, ItemClassification.useful),
    "Stardew": ItemData(BASE_ID + CONSUMABLE_FLAG + 4, ItemClassification.useful),
    "Serum": ItemData(BASE_ID + CONSUMABLE_FLAG + 10, ItemClassification.useful),
    "H.Water": ItemData(BASE_ID + CONSUMABLE_FLAG + 11, ItemClassification.useful),
    "STR Potion": ItemData(BASE_ID + CONSUMABLE_FLAG + 12, ItemClassification.useful),
    "DEF Potion": ItemData(BASE_ID + CONSUMABLE_FLAG + 13, ItemClassification.useful),
    "Luck Potion": ItemData(BASE_ID + CONSUMABLE_FLAG + 14, ItemClassification.useful),
    "Life Potion": ItemData(BASE_ID + CONSUMABLE_FLAG + 15, ItemClassification.useful),
}

# JUNK/FILLER ITEMS - Gems - Range: BASE_ID + GEM_FLAG + index (701024-701279)
junk_items = {
    "30 Gems": ItemData(BASE_ID + GEM_FLAG + 0, ItemClassification.filler),
    "50 Gems": ItemData(BASE_ID + GEM_FLAG + 1, ItemClassification.filler),
    "100 Gems": ItemData(BASE_ID + GEM_FLAG + 2, ItemClassification.filler),
    "200 Gems": ItemData(BASE_ID + GEM_FLAG + 10, ItemClassification.filler),
    "300 Gems": ItemData(BASE_ID + GEM_FLAG + 11, ItemClassification.filler),
    "500 Gems": ItemData(BASE_ID + GEM_FLAG + 12, ItemClassification.filler),
    "753 Gems": ItemData(BASE_ID + GEM_FLAG + 20, ItemClassification.filler),
    "892 Gems": ItemData(BASE_ID + GEM_FLAG + 21, ItemClassification.filler),
    "1003 Gems": ItemData(BASE_ID + GEM_FLAG + 22, ItemClassification.filler)
}

# TRAP ITEMS - Range: BASE_ID + TRAP_FLAG + index (701280-701535)
trap_items = {
    "Speed Trap": ItemData(BASE_ID + TRAP_FLAG + 0, ItemClassification.trap),
    "Damage Trap": ItemData(BASE_ID + TRAP_FLAG + 1, ItemClassification.trap),
    "Confusion Trap": ItemData(BASE_ID + TRAP_FLAG + 2, ItemClassification.trap)
}

# Combine equipment items for convenience
useful_items = {
    **weapon_items,
    **armor_items,
    **consumable_items,
}

# Junk item weights for random selection
junk_weights = {
    "30 Gems": 15,
    "50 Gems": 20, 
    "100 Gems": 25,
    "200 Gems": 20,
    "300 Gems": 15,
    "500 Gems": 10,
    "753 Gems": 8,
    "892 Gems": 5,
    "1003 Gems": 3
}

# Combine all item tables
item_table = {
    **progression_items,
    **useful_items,
    **junk_items,
    **trap_items
}

# Junk item weights for random selection
junk_weights = {
    "30 Gems": 15,
    "50 Gems": 20, 
    "100 Gems": 25,
    "200 Gems": 20,
    "300 Gems": 15,
    "500 Gems": 10,
    "753 Gems": 8,
    "892 Gems": 5,
    "1003 Gems": 3
}

# Combine all item tables
item_table = {
    **progression_items,
    **useful_items,
    **junk_items,
    **trap_items
}
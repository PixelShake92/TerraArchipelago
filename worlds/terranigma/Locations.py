# Terranigma Locations.py - defines all check locations in the game
# Based on actual chest data from the Terranigma Randomizer KNOWN_CHESTS

from typing import Dict, TYPE_CHECKING
import logging

from .Types import LocData

if TYPE_CHECKING:
    from . import TerranigmaWorld

def get_total_locations(world: "TerranigmaWorld") -> int:
    """Get the total number of locations based on options"""
    total = 0
    for name in location_table:
        if is_valid_location(world, name):
            total += 1
    
    return total

def get_location_names() -> Dict[str, int]:
    """Get mapping of location names to their AP codes"""
    names = {name: data.ap_code for name, data in location_table.items()}
    return names

def is_valid_location(world: "TerranigmaWorld", name: str) -> bool:
    """Check if a location should be included based on options"""
    # All locations are valid for now - can add option filtering here later
    return True

# CHEST LOCATIONS - Based on actual KNOWN_CHESTS data from your project
# Using real mapName values and chest IDs - ALL CHESTS INCLUDED
chest_locations = {
    # Louran Chests
    "Louran FireRing Chest": LocData(70010006, "Louran Region"),
    "Safarium S.Bulb Chest": LocData(70010010, "Surface Initial"),
    "Loire Castle Tower 3rd Floor Protect Bell": LocData(70010011, "Loire Castle"),
    "Nirlake House Tin Sheet Chest": LocData(70010012, "Norfest Region"),
    "Mush Near Loire L.Bulb Chest": LocData(70010013, "Norfest Region"),
    
    # Tower Chests (128-137) - The 5 towers in the underworld
    "Tower 1 1st Floor S.Bulb Chest": LocData(70010128, "Underworld Start"),
    "Tower 2 1st Floor S.Bulb Chest": LocData(70010129, "Underworld Start"),
    "Tower 3 1st Floor 44 Gems Chest": LocData(70010130, "Underworld Start"),
    "Tower 3 1st Floor S.Bulb Chest": LocData(70010131, "Underworld Start"),
    "Tower 3 4th Floor Sleepless Seal Chest": LocData(70010132, "Underworld Start"),
    "Tower 4 -1st Floor 44 Gems Chest": LocData(70010134, "Underworld Start"),
    "Tower 4 2nd Floor M.Bulb Chest": LocData(70010135, "Underworld Start"),
    "Tower 4 2nd Floor Life Potion Chest": LocData(70010136, "Underworld Start"),
    "Tower 4 3rd Floor Crystal Thread Chest": LocData(70010137, "Tower4 Area"),
    
    # Tree Cave chests (138-141, 154-156, 211-214, 236-237)
    "Tree Cave Ra Spear Chest": LocData(70010138, "Tree Cave Entrance"),
    "Tree Cave M.Bulb Chest": LocData(70010139, "Tree Cave Entrance"),
    "Tree cave Giant Leaves Chest": LocData(70010140, "Tree Cave Inner"),
    "Tree Cave LeafSuit Chest": LocData(70010141, "Tree Cave Inner"),
    "Tree cave P. Cure Chest": LocData(70010211, "Tree Cave Entrance"),
    "Tree cave Life Potion Chest": LocData(70010212, "Tree Cave Entrance"),
    "Tree cave P. Cure Chest 2": LocData(70010213, "Tree Cave Entrance"),
    "Tree cave S.Bulb Chest": LocData(70010214, "Tree Cave Entrance"),
    "Tree cave S.Bulb Chest 2": LocData(70010236, "Tree Cave Entrance"),
    "Tree cave 42 Gems Chest": LocData(70010237, "Tree Cave Entrance"),
    
    # Grecliff Cave
    "Grecliff Cave RocSpear Chest": LocData(70010142, "Grecliff Middle"),
    
    # Louran area chests
    "Louran-Meilins House Red Scarf Chest": LocData(70010143, "Louran Region"),
    "Louran House M.Bulb Chest": LocData(70010144, "Louran Region"),
    "Louran House Holy Seal Chest": LocData(70010145, "Louran Region"),
    "Louran House LightRod Chest": LocData(70010146, "Louran Region"),
    "Louran Storage P. Cure Chest": LocData(70010189, "Louran Region"),
    "Louran House L.Bulb Chest": LocData(70010190, "Louran Region"),
    "Louran north side room 178 Gems Chest": LocData(70010191, "Louran Region"),
    "Louran north side Zombies STR Potion Chest": LocData(70010251, "Louran Region"),
    
    # Sylvain Castle
    "Sylvain Castle Tower Key Chest": LocData(70010147, "Sylvain Castle"),
    "Sylvain Castle Icepick Chest": LocData(70010148, "Sylvain Castle"),
    "Sylvian Castle Ruby Chest": LocData(70010149, "Sylvain Castle"),
    
    # Stockholm House - Portrait (special handling needed)
    "Stockholm House Portrait Chest": LocData(70010150, "Storkolm Region"),
    
    # Mu areas
    "Mu DEF Potion Chest": LocData(70010234, "Mu Region"),
    "Mu EnbuPike Chest": LocData(70010235, "Mu Region"),
    
    # Lab areas
    "Lab 1F SoulArmr Chest": LocData(70010192, "Lab 1F"),
    "Lab 1F DEF Potion Chest": LocData(70010252, "Lab 1F"),
    
    # Dragoon Castle chests
    "Dragoon Castle 1st Floor Room 1 200 Gems": LocData(70010193, "Dragoon Castle"),
    "Dragoon Castle -1st Floor Room 2 300 Gems": LocData(70010194, "Dragoon Castle"),
    "Dragoon Castle -1st Floor Room 2 L.Bulb": LocData(70010195, "Dragoon Castle"),
    "Dragoon Castle -1st Floor Room 3-A PartRod": LocData(70010196, "Dragoon Castle"),
    
    # Astarica areas
    "Astarica backroom Chest": LocData(70010197, "Astarica Region"),
    "Astarika Starstone Chest": LocData(70010254, "Astarica Region"),
    
    # Great Lakes Cavern
    "Great Lakes Cavern 753 Gems Chest": LocData(70010205, "Great Lakes Cavern"),
    "Great Lakes Cavern Air Herb Chest": LocData(70010206, "Great Lakes Cavern"),
    "Great Lakes Cavern GeoStaff Chest": LocData(70010207, "Great Lakes Cavern"),
    "Great Lakes Cavern DrgnMail Chest": LocData(70010219, "Great Lakes Cavern"),
    
    # Labtower
    "Labtower Life Potion Chest": LocData(70010208, "Labtower"),
    
    # Sewer
    "Sewer KingArmr Chest": LocData(70010209, "Neotokyo Sewer"),
    
    # Mermaid Tower
    "Mermaid Tower 1st sub floor SeaSpear": LocData(70010255, "Mermaid Tower Region"),
    
    # Zue area chests (215-218, 250)
    "Zue DEF Potion Chest": LocData(70010215, "Surface Initial"),
    "Zue P. Cure Chest": LocData(70010216, "Surface Initial"),
    "Zue M.Bulb Chest": LocData(70010217, "Surface Initial"),
    "Zue Sticker Chest": LocData(70010218, "Surface Initial"),
    "Zue M.Bulb Chest 2": LocData(70010250, "Surface Initial"),
    
    # Hidden area chests (210, 220-241)
    "Hidden area Speed Shoes Chest": LocData(70010210, "Hidden Regions"),
    "Hidden area Life Potion Chest": LocData(70010220, "Hidden Regions"),
    "Hidden area 378 Gems Chest": LocData(70010221, "Hidden Regions"),
    "Hidden area M.Bulb Chest": LocData(70010222, "Hidden Regions"),
    "Hidden area 378 Gems Chest 2": LocData(70010223, "Hidden Regions"),
    "Hidden area STR Potion Chest": LocData(70010224, "Hidden Regions"),
    "Hidden area near Odemrock Life Potion": LocData(70010225, "Hidden Regions"),
    "Hidden area near Odemrock 228 Gems": LocData(70010226, "Hidden Regions"),
    "Hidden area 378 Gems Chest 3": LocData(70010227, "Hidden Regions"),
    "Hidden area Luck Potion Chest": LocData(70010228, "Hidden Regions"),
    "Hidden area 1403 Gems Chest": LocData(70010229, "Hidden Regions"),
    "Hidden area near tower BlockRod": LocData(70010231, "Hidden Regions"),
    "Hidden area Sahara 703 Gems": LocData(70010232, "Hidden Regions"),
    "Hidden area Sahara 1003 Gems": LocData(70010233, "Hidden Regions"),
    "Hidden area 961 Gems Chest": LocData(70010238, "Hidden Regions"),
    "Hidden area Part 2 Life Potion": LocData(70010239, "Hidden Regions"),
    "Hidden area Part 2 Sea Mail": LocData(70010240, "Hidden Regions"),
    "Hidden area near Odemrock 892 Gems": LocData(70010241, "Hidden Regions"),
    
    # Surface Initial area chests (157, 159) from PROGRESSION_AREAS data
    "Surface Area Hidden Chest 1": LocData(70010157, "Surface Initial"),
    "Surface Area Hidden Chest 2": LocData(70010159, "Surface Initial"),
    
    # Tree Cave Inner (164) from PROGRESSION_AREAS
    "Tree Cave Inner Hidden Chest": LocData(70010164, "Tree Cave Inner"),
}

# EVENT LOCATIONS - Story progression events
event_locations = {
    "Underworld Awakened": LocData(70010500, "Underworld Start"),
    "Surface World Access": LocData(70010501, "Surface Initial"),
    "Grecliff Boss Defeated": LocData(70010502, "Grecliff Boss"),
    "Louran Flourished": LocData(70010503, "Louran Region"),
    "Loire Castle Accessed": LocData(70010504, "Loire Castle"),
    "Dragoon Castle Opened": LocData(70010505, "Dragoon Castle"),
    "Freedom Liberated": LocData(70010506, "Neotokyo Sewer"),
    "Modern Era Reached": LocData(70010507, "Great Lakes Cavern"),
    "Astarica Accessed": LocData(70010508, "Astarica Region"),
    "Dark Gaia Defeated": LocData(70010509, "Dark Gaia Arena"),
}

# SHOP LOCATIONS - Based on SHOP_LOCATIONS from your progression.py
shop_locations = {
    "Crysta Day Shop": LocData(70010600, "Crysta"),
    "Crysta Night Shop": LocData(70010601, "Crysta"),
    "Lumina stage 1 Shop": LocData(70010602, "Surface Initial"),
    "Lumina stage 2/3 Shop": LocData(70010603, "Surface Initial"),
    "Sanctuar birds Shop": LocData(70010605, "Surface Initial"),
    "Sanctuar pre-birds Shop": LocData(70010606, "Surface Initial"),
    "Safarium Shop": LocData(70010607, "Surface Initial"),
    "Louran Shop": LocData(70010609, "Louran Region"),
    "Lhase - Shop": LocData(70010612, "Norfest Region"),
    "Loire - Shop": LocData(70010613, "Norfest Region"),
    "Freedom - Weapons Shop": LocData(70010624, "Neotokyo Sewer"),
    "Freedom - Armor Shop": LocData(70010628, "Neotokyo Sewer"),
    "Ring Shop": LocData(70010636, "Great Lakes Cavern"),
    "Suncoast - Merchant Shop": LocData(70010639, "Great Lakes Cavern"),
    "Indus River - Ring Shop": LocData(70010650, "Eklemata Region"),
}

# Combine all location tables
location_table = {
    **chest_locations,
    **event_locations,
    **shop_locations,
}
# Terranigma Regions.py - defines the game world structure
# Based on actual progression areas from the Terranigma Randomizer

from BaseClasses import Region
from .Types import TerranigmaLocation
from .Locations import location_table, is_valid_location
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import TerranigmaWorld

def create_regions(world: "TerranigmaWorld"):
    """Create the game world regions based on Terranigma's progression structure"""
    
    # Create Menu region (starting point)
    menu = create_region(world, "Menu")
    
    # CHAPTER 1 - UNDERWORLD
    crysta = create_region_and_connect(world, "Crysta", "Menu -> Crysta", menu)
    tower_babel = create_region_and_connect(world, "Tower of Babel", "Crysta -> Tower of Babel", crysta)
    tree_cave_entrance = create_region_and_connect(world, "Tree Cave Entrance", "Tower of Babel -> Tree Cave", tower_babel)
    tree_cave_inner = create_region_and_connect(world, "Tree Cave Inner", "Tree Cave Entrance -> Tree Cave Inner", tree_cave_entrance)
    sylvain_castle = create_region_and_connect(world, "Sylvain Castle", "Tree Cave -> Sylvain Castle", tree_cave_entrance)
    
    # CHAPTER 2 - SURFACE WORLD  
    surface_initial = create_region_and_connect(world, "Surface Initial", "Tree Cave -> Surface World", tree_cave_inner)
    grecliff_entrance = create_region_and_connect(world, "Grecliff Entrance", "Surface -> Grecliff", surface_initial)
    grecliff_middle = create_region_and_connect(world, "Grecliff Middle", "Grecliff Entrance -> Middle", grecliff_entrance)
    grecliff_boss = create_region_and_connect(world, "Grecliff Boss", "Grecliff Middle -> Boss", grecliff_middle)
    zue = create_region_and_connect(world, "Zue", "Surface -> Zue", surface_initial)
    
    # CHAPTER 3 - CIVILIZATION
    # Eklemata Region (Ancient Civilization)
    eklemata_region = create_region_and_connect(world, "Eklemata Region", "Grecliff -> Eklemata", grecliff_boss)
    louran = create_region_and_connect(world, "Louran", "Eklemata -> Louran", eklemata_region)
    
    # Norfest Region (Medieval Civilization)  
    norfest_region = create_region_and_connect(world, "Norfest Region", "Louran -> Norfest", louran)
    loire_castle = create_region_and_connect(world, "Loire Castle", "Norfest -> Loire Castle", norfest_region)
    dragoon_castle = create_region_and_connect(world, "Dragoon Castle", "Loire -> Dragoon", loire_castle)
    
    # Neo-Tokyo (Modern Civilization)
    neotokyo_sewer = create_region_and_connect(world, "Neotokyo Sewer", "Dragoon -> Neo-Tokyo", dragoon_castle)
    great_lakes_cavern = create_region_and_connect(world, "Great Lakes Cavern", "Neo-Tokyo -> Great Lakes", neotokyo_sewer)
    
    # CHAPTER 4 - MODERN WORLD
    mermaid_tower_region = create_region_and_connect(world, "Mermaid Tower Region", "Great Lakes -> Mermaid Tower", great_lakes_cavern)  
    mu_region = create_region_and_connect(world, "Mu Region", "Mermaid Tower -> Mu", mermaid_tower_region)
    astarica_region = create_region_and_connect(world, "Astarica Region", "Mu -> Astarica", mu_region)
    
    # CHAPTER 5 - FINAL AREAS
    hidden_regions = create_region_and_connect(world, "Hidden Regions", "Surface -> Hidden Areas", surface_initial)
    stockholm = create_region_and_connect(world, "Stockholm", "Surface -> Stockholm", surface_initial)
    labtower = create_region_and_connect(world, "Labtower", "Great Lakes -> Lab", great_lakes_cavern)
    lab_1f = create_region_and_connect(world, "Lab 1F", "Labtower -> Lab 1F", labtower)
    
    # Shop locations
    ring_shop_location = create_region_and_connect(world, "Ring Shop Location", "Great Lakes -> Ring Shop", great_lakes_cavern)
    
    # Final boss area
    dark_gaia_arena = create_region_and_connect(world, "Dark Gaia Arena", "Astarica -> Final Boss", astarica_region)

def create_region(world: "TerranigmaWorld", name: str) -> Region:
    """Create a region and add its locations"""
    reg = Region(name, world.player, world.multiworld)
    
    # Add all locations that belong to this region
    for (key, data) in location_table.items():
        if data.region == name:
            if not is_valid_location(world, key):
                continue
            location = TerranigmaLocation(world.player, key, data.ap_code, reg)
            reg.locations.append(location)
    
    world.multiworld.regions.append(reg)
    return reg

def create_region_and_connect(world: "TerranigmaWorld",
                               name: str, entrance_name: str, connected_region: Region) -> Region:
    """Create a region and connect it to another region"""
    reg: Region = create_region(world, name)
    connected_region.connect(reg, entrance_name)
    return reg
# Terranigma Rules.py - defines progression logic
# Based on KEY_PROGRESSION_POINTS from the Terranigma Randomizer

from worlds.generic.Rules import add_rule
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import TerranigmaWorld

def set_rules(world: "TerranigmaWorld"):
    """Set progression rules based on Terranigma's key item requirements"""
    player = world.player
    multiworld = world.multiworld
    
    # CHAPTER 1 - UNDERWORLD PROGRESSION
    
    # Crystal Thread needed to access Tree Cave
    add_rule(multiworld.get_entrance("Tower of Babel -> Tree Cave", player),
             lambda state: state.has("Crystal Thread", player))
    
    # Ra Dewdrop needed to access Tree Cave Inner areas
    add_rule(multiworld.get_entrance("Tree Cave Entrance -> Tree Cave Inner", player),
             lambda state: state.has("Ra Dewdrop", player))
    
    # CHAPTER 2 - SURFACE WORLD ACCESS
    
    # Giant Leaves + ElleCape needed to access Surface World
    add_rule(multiworld.get_entrance("Tree Cave -> Surface World", player),
             lambda state: state.has("Giant Leaves", player) and state.has("ElleCape", player))
    
    # RocSpear needed to access Grecliff Middle
    add_rule(multiworld.get_entrance("Grecliff Entrance -> Middle", player),
             lambda state: state.has("RocSpear", player))
    
    # Sharp Claws needed to defeat Grecliff Boss
    add_rule(multiworld.get_entrance("Grecliff Middle -> Boss", player),
             lambda state: state.has("Sharp Claws", player))
    
    # CHAPTER 3 - CIVILIZATION PROGRESSION
    
    # Snowgrass Leaf needed to access Eklemata Region (Louran)
    add_rule(multiworld.get_entrance("Grecliff -> Eklemata", player),
             lambda state: state.has("Snowgrass Leaf", player))
    
    # Red Scarf + Holy Seal needed for Louran progression
    add_rule(multiworld.get_entrance("Eklemata -> Louran", player),
             lambda state: state.has("Red Scarf", player) and state.has("Holy Seal", player))
    
    # Protect Bell needed for Loire Castle
    add_rule(multiworld.get_entrance("Norfest -> Loire Castle", player),
             lambda state: state.has("Protect Bell", player))
    
    # Tower Key needed for Dragoon Castle
    add_rule(multiworld.get_entrance("Loire -> Dragoon", player),
             lambda state: state.has("Tower Key", player))
    
    # Ruby, Sapphire, Black Opal, Topaz needed for progression past Dragoon
    # (These are the gems needed for Bloody Mary)
    add_rule(multiworld.get_entrance("Dragoon -> Neo-Tokyo", player),
             lambda state: (state.has("Ruby", player) and 
                           state.has("Sapphire", player) and
                           state.has("Black Opal", player) and
                           state.has("Topaz", player)))
    
    # CHAPTER 4 - MODERN WORLD PROGRESSION
    
    # Sewer Key needed for Neo-Tokyo Sewer
    add_rule(multiworld.get_entrance("Dragoon -> Neo-Tokyo", player),
             lambda state: state.has("Sewer Key", player))
    
    # Transceiver needed for advanced Neo-Tokyo areas
    add_rule(multiworld.get_entrance("Neo-Tokyo -> Great Lakes", player),
             lambda state: state.has("Transceiver", player))
    
    # Engagement Ring needed for Mermaid Tower
    add_rule(multiworld.get_entrance("Great Lakes -> Mermaid Tower", player),
             lambda state: state.has("Engagement Ring", player))
    
    # Magic Anchor needed for Mu Region
    add_rule(multiworld.get_entrance("Mermaid Tower -> Mu", player),
             lambda state: state.has("Magic Anchor", player))
    
    # Air Herb needed for some areas
    # Speed Shoes needed for Hidden Regions
    add_rule(multiworld.get_entrance("Surface -> Hidden Areas", player),
             lambda state: state.has("Speed Shoes", player))
    
    # 5 Starstones needed to access Astarica
    add_rule(multiworld.get_entrance("Mu -> Astarica", player),
             lambda state: state.has("Starstone", player, 5))
    
    # CHAPTER 5 - FINAL PROGRESSION
    
    # Time Bomb and Air Herb needed for certain final areas
    add_rule(multiworld.get_entrance("Astarica -> Final Boss", player),
             lambda state: (state.has("Time Bomb", player) and 
                           state.has("Air Herb", player)))
    
    # Victory condition - defeat Dark Gaia (requires all major progression items)
    multiworld.completion_condition[player] = lambda state: (
        state.has("Victory", player) and
        # Ensure player has core progression items
        state.has("Giant Leaves", player) and
        state.has("ElleCape", player) and
        state.has("RocSpear", player) and
        state.has("Sharp Claws", player) and
        state.has("Holy Seal", player) and
        # Ensure they can access final areas - need 5 Starstones for Astarica
        state.has("Starstone", player, 5) and
        state.has("Time Bomb", player) and
        state.has("Air Herb", player)
    )
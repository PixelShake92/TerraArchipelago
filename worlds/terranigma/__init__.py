# Terranigma Archipelago World implementation

import logging
import os

from BaseClasses import MultiWorld, Item, Tutorial
from worlds.AutoWorld import World, CollectionState, WebWorld
from typing import Dict

from .Locations import get_location_names, get_total_locations
from .Items import create_item, create_itempool, item_table
from .Options import TerranigmaOptions
from .Regions import create_regions
from .Rules import set_rules
from .Types import TerranigmaItem
from .Rom import patch_rom, TerranigmaProcedurePatch  # Added ROM imports

class TerranigmaWeb(WebWorld):
    theme = "grass"
    
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Terranigma for Archipelago. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        ["YourUsername"]
    )]

class TerranigmaWorld(World):
    """
    Terranigma is a single player RPG developed by Quintet for the SNES. You play as Ark who is tasked 
    with re-awakening the world through five acts: the Underworld, Surface World, and three periods of 
    human civilization. This randomizer shuffles key progression items and equipment across the world 
    while maintaining logical progression through the game's complex story.
    """

    game = "Terranigma"
    item_name_to_id = {name: data.ap_code for name, data in item_table.items()}
    location_name_to_id = get_location_names()
    options_dataclass = TerranigmaOptions
    options = TerranigmaOptions
    web = TerranigmaWeb()

    required_client_version = (0, 4, 4)
    
    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.locked_items = []
        self.victory_location = None

    def generate_early(self):
        starting_region = self.options.starting_region.value
        
        if starting_region != "crysta":
            region_items = {
                "lumina": "Surface Access",
                "louran": "Louran Access", 
                "loire": "Loire Access",
                "freedom": "Freedom Access"
            }
            
            if starting_region in region_items:
                self.multiworld.push_precollected(self.create_item(region_items[starting_region]))

        if self.options.key_item_placement.value == "early":
            for item in ["Giant Leaves", "Crystal Thread", "Ra Dewdrop"]:
                if item in item_table:
                    early_item = self.create_item(item)
                    self.locked_items.append(early_item)

    def create_regions(self):
        create_regions(self)

    def create_items(self):
        itempool = create_itempool(self)
        
        for locked_item in self.locked_items:
            if locked_item in itempool:
                itempool.remove(locked_item)
        
        self.multiworld.itempool += itempool

    def create_item(self, name: str) -> Item:
        return create_item(self, name)
    
    def set_rules(self):
        set_rules(self)
    
    def generate_output(self, output_directory: str) -> None:
        """Generate the ROM patch for this world"""
        try:
            # Create the patch using our basepatch
            patch = TerranigmaProcedurePatch(player=self.player, 
                                           player_name=self.multiworld.player_name[self.player])
            patch_rom(self, patch)
            
            # Write the patch file
            patch_path = os.path.join(output_directory,
                                    f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}")
            patch.write(patch_path)
            
        except Exception as e:
            raise Exception(f"Failed to generate Terranigma ROM patch: {e}")
    
    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {
            "options": {
                "starting_region":          self.options.starting_region.value,
                "key_item_placement":       self.options.key_item_placement.value,
                "equipment_scaling":        self.options.equipment_scaling.value,
                "shop_randomization":       self.options.shop_randomization.value,
                "magic_randomization":      self.options.magic_randomization.value,
                "boss_difficulty":          self.options.boss_difficulty.value,
                "trap_chance":              self.options.trap_chance.value,
                "speed_trap_weight":        self.options.speed_trap_weight.value,
                "damage_trap_weight":       self.options.damage_trap_weight.value,
                "confusion_trap_weight":    self.options.confusion_trap_weight.value
            },
            "seed": self.multiworld.seed_name,
            "slot": self.multiworld.player_name[self.player],
            "total_locations": get_total_locations(self)
        }

        return slot_data
    
    def collect(self, state: "CollectionState", item: "Item") -> bool:
        return super().collect(state, item)
    
    def remove(self, state: "CollectionState", item: "Item") -> bool:
        return super().remove(state, item)
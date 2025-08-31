# Terranigma client_data.py - Memory addresses and data structures
# Based on actual addresses from the Terranigma Randomizer project

from .Items import BASE_ID

# SNES Memory Layout
SRAM_START = 0x700000  # Base SRAM address
WRAM_START = 0x000000  # Work RAM base

# Game Save Data Locations (SRAM)
GAME_STATE_FLAGS = SRAM_START + 0x06C0  # Main game progression flags
CHEST_FLAGS_START = SRAM_START + 0x1000  # Chest open flags (bitfield)
PROGRESSION_FLAGS = SRAM_START + 0x1100  # Story progression flags
INVENTORY_START = SRAM_START + 0x0800   # Player inventory
EQUIPMENT_START = SRAM_START + 0x0900   # Equipped items
STATS_START = SRAM_START + 0x0A00       # Player stats (HP, ATK, etc.)

# Key Game State Addresses
ARK_HP = SRAM_START + 0x0692           # Ark's current HP (2 bytes)
ARK_MAX_HP = SRAM_START + 0x0694       # Ark's max HP (2 bytes)
ARK_LEVEL = SRAM_START + 0x0690        # Ark's level (1 byte)
ARK_EXP = SRAM_START + 0x0691          # Ark's experience (2 bytes)
ARK_GEMS = SRAM_START + 0x0694         # Current gems (3 bytes BCD)
ARK_X_POS = SRAM_START + 0x0210        # Ark's X position (2 bytes)
ARK_Y_POS = SRAM_START + 0x0212        # Ark's Y position (2 bytes)
CURRENT_MAP = SRAM_START + 0x0214      # Current map ID (2 bytes)

# Progression Flag Addresses (from ASM patches)
TOWER_FLAGS = SRAM_START + 0x06C4      # Tower access flags
GATE_FLAGS = SRAM_START + 0x0712       # Gate/barrier flags
CRYSTAL_THREAD_FLAG = SRAM_START + 0x06E3  # Crystal Thread obtained
SURFACE_ACCESS_FLAG = SRAM_START + 0x06C5  # Surface world access
GRECLIFF_FLAGS = SRAM_START + 0x0708   # Grecliff progression
LOURAN_FLAGS = SRAM_START + 0x0720     # Louran progression
LOIRE_FLAGS = SRAM_START + 0x0730      # Loire progression
FREEDOM_FLAGS = SRAM_START + 0x0740    # Freedom progression

# AP-specific Memory Locations (custom addresses in expanded SRAM)
AP_SLOT_DATA = SRAM_START + 0x2000         # AP options and settings
AP_RECEIVED_ITEMS = SRAM_START + 0x2100    # Counter of items received from AP
AP_SENT_LOCATIONS = SRAM_START + 0x2200    # Bitfield of locations sent to AP
AP_ITEM_QUEUE = SRAM_START + 0x2300        # Queue of items to give to player
AP_DEATH_LINK = SRAM_START + 0x2400        # Death link status
AP_CLIENT_STATE = SRAM_START + 0x2500      # Client connection state

# Chest Flag Mappings - Based on actual chest IDs from your KNOWN_CHESTS data
# These map chest IDs to their flag bit positions in SRAM
chest_id_to_flag = {
    # Tower of Babel chests (128-137)
    128: (CHEST_FLAGS_START + 0x10, 0x01),  # Tower floor 1
    129: (CHEST_FLAGS_START + 0x10, 0x02),  # Tower floor 2
    130: (CHEST_FLAGS_START + 0x10, 0x04),  # Tower floor 3
    131: (CHEST_FLAGS_START + 0x10, 0x08),  # Tower floor 4
    134: (CHEST_FLAGS_START + 0x10, 0x10),  # Tower floor 5
    135: (CHEST_FLAGS_START + 0x10, 0x20),  # Tower floor 6
    136: (CHEST_FLAGS_START + 0x10, 0x40),  # Tower floor 7
    137: (CHEST_FLAGS_START + 0x10, 0x80),  # Crystal Thread chest
    
    # Tree Cave chests (138-141, 154-156, 211-214, 236-237)
    138: (CHEST_FLAGS_START + 0x11, 0x01),
    139: (CHEST_FLAGS_START + 0x11, 0x02),
    140: (CHEST_FLAGS_START + 0x11, 0x04),  # Ra Tree inner
    141: (CHEST_FLAGS_START + 0x11, 0x08),  # Ra Tree inner
    154: (CHEST_FLAGS_START + 0x13, 0x01),
    155: (CHEST_FLAGS_START + 0x13, 0x02),
    156: (CHEST_FLAGS_START + 0x13, 0x04),
    211: (CHEST_FLAGS_START + 0x1A, 0x01),
    212: (CHEST_FLAGS_START + 0x1A, 0x02),
    213: (CHEST_FLAGS_START + 0x1A, 0x04),
    214: (CHEST_FLAGS_START + 0x1A, 0x08),
    236: (CHEST_FLAGS_START + 0x1D, 0x01),
    237: (CHEST_FLAGS_START + 0x1D, 0x02),
    
    # Grecliff Cave chest (142)
    142: (CHEST_FLAGS_START + 0x11, 0x10),  # RocSpear chest
    
    # Louran Area chests (143-146, 251)
    143: (CHEST_FLAGS_START + 0x11, 0x20),  # Meilins House
    144: (CHEST_FLAGS_START + 0x11, 0x40),  # M.Bulb chest
    145: (CHEST_FLAGS_START + 0x11, 0x80),  # Holy Seal chest
    146: (CHEST_FLAGS_START + 0x12, 0x01),  # LightRod chest
    251: (CHEST_FLAGS_START + 0x1F, 0x01),  # Zombie area chest
    
    # Sylvain Castle chests (147-149)
    147: (CHEST_FLAGS_START + 0x12, 0x02),  # Tower Key chest
    148: (CHEST_FLAGS_START + 0x12, 0x04),  # Icepick chest
    149: (CHEST_FLAGS_START + 0x12, 0x08),  # Ruby chest
    
    # Stockholm House - Portrait (150)
    150: (CHEST_FLAGS_START + 0x12, 0x10),  # Portrait chest
    
    # Continue mapping for other chests...
    # This would include all chest IDs from your KNOWN_CHESTS data
}

# Boss Flag Mappings - Based on story progression
boss_flags = {
    # Major bosses that give progression items
    0x01: BASE_ID + 1000,  # Ra Tree Boss
    0x02: BASE_ID + 1001,  # Shadow Keeper (Tower of Babel)
    0x04: BASE_ID + 1002,  # King of Birds (Sylvain)
    0x08: BASE_ID + 1003,  # Grecliff Boss
    0x10: BASE_ID + 1004,  # Bloody Mary (Louran)
    0x20: BASE_ID + 1005,  # Dragoon Castle Boss
    0x40: BASE_ID + 1006,  # Beruga (Lab)
    0x80: BASE_ID + 1007,  # Dark Gaia
}

# Event Flag Mappings - Story progression events
event_flags = {
    # Major story milestones
    0x0001: BASE_ID + 2000,  # Underworld Awakened
    0x0002: BASE_ID + 2001,  # Surface World Access
    0x0004: BASE_ID + 2002,  # Grecliff Boss Defeated
    0x0008: BASE_ID + 2003,  # Louran Flourished
    0x0010: BASE_ID + 2004,  # Loire Castle Accessed
    0x0020: BASE_ID + 2005,  # Dragoon Castle Opened
    0x0040: BASE_ID + 2006,  # Freedom Liberated
    0x0080: BASE_ID + 2007,  # Modern Era Reached
    0x0100: BASE_ID + 2008,  # Astarica Accessed
}

# Item ID Conversion Tables
# Maps Terranigma game item IDs to AP item IDs and vice versa
game_to_ap_item = {
    # Key progression items from ITEM_DATABASE
    0x0030: BASE_ID + 1,    # Crystal Thread
    0x0032: BASE_ID + 2,    # ElleCape
    0x0033: BASE_ID + 3,    # Sharp Claws
    0x0031: BASE_ID + 10,   # Giant Leaves
    0x0041: BASE_ID + 11,   # Ra Dewdrop
    0x0083: BASE_ID + 12,   # RocSpear
    0x0042: BASE_ID + 13,   # Snowgrass Leaf
    0x0034: BASE_ID + 20,   # Red Scarf
    0x0035: BASE_ID + 21,   # Holy Seal
    0x0036: BASE_ID + 23,   # Protect Bell
    0x0039: BASE_ID + 25,   # Ruby
    0x003A: BASE_ID + 26,   # Sapphire
    0x003C: BASE_ID + 27,   # Black Opal
    0x003D: BASE_ID + 28,   # Topaz
    0x003E: BASE_ID + 29,   # Tower Key
    0x007B: BASE_ID + 30,   # Speed Shoes
    0x007E: BASE_ID + 33,   # Air Herb
    0x004C: BASE_ID + 40,   # Starstone
    
    # Weapons (with WEAPON_FLAG)
    0x0080: BASE_ID + 0x100 + 0,   # HexRod
    0x0081: BASE_ID + 0x100 + 1,   # CrySpear
    0x0082: BASE_ID + 0x100 + 2,   # RaSpear
    0x0083: BASE_ID + 0x100 + 3,   # RocSpear (also progression)
    0x0084: BASE_ID + 0x100 + 4,   # Sticker
    0x0085: BASE_ID + 0x100 + 5,   # Neo Fang
    0x0086: BASE_ID + 0x100 + 6,   # Icepick
    
    # Consumables (with CONSUMABLE_FLAG)
    0x0011: BASE_ID + 0x300 + 0,   # M.Bulb
    0x0013: BASE_ID + 0x300 + 1,   # P. Cure
    0x0010: BASE_ID + 0x300 + 2,   # S.Bulb
    0x0014: BASE_ID + 0x300 + 3,   # Cure
    0x0015: BASE_ID + 0x300 + 4,   # Stardew
    0x0016: BASE_ID + 0x300 + 10,  # Serum
    0x0017: BASE_ID + 0x300 + 12,  # STR Potion
    0x0018: BASE_ID + 0x300 + 13,  # DEF Potion
    0x0019: BASE_ID + 0x300 + 14,  # Luck Potion
    0x001A: BASE_ID + 0x300 + 15,  # Life Potion
    
    # Gems (with GEM_FLAG)
    0x8030: BASE_ID + 0x400 + 0,   # 30 Gems
    0x8050: BASE_ID + 0x400 + 1,   # 50 Gems
    0x8100: BASE_ID + 0x400 + 2,   # 100 Gems
    0x8200: BASE_ID + 0x400 + 10,  # 200 Gems
    0x8300: BASE_ID + 0x400 + 11,  # 300 Gems
    0x8500: BASE_ID + 0x400 + 12,  # 500 Gems
}

# Reverse mapping for AP to game items
ap_to_game_item = {v: k for k, v in game_to_ap_item.items()}

# Special Location IDs - locations that require special handling
special_locations = {
    "Dark Gaia Defeated": BASE_ID + 10000,    # Victory location
    "Portrait Obtained": BASE_ID + 10001,     # Special handling needed
}

# Death link configuration
DEATH_LINK_ENABLED = AP_DEATH_LINK
ARK_DEATH_STATE = SRAM_START + 0x2401      # 0 = alive, 1 = dead
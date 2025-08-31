import os
import pkgutil
import Utils
import hashlib
import settings
from worlds.Files import APAutoPatchInterface, APTokenMixin, APTokenTypes
from typing import Iterable, TYPE_CHECKING, Optional
from struct import pack

if TYPE_CHECKING:
    from . import TerranigmaWorld

# You need to replace this with your actual ROM hash
# Get it with: Get-FileHash "path_to_your_rom.sfc" -Algorithm MD5
TERRANIGMA_HASH = "your_actual_rom_hash_here"  # Replace with actual MD5 hash

# AP-specific ROM addresses for integration (matching ASM)
AP_SLOT_DATA = 0x001000          # Matches ASM !AP_SLOT_DATA
AP_ITEM_QUEUE = 0x001400         # Matches ASM !AP_ITEM_QUEUE  
AP_LOCATION_FLAGS = 0x001200     # Matches ASM !AP_SENT_LOCATIONS
AP_ROM_NAME = 0x001700           # Matches ASM !AP_ROM_NAME

class TerranigmaProcedurePatch(APAutoPatchInterface, APTokenMixin):
    hash = [TERRANIGMA_HASH]
    game = "Terranigma" 
    patch_file_ending = ".apterranigma"
    result_file_ending = ".sfc"
    name: bytearray

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def patch(self, target: str) -> None:
        """Apply the basepatch and tokens to create the final ROM"""
        # Get the basepatch data
        basepatch_data = pkgutil.get_data(__name__, os.path.join("data", "terranigma_basepatch.bsdiff4"))
        if not basepatch_data:
            raise Exception("Could not find terranigma_basepatch.bsdiff4")
        
        # Apply bsdiff4 patch
        import bsdiff4
        source_data = self.get_source_data()
        patched_data = bytearray(bsdiff4.patch(source_data, basepatch_data))
        
        # Apply token patches (additional modifications)
        self.apply_tokens(patched_data)
        
        # Write final ROM
        with open(target, 'wb') as f:
            f.write(patched_data)

    def write_byte(self, offset: int, value: int):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset: int, value: Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))

    def write_int32(self, offset: int, value: int):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(4, "little"))

def patch_rom(world: "TerranigmaWorld", patch: TerranigmaProcedurePatch):
    """Apply all patches needed for Terranigma AP integration"""
    
    # APAutoPatchInterface handles the basepatch automatically
    # We just need to write our additional data
    
    # Write player options to ROM (at addresses matching ASM)
    write_options_to_rom(world, patch)
    
    # Generate unique ROM name for client identification
    patch_name = bytearray(
        f'TER{Utils.__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0', 'utf8')[:32]
    patch_name.extend([0] * (32 - len(patch_name)))
    patch.name = bytes(patch_name)
    
    # Write to both SNES header location and AP ROM name location
    patch.write_bytes(0x7FC0, patch.name[:21])  # SNES ROM title (21 bytes max)
    patch.write_bytes(AP_ROM_NAME, patch.name)  # AP client identifier (32 bytes)

def write_options_to_rom(world: "TerranigmaWorld", patch: TerranigmaProcedurePatch):
    """Write player options to ROM at addresses matching the ASM"""
    
    # Write options to AP_SLOT_DATA (matches !AP_SLOT_DATA in ASM)
    patch.write_byte(AP_SLOT_DATA, world.options.starting_region.value)
    patch.write_byte(AP_SLOT_DATA + 1, world.options.key_item_placement.value)
    patch.write_byte(AP_SLOT_DATA + 2, int(world.options.equipment_scaling.value))
    patch.write_byte(AP_SLOT_DATA + 3, int(world.options.shop_randomization.value))
    patch.write_byte(AP_SLOT_DATA + 4, int(world.options.magic_randomization.value))
    patch.write_byte(AP_SLOT_DATA + 5, world.options.boss_difficulty.value)
    patch.write_byte(AP_SLOT_DATA + 6, world.options.trap_chance.value)
    patch.write_byte(AP_SLOT_DATA + 7, world.options.speed_trap_weight.value)
    patch.write_byte(AP_SLOT_DATA + 8, world.options.damage_trap_weight.value)
    patch.write_byte(AP_SLOT_DATA + 9, world.options.confusion_trap_weight.value)
    
    # Death link option (if available)
    if hasattr(world.options, 'death_link'):
        patch.write_byte(AP_SLOT_DATA + 10, int(world.options.death_link.value))
    
    # Write slot data for client
    patch.write_int32(AP_SLOT_DATA + 20, len([loc for loc in world.multiworld.get_locations(world.player) 
                                             if not loc.event and not loc.locked]))
    patch.write_int32(AP_SLOT_DATA + 24, world.player)

def get_base_rom_bytes() -> bytes:
    """Get the base Terranigma ROM data"""
    rom_file: str = get_base_rom_path()
    base_rom_bytes: Optional[bytes] = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    
    if not base_rom_bytes:
        base_rom_bytes = bytes(Utils.read_snes_rom(open(rom_file, "rb")))

        # Validate ROM hash
        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {TERRANIGMA_HASH}:
            raise Exception(f"Supplied Base Rom does not match known MD5 for Terranigma. "
                          f"Expected: {TERRANIGMA_HASH}, Got: {basemd5.hexdigest()}")
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes

def get_base_rom_path(file_name: str = "") -> str:
    """Get the path to the base Terranigma ROM"""
    options: settings.Settings = settings.get_settings()
    if not file_name:
        file_name = options.get("terranigma_options", {}).get("rom_file", "")
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
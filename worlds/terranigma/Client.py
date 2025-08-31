import logging
import time
import typing
from NetUtils import ClientStatus, color, NetworkItem
from worlds.AutoSNIClient import SNIClient
from typing import TYPE_CHECKING
from .Items import BASE_ID, item_table
from .client_data import (
    # Game state addresses
    ARK_HP, ARK_MAX_HP, ARK_LEVEL, CURRENT_MAP, GAME_STATE_FLAGS,
    
    # AP-specific addresses
    AP_RECEIVED_ITEMS, AP_SENT_LOCATIONS, AP_ITEM_QUEUE, AP_DEATH_LINK, AP_CLIENT_STATE,
    
    # Flag mappings
    chest_id_to_flag, boss_flags, event_flags, game_to_ap_item, ap_to_game_item,
    
    # Special locations
    special_locations, DEATH_LINK_ENABLED, ARK_DEATH_STATE
)

if TYPE_CHECKING:
    from SNIClient import SNIContext

snes_logger = logging.getLogger("SNES")

# FXPAK Pro protocol memory mapping used by SNI
# Terranigma uses LoROM mapping
ROM_START = 0x000000
SRAM_START = 0x700000

class TerranigmaSNIClient(SNIClient):
    game = "Terranigma"
    patch_suffix = ".apterranigma"
    
    item_queue: typing.List[NetworkItem] = []
    death_link_enabled = False

    async def deathlink_kill_player(self, ctx: "SNIContext") -> None:
        """Kill the player for death link"""
        from SNIClient import DeathState, snes_buffered_write, snes_read, snes_flush_writes
        
        # Check if we're in a state where we can kill the player
        current_hp = int.from_bytes(await snes_read(ctx, ARK_HP, 2), "little")
        if current_hp > 0:
            # Set HP to 0 to kill Ark
            snes_buffered_write(ctx, ARK_HP, int.to_bytes(0, 2, "little"))
            snes_buffered_write(ctx, ARK_DEATH_STATE, int.to_bytes(1, 1, "little"))
            await snes_flush_writes(ctx)
            ctx.death_state = DeathState.dead
            ctx.last_death_link = time.time()

    async def validate_rom(self, ctx: "SNIContext") -> bool:
        """Validate that this is a compatible Terranigma ROM"""
        from SNIClient import snes_read
        
        # Read ROM name from standard SNES header location
        rom_name = await snes_read(ctx, 0x7FC0, 0x15)
        if rom_name is None or rom_name == bytes([0] * 0x15):
            return False
        
        # Check if it's a Terranigma AP ROM (starts with "TER")
        if rom_name[:3] != b"TER":
            return False

        ctx.game = self.game
        ctx.rom = rom_name
        ctx.items_handling = 0b111  # full remote
        ctx.allow_collect = True

        # Check death link setting
        death_link = await snes_read(ctx, DEATH_LINK_ENABLED, 1)
        if death_link:
            self.death_link_enabled = bool(death_link[0] & 0b1)
            await ctx.update_death_link(self.death_link_enabled)
        
        return True

    async def pop_item(self, ctx: "SNIContext"):
        """Give queued items to the player"""
        from SNIClient import snes_read, snes_buffered_write
        
        if not self.item_queue:
            return
            
        # Check if we can give items (not in cutscene, menu, etc.)
        game_state = int.from_bytes(await snes_read(ctx, GAME_STATE_FLAGS, 1), "little")
        
        # Only give items during normal gameplay (adjust conditions as needed)
        if game_state & 0x80:  # In cutscene or menu
            return
            
        item = self.item_queue.pop(0)
        
        # Convert AP item to game item
        if item.item in ap_to_game_item:
            game_item_id = ap_to_game_item[item.item]
            
            # Add item to player inventory
            # This would need to be implemented based on Terranigma's inventory system
            await self.add_item_to_inventory(ctx, game_item_id)
            
            # Play item received sound effect
            snes_buffered_write(ctx, GAME_STATE_FLAGS + 10, int.to_bytes(0x01, 1, "little"))
        
        # Handle special items
        elif item.item & 0x500 == 0x500:  # Trap items
            await self.activate_trap(ctx, item.item)

    async def add_item_to_inventory(self, ctx: "SNIContext", game_item_id: int):
        """Add an item to the player's inventory"""
        from SNIClient import snes_read, snes_buffered_write
        
        # This is a simplified version - would need proper inventory management
        # based on Terranigma's inventory system
        
        # For now, just set a flag that an item was received
        items_received = int.from_bytes(await snes_read(ctx, AP_RECEIVED_ITEMS, 2), "little")
        items_received += 1
        snes_buffered_write(ctx, AP_RECEIVED_ITEMS, items_received.to_bytes(2, "little"))

    async def activate_trap(self, ctx: "SNIContext", trap_id: int):
        """Activate a trap effect"""
        from SNIClient import snes_buffered_write
        
        trap_type = trap_id & 0xFF
        
        if trap_type == 0:  # Speed Trap
            # Reduce movement speed temporarily
            snes_buffered_write(ctx, GAME_STATE_FLAGS + 20, int.to_bytes(0x01, 1, "little"))
        elif trap_type == 1:  # Damage Trap
            # Reduce attack power temporarily  
            snes_buffered_write(ctx, GAME_STATE_FLAGS + 21, int.to_bytes(0x01, 1, "little"))
        elif trap_type == 2:  # Confusion Trap
            # Reverse controls temporarily
            snes_buffered_write(ctx, GAME_STATE_FLAGS + 22, int.to_bytes(0x01, 1, "little"))

    async def game_watcher(self, ctx: "SNIContext") -> None:
        """Main game watching loop"""
        from SNIClient import snes_read, snes_buffered_write, snes_flush_writes, DeathState

        # Check if we're connected and the ROM is valid
        game_state = int.from_bytes(await snes_read(ctx, GAME_STATE_FLAGS, 1), "little")
        if not game_state:
            return

        # Handle death link
        if self.death_link_enabled:
            current_hp = int.from_bytes(await snes_read(ctx, ARK_HP, 2), "little")
            if current_hp == 0 and ctx.death_state == DeathState.alive and ctx.last_death_link + 1 < time.time():
                await ctx.handle_deathlink_state(True, f"Ark died in the world of {ctx.player_names[ctx.slot]}.")
            elif current_hp > 0:
                ctx.death_state = DeathState.alive

        # Handle received items
        recv_count = int.from_bytes(await snes_read(ctx, AP_RECEIVED_ITEMS, 2), "little")
        if recv_count < len(ctx.items_received):
            item = ctx.items_received[recv_count]
            recv_count += 1
            
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), 
                recv_count, len(ctx.items_received)))
            
            snes_buffered_write(ctx, AP_RECEIVED_ITEMS, recv_count.to_bytes(2, "little"))
            
            # Add item to queue for processing
            self.item_queue.append(item)

        # Process item queue
        await self.pop_item(ctx)

        # Check for new locations (chests opened, bosses defeated, etc.)
        new_checks = []

        # Check chest flags
        for chest_id, (flag_addr, flag_bit) in chest_id_to_flag.items():
            chest_flags = int.from_bytes(await snes_read(ctx, flag_addr, 1), "little")
            location_id = BASE_ID + chest_id
            
            if (chest_flags & flag_bit) and location_id not in ctx.checked_locations:
                new_checks.append(location_id)

        # Check boss flags
        boss_flag_data = int.from_bytes(await snes_read(ctx, GAME_STATE_FLAGS + 50, 4), "little")
        for flag, location_id in boss_flags.items():
            if (boss_flag_data & flag) and location_id not in ctx.checked_locations:
                new_checks.append(location_id)

        # Check event flags
        event_flag_data = int.from_bytes(await snes_read(ctx, GAME_STATE_FLAGS + 60, 4), "little")
        for flag, location_id in event_flags.items():
            if (event_flag_data & flag) and location_id not in ctx.checked_locations:
                new_checks.append(location_id)

        # Check victory condition
        victory_flag = int.from_bytes(await snes_read(ctx, GAME_STATE_FLAGS + 100, 1), "little")
        if victory_flag & 0x80:  # Dark Gaia defeated
            if special_locations["Dark Gaia Defeated"] not in ctx.checked_locations:
                new_checks.append(special_locations["Dark Gaia Defeated"])
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True

        # Send all new checks to the server
        if new_checks:
            await ctx.check_locations(new_checks)
            for new_check_id in new_checks:
                ctx.locations_checked.add(new_check_id)
                location = ctx.location_names.lookup_in_game(new_check_id)
                snes_logger.info(
                    f'New Check: {location} ({len(ctx.locations_checked)}/'
                    f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')

        await snes_flush_writes(ctx)
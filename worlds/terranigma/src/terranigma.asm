; Terranigma Archipelago Basepatch
; Based on actual ROM analysis and memory addresses

hirom

; WRAM addresses (System Bus format - no 7E prefix needed in code)
!ARK_LEVEL = $000656
!ARK_CURRENT_HP = $00065D
!ARK_XP_START = $000690          ; 3 bytes BCD format
!ARK_MONEY_START = $000694       ; 3 bytes BCD format
!ARK_MAGIROCKS = $0007EC         ; 3 bytes BCD format
!EVENT_FLAGS_START = $0006C4     ; Event flags 06C4-073F
!INVENTORY_ACCESS = $0006DF      ; bit 40 = inventory access, bit 80 = magic in bosses
!TOWER_ACCESS = $0006E0          ; Set to AA to open all towers

; Chest system addresses
!CHEST_ITEM_STORAGE = $8109C7    ; Where chest item ID gets stored
!CHEST_FLAG_STORAGE = $8109C9    ; Where chest_id + 8500 gets stored
!CHEST_ROM_TABLE = $99D859       ; Base ROM address for chest data

; AP-specific memory locations (using unused WRAM space)
!AP_SLOT_DATA = $001000          ; AP options and settings
!AP_RECEIVED_ITEMS = $001100     ; 2-byte counter of items received from AP
!AP_SENT_LOCATIONS = $001200     ; Bitfield of sent locations (256 bytes)
!AP_ITEM_QUEUE = $001400         ; Queue of items to give player
!AP_DEATH_LINK = $001500         ; Death link status
!AP_CLIENT_STATE = $001600       ; Client connection state
!AP_ROM_NAME = $001700           ; AP ROM identifier (32 bytes)

; Hook the main chest opening routine - THE critical intercept point
org $87939E
hook_chest_open:
    JSL handle_ap_chest_open
    LDA $99D85C,X               ; Original: load item ID from ROM

; Hook the intro sequence for initialization
org $90886F
hook_intro:
    JML ap_initialization
    NOP #6

; Custom code space - Bank FE is completely unused
org $FE0000

ap_initialization:
    ; Do the original intro skip AND AP initialization
    SEP #$20
    
    ; Set up all the intro skip flags (from PixelShake's patch)
    LDA #$CF
    ORA $06C4
    STA $06C4                   ; flags 0020, 0021, 0022, 0023, 0026, 0027
    
    LDA #$43                    ; Changed to 43 for post-Crystal Thread state
    ORA $06C5
    STA $06C5                   ; flags 0028, 002E
    
    LDA #$10
    ORA $06C7
    STA $06C7                   ; flag 003C
    
    LDA #$40
    ORA $06DF
    STA $06DF                   ; flag 00FE (inventory access)
    
    LDA #$1F
    ORA $0708
    STA $0708                   ; flags 0240, 0241, 0242, 0243, 0244
    
    LDA #$5F                    ; Open the gate
    ORA $0712
    STA $0712                   ; flags 0290, 0291, 0292, 0293, 0294
    
    LDA #$0F
    STA $0710                   ; Open Tower 1 doors
    
    ; Set starting inventory
    REP #$20
    LDA #$017A
    STA $7F8036                 ; 1x Jewel Box
    LDA #$0181
    STA $7F8048                 ; 1x CrySpear
    LDA #$01A0
    STA $7F8068                 ; 1x Clothes
    
    ; Initialize AP memory
    JSL init_ap_memory
    
    ; Warp outside Crysta
    COP #$14                    ; warp command
    dw $0003                    ; map
    db $00                      ; layer
    db $55                      ; entrance
    dw $0210                    ; X pos
    dw $0210                    ; Y pos
    JML $908879                 ; Return to game

handle_ap_chest_open:
    PHA                         ; Save A register
    PHX                         ; Save X register  
    PHY                         ; Save Y register
    
    ; Get the chest ID from ROM
    LDA $99D85E,X              ; Load chest ID from ROM data
    TAY                        ; Store chest_id in Y
    
    ; Calculate AP location ID: chest_id + 8500 (matching game's system)
    CLC
    ADC #$8500
    STA !CHEST_FLAG_STORAGE     ; Store for flag system
    
    ; Check if this is an AP-managed location
    TYA                        ; chest_id back to A
    JSL check_ap_location
    BCC .use_original_item     ; If not AP location, use original item
    
    ; This IS an AP location - send location check
    TYA                        ; chest_id to A
    JSL send_location_check
    
    ; Get replacement item from AP
    JSL get_ap_item
    BRA .store_item
    
.use_original_item:
    ; Use original item from ROM
    LDA $99D85C,X              ; Original item ID from ROM
    
.store_item:
    ; Store the item (either original or AP replacement)
    STA !CHEST_ITEM_STORAGE     ; Store at $8109C7
    
    PLY                        ; Restore Y register
    PLX                        ; Restore X register
    PLA                        ; Restore A register
    RTL

send_location_check:
    PHA
    PHX
    PHY
    
    TAX                        ; chest_id to X
    
    ; Calculate byte offset and bit position for bitfield
    ; Byte offset = chest_id / 8
    TXA
    LSR A                      ; /2
    LSR A                      ; /4  
    LSR A                      ; /8
    CLC
    ADC #!AP_SENT_LOCATIONS    ; Add base address
    STA $00                    ; Store address in zero page
    
    ; Bit position = chest_id % 8
    TXA
    AND #$0007                 ; A = chest_id % 8
    TAX                        ; bit_position to X
    
    ; Create bit mask (1 << bit_position)
    LDA #$0001
.shift_loop:
    CPX #$0000
    BEQ .apply_mask
    ASL A                      ; Shift left
    DEX
    BRA .shift_loop
    
.apply_mask:
    ; Set the bit using indirect addressing
    ORA ($00)
    STA ($00)
    
    PLY
    PLX
    PLA
    RTL

check_ap_location:
    ; For now, ALL chests are AP locations
    SEC                        ; Set carry (is AP location)
    RTL

get_ap_item:
    ; Get the AP replacement item for this location
    ; TODO: Implement actual AP item lookup
    LDA #$0010                 ; Small Bulb as placeholder
    RTL

init_ap_memory:
    PHA
    PHX
    PHY
    
    ; Clear AP memory space
    LDX #$0000
    LDA #$0000
.clear_loop:
    STA !AP_SLOT_DATA,X
    INX
    INX
    CPX #$0800                 ; Clear 2048 bytes of AP data  
    BCC .clear_loop
    
    ; Set ROM identifier for AP client recognition
    LDX #$0000
.name_loop:
    LDA.l ap_rom_name,X
    STA !AP_ROM_NAME,X
    INX
    CPX #$0020                 ; 32 bytes
    BCC .name_loop
    
    PLY
    PLX
    PLA
    RTL

ap_rom_name:
    db "TERRANIGMA_AP_BASEPATCH_V1.0", $00, $00
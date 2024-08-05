#!/usr/bin/env python3

import sys
import os
import re
import binascii


### globals

outputfilename = 'newbag.sav'
version = "0.7.0"
money_offset = 0x0490
coins_offset = 0x0494
soot_sack_steps_offset = 0x04AC
team_size_offset = 0x0234
pokedex_owned_offset = 0x0028
pokedex_seen_offset = 0x005C
game_code = -1
pokeball = '◓'

RUBY_SAPPHIRE = 0
FIRERED_LEAFGREEN = 1
EMERALD = 2

max_q = {
	'PC_ITEMS' : 50,
	'ITEMS' : 30,
	'KEY_ITEMS' : 30,
	'POKE_BALLS' : 16,
	'TM_HM' : 64,
	'BERRIES' : 46,
}

offset = {
	'PC_ITEMS' : 0x0498,
	'ITEMS' : 0x0560,
	'KEY_ITEMS' : 0x05D8,
	'POKE_BALLS' : 0x0650,
	'TM_HM' : 0x0690,
	'BERRIES' : 0x0790,
}

eng_letter = {}
eng_index = {
	0x80: ' ',
	0xa1: '0',
	0xa2: '1',
	0xa3: '2',
	0xa4: '3',
	0xa5: '4',
	0xa6: '5',
	0xa7: '6',
	0xa8: '7',
	0xa9: '8',
	0xaa: '9',
	0xab: '!',
	0xac: '?',
	0xad: '.',
	0xae: '-',
	0xB0: '_', # ellipsis
	0xB1: '"',
	0xB2: '"',
	0xB3: "'",
	0xB4: "'",
	0xB5: '^', # male symbol
	0xB6: '+', # female symbol
	0xB8: ',',
	0xBA: '/',
	0xbb: 'A',
	0xbc: 'B',
	0xbd: 'C',
	0xbe: 'D',
	0xbf: 'E',
	0xc0: 'F',
	0xc1: 'G',
	0xc2: 'H',
	0xc3: 'I',
	0xc4: 'J',
	0xc5: 'K',
	0xc6: 'L',
	0xc7: 'M',
	0xc8: 'N',
	0xc9: 'O',
	0xca: 'P',
	0xcb: 'Q',
	0xcc: 'R',
	0xcd: 'S',
	0xce: 'T',
	0xcf: 'U',
	0xd0: 'V',
	0xd1: 'W',
	0xd2: 'X',
	0xd3: 'Y',
	0xd4: 'Z',
	0xd5: 'a',
	0xd6: 'b',
	0xd7: 'c',
	0xd8: 'd',
	0xd9: 'e',
	0xda: 'f',
	0xdb: 'g',
	0xdc: 'h',
	0xdd: 'i',
	0xde: 'j',
	0xdf: 'k',
	0xe0: 'l',
	0xe1: 'm',
	0xe2: 'n',
	0xe3: 'o',
	0xe4: 'p',
	0xe5: 'q',
	0xe6: 'r',
	0xe7: 's',
	0xe8: 't',
	0xe9: 'u',
	0xea: 'v',
	0xeb: 'w',
	0xec: 'x',
	0xed: 'y',
	0xee: 'z',
}




### big dicts

items_index = {0: 'NONE', 1: 'MASTER_BALL', 2: 'ULTRA_BALL', 3: 'GREAT_BALL', 4: 'POKE_BALL', 5: 'SAFARI_BALL', 6: 'NET_BALL', 7: 'DIVE_BALL', 8: 'NEST_BALL', 9: 'REPEAT_BALL', 10: 'TIMER_BALL', 11: 'LUXURY_BALL', 12: 'PREMIER_BALL', 13: 'POTION', 14: 'ANTIDOTE', 15: 'BURN_HEAL', 16: 'ICE_HEAL', 17: 'AWAKENING', 18: 'PARALYZE_HEAL', 19: 'FULL_RESTORE', 20: 'MAX_POTION', 21: 'HYPER_POTION', 22: 'SUPER_POTION', 23: 'FULL_HEAL', 24: 'REVIVE', 25: 'MAX_REVIVE', 26: 'FRESH_WATER', 27: 'SODA_POP', 28: 'LEMONADE', 29: 'MOOMOO_MILK', 30: 'ENERGY_POWDER', 31: 'ENERGY_ROOT', 32: 'HEAL_POWDER', 33: 'REVIVAL_HERB', 34: 'ETHER', 35: 'MAX_ETHER', 36: 'ELIXIR', 37: 'MAX_ELIXIR', 38: 'LAVA_COOKIE', 39: 'BLUE_FLUTE', 40: 'YELLOW_FLUTE', 41: 'RED_FLUTE', 42: 'BLACK_FLUTE', 43: 'WHITE_FLUTE', 44: 'BERRY_JUICE', 45: 'SACRED_ASH', 46: 'SHOAL_SALT', 47: 'SHOAL_SHELL', 48: 'RED_SHARD', 49: 'BLUE_SHARD', 50: 'YELLOW_SHARD', 51: 'GREEN_SHARD', 52: '034', 53: '035', 54: '036', 55: '037', 56: '038', 57: '039', 58: '03A', 59: '03B', 60: '03C', 61: '03D', 62: '03E', 63: 'HP_UP', 64: 'PROTEIN', 65: 'IRON', 66: 'CARBOS', 67: 'CALCIUM', 68: 'RARE_CANDY', 69: 'PP_UP', 70: 'ZINC', 71: 'PP_MAX', 72: '048', 73: 'GUARD_SPEC', 74: 'DIRE_HIT', 75: 'X_ATTACK', 76: 'X_DEFEND', 77: 'X_SPEED', 78: 'X_ACCURACY', 79: 'X_SPECIAL', 80: 'POKE_DOLL', 81: 'FLUFFY_TAIL', 82: '052', 83: 'SUPER_REPEL', 84: 'MAX_REPEL', 85: 'ESCAPE_ROPE', 86: 'REPEL', 87: '057', 88: '058', 89: '059', 90: '05A', 91: '05B', 92: '05C', 93: 'SUN_STONE', 94: 'MOON_STONE', 95: 'FIRE_STONE', 96: 'THUNDER_STONE', 97: 'WATER_STONE', 98: 'LEAF_STONE', 99: '063', 100: '064', 101: '065', 102: '066', 103: 'TINY_MUSHROOM', 104: 'BIG_MUSHROOM', 105: '069', 106: 'PEARL', 107: 'BIG_PEARL', 108: 'STARDUST', 109: 'STAR_PIECE', 110: 'NUGGET', 111: 'HEART_SCALE', 112: '070', 113: '071', 114: '072', 115: '073', 116: '074', 117: '075', 118: '076', 119: '077', 120: '078', 121: 'ORANGE_MAIL', 122: 'HARBOR_MAIL', 123: 'GLITTER_MAIL', 124: 'MECH_MAIL', 125: 'WOOD_MAIL', 126: 'WAVE_MAIL', 127: 'BEAD_MAIL', 128: 'SHADOW_MAIL', 129: 'TROPIC_MAIL', 130: 'DREAM_MAIL', 131: 'FAB_MAIL', 132: 'RETRO_MAIL', 133: 'CHERI_BERRY', 134: 'CHESTO_BERRY', 135: 'PECHA_BERRY', 136: 'RAWST_BERRY', 137: 'ASPEAR_BERRY', 138: 'LEPPA_BERRY', 139: 'ORAN_BERRY', 140: 'PERSIM_BERRY', 141: 'LUM_BERRY', 142: 'SITRUS_BERRY', 143: 'FIGY_BERRY', 144: 'WIKI_BERRY', 145: 'MAGO_BERRY', 146: 'AGUAV_BERRY', 147: 'IAPAPA_BERRY', 148: 'RAZZ_BERRY', 149: 'BLUK_BERRY', 150: 'NANAB_BERRY', 151: 'WEPEAR_BERRY', 152: 'PINAP_BERRY', 153: 'POMEG_BERRY', 154: 'KELPSY_BERRY', 155: 'QUALOT_BERRY', 156: 'HONDEW_BERRY', 157: 'GREPA_BERRY', 158: 'TAMATO_BERRY', 159: 'CORNN_BERRY', 160: 'MAGOST_BERRY', 161: 'RABUTA_BERRY', 162: 'NOMEL_BERRY', 163: 'SPELON_BERRY', 164: 'PAMTRE_BERRY', 165: 'WATMEL_BERRY', 166: 'DURIN_BERRY', 167: 'BELUE_BERRY', 168: 'LIECHI_BERRY', 169: 'GANLON_BERRY', 170: 'SALAC_BERRY', 171: 'PETAYA_BERRY', 172: 'APICOT_BERRY', 173: 'LANSAT_BERRY', 174: 'STARF_BERRY', 175: 'ENIGMA_BERRY', 176: 'UNUSED_BERRY_1', 177: 'UNUSED_BERRY_2', 178: 'UNUSED_BERRY_3', 179: 'BRIGHT_POWDER', 180: 'WHITE_HERB', 181: 'MACHO_BRACE', 182: 'EXP_SHARE', 183: 'QUICK_CLAW', 184: 'SOOTHE_BELL', 185: 'MENTAL_HERB', 186: 'CHOICE_BAND', 187: 'KINGS_ROCK', 188: 'SILVER_POWDER', 189: 'AMULET_COIN', 190: 'CLEANSE_TAG', 191: 'SOUL_DEW', 192: 'DEEP_SEA_TOOTH', 193: 'DEEP_SEA_SCALE', 194: 'SMOKE_BALL', 195: 'EVERSTONE', 196: 'FOCUS_BAND', 197: 'LUCKY_EGG', 198: 'SCOPE_LENS', 199: 'METAL_COAT', 200: 'LEFTOVERS', 201: 'DRAGON_SCALE', 202: 'LIGHT_BALL', 203: 'SOFT_SAND', 204: 'HARD_STONE', 205: 'MIRACLE_SEED', 206: 'BLACK_GLASSES', 207: 'BLACK_BELT', 208: 'MAGNET', 209: 'MYSTIC_WATER', 210: 'SHARP_BEAK', 211: 'POISON_BARB', 212: 'NEVER_MELT_ICE', 213: 'SPELL_TAG', 214: 'TWISTED_SPOON', 215: 'CHARCOAL', 216: 'DRAGON_FANG', 217: 'SILK_SCARF', 218: 'UP_GRADE', 219: 'SHELL_BELL', 220: 'SEA_INCENSE', 221: 'LAX_INCENSE', 222: 'LUCKY_PUNCH', 223: 'METAL_POWDER', 224: 'THICK_CLUB', 225: 'STICK', 226: '0E2', 227: '0E3', 228: '0E4', 229: '0E5', 230: '0E6', 231: '0E7', 232: '0E8', 233: '0E9', 234: '0EA', 235: '0EB', 236: '0EC', 237: '0ED', 238: '0EE', 239: '0EF', 240: '0F0', 241: '0F1', 242: '0F2', 243: '0F3', 244: '0F4', 245: '0F5', 246: '0F6', 247: '0F7', 248: '0F8', 249: '0F9', 250: '0FA', 251: '0FB', 252: '0FC', 253: '0FD', 254: 'RED_SCARF', 255: 'BLUE_SCARF', 256: 'PINK_SCARF', 257: 'GREEN_SCARF', 258: 'YELLOW_SCARF', 259: 'MACH_BIKE', 260: 'COIN_CASE', 261: 'ITEMFINDER', 262: 'OLD_ROD', 263: 'GOOD_ROD', 264: 'SUPER_ROD', 265: 'SS_TICKET', 266: 'CONTEST_PASS', 267: '10B', 268: 'WAILMER_PAIL', 269: 'DEVON_GOODS', 270: 'SOOT_SACK', 271: 'BASEMENT_KEY', 272: 'ACRO_BIKE', 273: 'POKEBLOCK_CASE', 274: 'LETTER', 275: 'EON_TICKET', 276: 'RED_ORB', 277: 'BLUE_ORB', 278: 'SCANNER', 279: 'GO_GOGGLES', 280: 'METEORITE', 281: 'ROOM_1_KEY', 282: 'ROOM_2_KEY', 283: 'ROOM_4_KEY', 284: 'ROOM_6_KEY', 285: 'STORAGE_KEY', 286: 'ROOT_FOSSIL', 287: 'CLAW_FOSSIL', 288: 'DEVON_SCOPE', 289: 'TM01 Focus Punch', 290: 'TM02 Dragon Claw', 291: 'TM03 Water Pulse', 292: 'TM04 Calm Mind', 293: 'TM05 Roar', 294: 'TM06 Toxic', 295: 'TM07 Hail', 296: 'TM08 Bulk Up', 297: 'TM09 Bullet Seed', 298: 'TM10 Hidden Power', 299: 'TM11 Sunny Day', 300: 'TM12 Taunt', 301: 'TM13 Ice Beam', 302: 'TM14 Blizzard', 303: 'TM15 Hyper Beam', 304: 'TM16 Light Screen', 305: 'TM17 Protect', 306: 'TM18 Rain Dance', 307: 'TM19 Giga Drain', 308: 'TM20 Safeguard', 309: 'TM21 Frustration', 310: 'TM22 Solarbeam', 311: 'TM23 Iron Tail', 312: 'TM24 Thunderbolt', 313: 'TM25 Thunder', 314: 'TM26 Earthquake', 315: 'TM27 Return', 316: 'TM28 Dig', 317: 'TM29 Psychic', 318: 'TM30 Shadow Ball', 319: 'TM31 Brick Break', 320: 'TM32 Double Team', 321: 'TM33 Reflect', 322: 'TM34 Shock Wave', 323: 'TM35 Flamethrower', 324: 'TM36 Sludge Bomb', 325: 'TM37 Sandstorm', 326: 'TM38 Fire Blast', 327: 'TM39 Rock Tomb', 328: 'TM40 Aerial Ace', 329: 'TM41 Torment', 330: 'TM42 Facade', 331: 'TM43 Secret Power', 332: 'TM44 Rest', 333: 'TM45 Attract', 334: 'TM46 Thief', 335: 'TM47 Steel Wing', 336: 'TM48 Skill Swap', 337: 'TM49 Snatch', 338: 'TM50 Overheat', 339: 'HM01 Cut', 340: 'HM02 Fly', 341: 'HM03 Surf', 342: 'HM04 Strength', 343: 'HM05 Flash', 344: 'HM06 Rock Smash', 345: 'HM07 Waterfall', 346: 'HM08 Dive', 347: '15B', 348: '15C', 349: 'OAKS_PARCEL', 350: 'POKE_FLUTE', 351: 'SECRET_KEY', 352: 'BIKE_VOUCHER', 353: 'GOLD_TEETH', 354: 'OLD_AMBER', 355: 'CARD_KEY', 356: 'LIFT_KEY', 357: 'HELIX_FOSSIL', 358: 'DOME_FOSSIL', 359: 'SILPH_SCOPE', 360: 'BICYCLE', 361: 'TOWN_MAP', 362: 'VS_SEEKER', 363: 'FAME_CHECKER', 364: 'TM_CASE', 365: 'BERRY_POUCH', 366: 'TEACHY_TV', 367: 'TRI_PASS', 368: 'RAINBOW_PASS', 369: 'TEA', 370: 'MYSTIC_TICKET', 371: 'AURORA_TICKET', 372: 'POWDER_JAR', 373: 'RUBY', 374: 'SAPPHIRE', 375: 'MAGMA_EMBLEM', 376: 'OLD_SEA_MAP'}

items_id = {'NONE': 0, 'MASTER_BALL': 1, 'ULTRA_BALL': 2, 'GREAT_BALL': 3, 'POKE_BALL': 4, 'SAFARI_BALL': 5, 'NET_BALL': 6, 'DIVE_BALL': 7, 'NEST_BALL': 8, 'REPEAT_BALL': 9, 'TIMER_BALL': 10, 'LUXURY_BALL': 11, 'PREMIER_BALL': 12, 'POTION': 13, 'ANTIDOTE': 14, 'BURN_HEAL': 15, 'ICE_HEAL': 16, 'AWAKENING': 17, 'PARALYZE_HEAL': 18, 'FULL_RESTORE': 19, 'MAX_POTION': 20, 'HYPER_POTION': 21, 'SUPER_POTION': 22, 'FULL_HEAL': 23, 'REVIVE': 24, 'MAX_REVIVE': 25, 'FRESH_WATER': 26, 'SODA_POP': 27, 'LEMONADE': 28, 'MOOMOO_MILK': 29, 'ENERGY_POWDER': 30, 'ENERGY_ROOT': 31, 'HEAL_POWDER': 32, 'REVIVAL_HERB': 33, 'ETHER': 34, 'MAX_ETHER': 35, 'ELIXIR': 36, 'MAX_ELIXIR': 37, 'LAVA_COOKIE': 38, 'BLUE_FLUTE': 39, 'YELLOW_FLUTE': 40, 'RED_FLUTE': 41, 'BLACK_FLUTE': 42, 'WHITE_FLUTE': 43, 'BERRY_JUICE': 44, 'SACRED_ASH': 45, 'SHOAL_SALT': 46, 'SHOAL_SHELL': 47, 'RED_SHARD': 48, 'BLUE_SHARD': 49, 'YELLOW_SHARD': 50, 'GREEN_SHARD': 51, '034': 52, '035': 53, '036': 54, '037': 55, '038': 56, '039': 57, '03A': 58, '03B': 59, '03C': 60, '03D': 61, '03E': 62, 'HP_UP': 63, 'PROTEIN': 64, 'IRON': 65, 'CARBOS': 66, 'CALCIUM': 67, 'RARE_CANDY': 68, 'PP_UP': 69, 'ZINC': 70, 'PP_MAX': 71, '048': 72, 'GUARD_SPEC': 73, 'DIRE_HIT': 74, 'X_ATTACK': 75, 'X_DEFEND': 76, 'X_SPEED': 77, 'X_ACCURACY': 78, 'X_SPECIAL': 79, 'POKE_DOLL': 80, 'FLUFFY_TAIL': 81, '052': 82, 'SUPER_REPEL': 83, 'MAX_REPEL': 84, 'ESCAPE_ROPE': 85, 'REPEL': 86, '057': 87, '058': 88, '059': 89, '05A': 90, '05B': 91, '05C': 92, 'SUN_STONE': 93, 'MOON_STONE': 94, 'FIRE_STONE': 95, 'THUNDER_STONE': 96, 'WATER_STONE': 97, 'LEAF_STONE': 98, '063': 99, '064': 100, '065': 101, '066': 102, 'TINY_MUSHROOM': 103, 'BIG_MUSHROOM': 104, '069': 105, 'PEARL': 106, 'BIG_PEARL': 107, 'STARDUST': 108, 'STAR_PIECE': 109, 'NUGGET': 110, 'HEART_SCALE': 111, '070': 112, '071': 113, '072': 114, '073': 115, '074': 116, '075': 117, '076': 118, '077': 119, '078': 120, 'ORANGE_MAIL': 121, 'HARBOR_MAIL': 122, 'GLITTER_MAIL': 123, 'MECH_MAIL': 124, 'WOOD_MAIL': 125, 'WAVE_MAIL': 126, 'BEAD_MAIL': 127, 'SHADOW_MAIL': 128, 'TROPIC_MAIL': 129, 'DREAM_MAIL': 130, 'FAB_MAIL': 131, 'RETRO_MAIL': 132, 'CHERI_BERRY': 133, 'CHESTO_BERRY': 134, 'PECHA_BERRY': 135, 'RAWST_BERRY': 136, 'ASPEAR_BERRY': 137, 'LEPPA_BERRY': 138, 'ORAN_BERRY': 139, 'PERSIM_BERRY': 140, 'LUM_BERRY': 141, 'SITRUS_BERRY': 142, 'FIGY_BERRY': 143, 'WIKI_BERRY': 144, 'MAGO_BERRY': 145, 'AGUAV_BERRY': 146, 'IAPAPA_BERRY': 147, 'RAZZ_BERRY': 148, 'BLUK_BERRY': 149, 'NANAB_BERRY': 150, 'WEPEAR_BERRY': 151, 'PINAP_BERRY': 152, 'POMEG_BERRY': 153, 'KELPSY_BERRY': 154, 'QUALOT_BERRY': 155, 'HONDEW_BERRY': 156, 'GREPA_BERRY': 157, 'TAMATO_BERRY': 158, 'CORNN_BERRY': 159, 'MAGOST_BERRY': 160, 'RABUTA_BERRY': 161, 'NOMEL_BERRY': 162, 'SPELON_BERRY': 163, 'PAMTRE_BERRY': 164, 'WATMEL_BERRY': 165, 'DURIN_BERRY': 166, 'BELUE_BERRY': 167, 'LIECHI_BERRY': 168, 'GANLON_BERRY': 169, 'SALAC_BERRY': 170, 'PETAYA_BERRY': 171, 'APICOT_BERRY': 172, 'LANSAT_BERRY': 173, 'STARF_BERRY': 174, 'ENIGMA_BERRY': 175, 'UNUSED_BERRY_1': 176, 'UNUSED_BERRY_2': 177, 'UNUSED_BERRY_3': 178, 'BRIGHT_POWDER': 179, 'WHITE_HERB': 180, 'MACHO_BRACE': 181, 'EXP_SHARE': 182, 'QUICK_CLAW': 183, 'SOOTHE_BELL': 184, 'MENTAL_HERB': 185, 'CHOICE_BAND': 186, 'KINGS_ROCK': 187, 'SILVER_POWDER': 188, 'AMULET_COIN': 189, 'CLEANSE_TAG': 190, 'SOUL_DEW': 191, 'DEEP_SEA_TOOTH': 192, 'DEEP_SEA_SCALE': 193, 'SMOKE_BALL': 194, 'EVERSTONE': 195, 'FOCUS_BAND': 196, 'LUCKY_EGG': 197, 'SCOPE_LENS': 198, 'METAL_COAT': 199, 'LEFTOVERS': 200, 'DRAGON_SCALE': 201, 'LIGHT_BALL': 202, 'SOFT_SAND': 203, 'HARD_STONE': 204, 'MIRACLE_SEED': 205, 'BLACK_GLASSES': 206, 'BLACK_BELT': 207, 'MAGNET': 208, 'MYSTIC_WATER': 209, 'SHARP_BEAK': 210, 'POISON_BARB': 211, 'NEVER_MELT_ICE': 212, 'SPELL_TAG': 213, 'TWISTED_SPOON': 214, 'CHARCOAL': 215, 'DRAGON_FANG': 216, 'SILK_SCARF': 217, 'UP_GRADE': 218, 'SHELL_BELL': 219, 'SEA_INCENSE': 220, 'LAX_INCENSE': 221, 'LUCKY_PUNCH': 222, 'METAL_POWDER': 223, 'THICK_CLUB': 224, 'STICK': 225, '0E2': 226, '0E3': 227, '0E4': 228, '0E5': 229, '0E6': 230, '0E7': 231, '0E8': 232, '0E9': 233, '0EA': 234, '0EB': 235, '0EC': 236, '0ED': 237, '0EE': 238, '0EF': 239, '0F0': 240, '0F1': 241, '0F2': 242, '0F3': 243, '0F4': 244, '0F5': 245, '0F6': 246, '0F7': 247, '0F8': 248, '0F9': 249, '0FA': 250, '0FB': 251, '0FC': 252, '0FD': 253, 'RED_SCARF': 254, 'BLUE_SCARF': 255, 'PINK_SCARF': 256, 'GREEN_SCARF': 257, 'YELLOW_SCARF': 258, 'MACH_BIKE': 259, 'COIN_CASE': 260, 'ITEMFINDER': 261, 'OLD_ROD': 262, 'GOOD_ROD': 263, 'SUPER_ROD': 264, 'SS_TICKET': 265, 'CONTEST_PASS': 266, '10B': 267, 'WAILMER_PAIL': 268, 'DEVON_GOODS': 269, 'SOOT_SACK': 270, 'BASEMENT_KEY': 271, 'ACRO_BIKE': 272, 'POKEBLOCK_CASE': 273, 'LETTER': 274, 'EON_TICKET': 275, 'RED_ORB': 276, 'BLUE_ORB': 277, 'SCANNER': 278, 'GO_GOGGLES': 279, 'METEORITE': 280, 'ROOM_1_KEY': 281, 'ROOM_2_KEY': 282, 'ROOM_4_KEY': 283, 'ROOM_6_KEY': 284, 'STORAGE_KEY': 285, 'ROOT_FOSSIL': 286, 'CLAW_FOSSIL': 287, 'DEVON_SCOPE': 288, 'TM01 Focus Punch': 289, 'TM02 Dragon Claw': 290, 'TM03 Water Pulse': 291, 'TM04 Calm Mind': 292, 'TM05 Roar': 293, 'TM06 Toxic': 294, 'TM07 Hail': 295, 'TM08 Bulk Up': 296, 'TM09 Bullet Seed': 297, 'TM10 Hidden Power': 298, 'TM11 Sunny Day': 299, 'TM12 Taunt': 300, 'TM13 Ice Beam': 301, 'TM14 Blizzard': 302, 'TM15 Hyper Beam': 303, 'TM16 Light Screen': 304, 'TM17 Protect': 305, 'TM18 Rain Dance': 306, 'TM19 Giga Drain': 307, 'TM20 Safeguard': 308, 'TM21 Frustration': 309, 'TM22 Solarbeam': 310, 'TM23 Iron Tail': 311, 'TM24 Thunderbolt': 312, 'TM25 Thunder': 313, 'TM26 Earthquake': 314, 'TM27 Return': 315, 'TM28 Dig': 316, 'TM29 Psychic': 317, 'TM30 Shadow Ball': 318, 'TM31 Brick Break': 319, 'TM32 Double Team': 320, 'TM33 Reflect': 321, 'TM34 Shock Wave': 322, 'TM35 Flamethrower': 323, 'TM36 Sludge Bomb': 324, 'TM37 Sandstorm': 325, 'TM38 Fire Blast': 326, 'TM39 Rock Tomb': 327, 'TM40 Aerial Ace': 328, 'TM41 Torment': 329, 'TM42 Facade': 330, 'TM43 Secret Power': 331, 'TM44 Rest': 332, 'TM45 Attract': 333, 'TM46 Thief': 334, 'TM47 Steel Wing': 335, 'TM48 Skill Swap': 336, 'TM49 Snatch': 337, 'TM50 Overheat': 338, 'HM01 Cut': 339, 'HM02 Fly': 340, 'HM03 Surf': 341, 'HM04 Strength': 342, 'HM05 Flash': 343, 'HM06 Rock Smash': 344, 'HM07 Waterfall': 345, 'HM08 Dive': 346, '15B': 347, '15C': 348, 'OAKS_PARCEL': 349, 'POKE_FLUTE': 350, 'SECRET_KEY': 351, 'BIKE_VOUCHER': 352, 'GOLD_TEETH': 353, 'OLD_AMBER': 354, 'CARD_KEY': 355, 'LIFT_KEY': 356, 'HELIX_FOSSIL': 357, 'DOME_FOSSIL': 358, 'SILPH_SCOPE': 359, 'BICYCLE': 360, 'TOWN_MAP': 361, 'VS_SEEKER': 362, 'FAME_CHECKER': 363, 'TM_CASE': 364, 'BERRY_POUCH': 365, 'TEACHY_TV': 366, 'TRI_PASS': 367, 'RAINBOW_PASS': 368, 'TEA': 369, 'MYSTIC_TICKET': 370, 'AURORA_TICKET': 371, 'POWDER_JAR': 372, 'RUBY': 373, 'SAPPHIRE': 374, 'MAGMA_EMBLEM': 375, 'OLD_SEA_MAP': 376}

items_pocket = {0: 'ITEMS', 1: 'POKE_BALLS', 2: 'POKE_BALLS', 3: 'POKE_BALLS', 4: 'POKE_BALLS', 5: 'POKE_BALLS', 6: 'POKE_BALLS', 7: 'POKE_BALLS', 8: 'POKE_BALLS', 9: 'POKE_BALLS', 10: 'POKE_BALLS', 11: 'POKE_BALLS', 12: 'POKE_BALLS', 13: 'ITEMS', 14: 'ITEMS', 15: 'ITEMS', 16: 'ITEMS', 17: 'ITEMS', 18: 'ITEMS', 19: 'ITEMS', 20: 'ITEMS', 21: 'ITEMS', 22: 'ITEMS', 23: 'ITEMS', 24: 'ITEMS', 25: 'ITEMS', 26: 'ITEMS', 27: 'ITEMS', 28: 'ITEMS', 29: 'ITEMS', 30: 'ITEMS', 31: 'ITEMS', 32: 'ITEMS', 33: 'ITEMS', 34: 'ITEMS', 35: 'ITEMS', 36: 'ITEMS', 37: 'ITEMS', 38: 'ITEMS', 39: 'ITEMS', 40: 'ITEMS', 41: 'ITEMS', 42: 'ITEMS', 43: 'ITEMS', 44: 'ITEMS', 45: 'ITEMS', 46: 'ITEMS', 47: 'ITEMS', 48: 'ITEMS', 49: 'ITEMS', 50: 'ITEMS', 51: 'ITEMS', 63: 'ITEMS', 64: 'ITEMS', 65: 'ITEMS', 66: 'ITEMS', 67: 'ITEMS', 68: 'ITEMS', 69: 'ITEMS', 70: 'ITEMS', 71: 'ITEMS', 73: 'ITEMS', 74: 'ITEMS', 75: 'ITEMS', 76: 'ITEMS', 77: 'ITEMS', 78: 'ITEMS', 79: 'ITEMS', 80: 'ITEMS', 81: 'ITEMS', 83: 'ITEMS', 84: 'ITEMS', 85: 'ITEMS', 86: 'ITEMS', 93: 'ITEMS', 94: 'ITEMS', 95: 'ITEMS', 96: 'ITEMS', 97: 'ITEMS', 98: 'ITEMS', 103: 'ITEMS', 104: 'ITEMS', 106: 'ITEMS', 107: 'ITEMS', 108: 'ITEMS', 109: 'ITEMS', 110: 'ITEMS', 111: 'ITEMS', 121: 'ITEMS', 122: 'ITEMS', 123: 'ITEMS', 124: 'ITEMS', 125: 'ITEMS', 126: 'ITEMS', 127: 'ITEMS', 128: 'ITEMS', 129: 'ITEMS', 130: 'ITEMS', 131: 'ITEMS', 132: 'ITEMS', 133: 'BERRIES', 134: 'BERRIES', 135: 'BERRIES', 136: 'BERRIES', 137: 'BERRIES', 138: 'BERRIES', 139: 'BERRIES', 140: 'BERRIES', 141: 'BERRIES', 142: 'BERRIES', 143: 'BERRIES', 144: 'BERRIES', 145: 'BERRIES', 146: 'BERRIES', 147: 'BERRIES', 148: 'BERRIES', 149: 'BERRIES', 150: 'BERRIES', 151: 'BERRIES', 152: 'BERRIES', 153: 'BERRIES', 154: 'BERRIES', 155: 'BERRIES', 156: 'BERRIES', 157: 'BERRIES', 158: 'BERRIES', 159: 'BERRIES', 160: 'BERRIES', 161: 'BERRIES', 162: 'BERRIES', 163: 'BERRIES', 164: 'BERRIES', 165: 'BERRIES', 166: 'BERRIES', 167: 'BERRIES', 168: 'BERRIES', 169: 'BERRIES', 170: 'BERRIES', 171: 'BERRIES', 172: 'BERRIES', 173: 'BERRIES', 174: 'BERRIES', 175: 'BERRIES', 179: 'ITEMS', 180: 'ITEMS', 181: 'ITEMS', 182: 'ITEMS', 183: 'ITEMS', 184: 'ITEMS', 185: 'ITEMS', 186: 'ITEMS', 187: 'ITEMS', 188: 'ITEMS', 189: 'ITEMS', 190: 'ITEMS', 191: 'ITEMS', 192: 'ITEMS', 193: 'ITEMS', 194: 'ITEMS', 195: 'ITEMS', 196: 'ITEMS', 197: 'ITEMS', 198: 'ITEMS', 199: 'ITEMS', 200: 'ITEMS', 201: 'ITEMS', 202: 'ITEMS', 203: 'ITEMS', 204: 'ITEMS', 205: 'ITEMS', 206: 'ITEMS', 207: 'ITEMS', 208: 'ITEMS', 209: 'ITEMS', 210: 'ITEMS', 211: 'ITEMS', 212: 'ITEMS', 213: 'ITEMS', 214: 'ITEMS', 215: 'ITEMS', 216: 'ITEMS', 217: 'ITEMS', 218: 'ITEMS', 219: 'ITEMS', 220: 'ITEMS', 221: 'ITEMS', 222: 'ITEMS', 223: 'ITEMS', 224: 'ITEMS', 225: 'ITEMS', 254: 'ITEMS', 255: 'ITEMS', 256: 'ITEMS', 257: 'ITEMS', 258: 'ITEMS', 259: 'KEY_ITEMS', 260: 'KEY_ITEMS', 261: 'KEY_ITEMS', 262: 'KEY_ITEMS', 263: 'KEY_ITEMS', 264: 'KEY_ITEMS', 265: 'KEY_ITEMS', 266: 'KEY_ITEMS', 268: 'KEY_ITEMS', 269: 'KEY_ITEMS', 270: 'KEY_ITEMS', 271: 'KEY_ITEMS', 272: 'KEY_ITEMS', 273: 'KEY_ITEMS', 274: 'KEY_ITEMS', 275: 'KEY_ITEMS', 276: 'KEY_ITEMS', 277: 'KEY_ITEMS', 278: 'KEY_ITEMS', 279: 'KEY_ITEMS', 280: 'KEY_ITEMS', 281: 'KEY_ITEMS', 282: 'KEY_ITEMS', 283: 'KEY_ITEMS', 284: 'KEY_ITEMS', 285: 'KEY_ITEMS', 286: 'KEY_ITEMS', 287: 'KEY_ITEMS', 288: 'KEY_ITEMS', 289: 'TM_HM', 290: 'TM_HM', 291: 'TM_HM', 292: 'TM_HM', 293: 'TM_HM', 294: 'TM_HM', 295: 'TM_HM', 296: 'TM_HM', 297: 'TM_HM', 298: 'TM_HM', 299: 'TM_HM', 300: 'TM_HM', 301: 'TM_HM', 302: 'TM_HM', 303: 'TM_HM', 304: 'TM_HM', 305: 'TM_HM', 306: 'TM_HM', 307: 'TM_HM', 308: 'TM_HM', 309: 'TM_HM', 310: 'TM_HM', 311: 'TM_HM', 312: 'TM_HM', 313: 'TM_HM', 314: 'TM_HM', 315: 'TM_HM', 316: 'TM_HM', 317: 'TM_HM', 318: 'TM_HM', 319: 'TM_HM', 320: 'TM_HM', 321: 'TM_HM', 322: 'TM_HM', 323: 'TM_HM', 324: 'TM_HM', 325: 'TM_HM', 326: 'TM_HM', 327: 'TM_HM', 328: 'TM_HM', 329: 'TM_HM', 330: 'TM_HM', 331: 'TM_HM', 332: 'TM_HM', 333: 'TM_HM', 334: 'TM_HM', 335: 'TM_HM', 336: 'TM_HM', 337: 'TM_HM', 338: 'TM_HM', 339: 'TM_HM', 340: 'TM_HM', 341: 'TM_HM', 342: 'TM_HM', 343: 'TM_HM', 344: 'TM_HM', 345: 'TM_HM', 346: 'TM_HM', 349: 'KEY_ITEMS', 350: 'KEY_ITEMS', 351: 'KEY_ITEMS', 352: 'KEY_ITEMS', 353: 'KEY_ITEMS', 354: 'KEY_ITEMS', 355: 'KEY_ITEMS', 356: 'KEY_ITEMS', 357: 'KEY_ITEMS', 358: 'KEY_ITEMS', 359: 'KEY_ITEMS', 360: 'KEY_ITEMS', 361: 'KEY_ITEMS', 362: 'KEY_ITEMS', 363: 'KEY_ITEMS', 364: 'KEY_ITEMS', 365: 'KEY_ITEMS', 366: 'KEY_ITEMS', 367: 'KEY_ITEMS', 368: 'KEY_ITEMS', 369: 'KEY_ITEMS', 370: 'KEY_ITEMS', 371: 'KEY_ITEMS', 372: 'KEY_ITEMS', 373: 'KEY_ITEMS', 374: 'KEY_ITEMS', 375: 'KEY_ITEMS', 376: 'KEY_ITEMS'}

items_name = {0: '????????', 1: 'MASTER BALL', 2: 'ULTRA BALL', 3: 'GREAT BALL', 4: 'POKé BALL', 5: 'SAFARI BALL', 6: 'NET BALL', 7: 'DIVE BALL', 8: 'NEST BALL', 9: 'REPEAT BALL', 10: 'TIMER BALL', 11: 'LUXURY BALL', 12: 'PREMIER BALL', 13: 'POTION', 14: 'ANTIDOTE', 15: 'BURN HEAL', 16: 'ICE HEAL', 17: 'AWAKENING', 18: 'PARLYZ HEAL', 19: 'FULL RESTORE', 20: 'MAX POTION', 21: 'HYPER POTION', 22: 'SUPER POTION', 23: 'FULL HEAL', 24: 'REVIVE', 25: 'MAX REVIVE', 26: 'FRESH WATER', 27: 'SODA POP', 28: 'LEMONADE', 29: 'MOOMOO MILK', 30: 'ENERGYPOWDER', 31: 'ENERGY ROOT', 32: 'HEAL POWDER', 33: 'REVIVAL HERB', 34: 'ETHER', 35: 'MAX ETHER', 36: 'ELIXIR', 37: 'MAX ELIXIR', 38: 'LAVA COOKIE', 39: 'BLUE FLUTE', 40: 'YELLOW FLUTE', 41: 'RED FLUTE', 42: 'BLACK FLUTE', 43: 'WHITE FLUTE', 44: 'BERRY JUICE', 45: 'SACRED ASH', 46: 'SHOAL SALT', 47: 'SHOAL SHELL', 48: 'RED SHARD', 49: 'BLUE SHARD', 50: 'YELLOW SHARD', 51: 'GREEN SHARD', 63: 'HP UP', 64: 'PROTEIN', 65: 'IRON', 66: 'CARBOS', 67: 'CALCIUM', 68: 'RARE CANDY', 69: 'PP UP', 70: 'ZINC', 71: 'PP MAX', 73: 'GUARD SPEC.', 74: 'DIRE HIT', 75: 'X ATTACK', 76: 'X DEFEND', 77: 'X SPEED', 78: 'X ACCURACY', 79: 'X SPECIAL', 80: 'POKé DOLL', 81: 'FLUFFY TAIL', 83: 'SUPER REPEL', 84: 'MAX REPEL', 85: 'ESCAPE ROPE', 86: 'REPEL', 93: 'SUN STONE', 94: 'MOON STONE', 95: 'FIRE STONE', 96: 'THUNDERSTONE', 97: 'WATER STONE', 98: 'LEAF STONE', 103: 'TINYMUSHROOM', 104: 'BIG MUSHROOM', 106: 'PEARL', 107: 'BIG PEARL', 108: 'STARDUST', 109: 'STAR PIECE', 110: 'NUGGET', 111: 'HEART SCALE', 121: 'ORANGE MAIL', 122: 'HARBOR MAIL', 123: 'GLITTER MAIL', 124: 'MECH MAIL', 125: 'WOOD MAIL', 126: 'WAVE MAIL', 127: 'BEAD MAIL', 128: 'SHADOW MAIL', 129: 'TROPIC MAIL', 130: 'DREAM MAIL', 131: 'FAB MAIL', 132: 'RETRO MAIL', 133: 'CHERI BERRY', 134: 'CHESTO BERRY', 135: 'PECHA BERRY', 136: 'RAWST BERRY', 137: 'ASPEAR BERRY', 138: 'LEPPA BERRY', 139: 'ORAN BERRY', 140: 'PERSIM BERRY', 141: 'LUM BERRY', 142: 'SITRUS BERRY', 143: 'FIGY BERRY', 144: 'WIKI BERRY', 145: 'MAGO BERRY', 146: 'AGUAV BERRY', 147: 'IAPAPA BERRY', 148: 'RAZZ BERRY', 149: 'BLUK BERRY', 150: 'NANAB BERRY', 151: 'WEPEAR BERRY', 152: 'PINAP BERRY', 153: 'POMEG BERRY', 154: 'KELPSY BERRY', 155: 'QUALOT BERRY', 156: 'HONDEW BERRY', 157: 'GREPA BERRY', 158: 'TAMATO BERRY', 159: 'CORNN BERRY', 160: 'MAGOST BERRY', 161: 'RABUTA BERRY', 162: 'NOMEL BERRY', 163: 'SPELON BERRY', 164: 'PAMTRE BERRY', 165: 'WATMEL BERRY', 166: 'DURIN BERRY', 167: 'BELUE BERRY', 168: 'LIECHI BERRY', 169: 'GANLON BERRY', 170: 'SALAC BERRY', 171: 'PETAYA BERRY', 172: 'APICOT BERRY', 173: 'LANSAT BERRY', 174: 'STARF BERRY', 175: 'ENIGMA BERRY', 179: 'BRIGHTPOWDER', 180: 'WHITE HERB', 181: 'MACHO BRACE', 182: 'EXP. SHARE', 183: 'QUICK CLAW', 184: 'SOOTHE BELL', 185: 'MENTAL HERB', 186: 'CHOICE BAND', 187: "KING'S ROCK", 188: 'SILVERPOWDER', 189: 'AMULET COIN', 190: 'CLEANSE TAG', 191: 'SOUL DEW', 192: 'DEEPSEATOOTH', 193: 'DEEPSEASCALE', 194: 'SMOKE BALL', 195: 'EVERSTONE', 196: 'FOCUS BAND', 197: 'LUCKY EGG', 198: 'SCOPE LENS', 199: 'METAL COAT', 200: 'LEFTOVERS', 201: 'DRAGON SCALE', 202: 'LIGHT BALL', 203: 'SOFT SAND', 204: 'HARD STONE', 205: 'MIRACLE SEED', 206: 'BLACKGLASSES', 207: 'BLACK BELT', 208: 'MAGNET', 209: 'MYSTIC WATER', 210: 'SHARP BEAK', 211: 'POISON BARB', 212: 'NEVERMELTICE', 213: 'SPELL TAG', 214: 'TWISTEDSPOON', 215: 'CHARCOAL', 216: 'DRAGON FANG', 217: 'SILK SCARF', 218: 'UP-GRADE', 219: 'SHELL BELL', 220: 'SEA INCENSE', 221: 'LAX INCENSE', 222: 'LUCKY PUNCH', 223: 'METAL POWDER', 224: 'THICK CLUB', 225: 'STICK', 254: 'RED SCARF', 255: 'BLUE SCARF', 256: 'PINK SCARF', 257: 'GREEN SCARF', 258: 'YELLOW SCARF', 259: 'MACH BIKE', 260: 'COIN CASE', 261: 'ITEMFINDER', 262: 'OLD ROD', 263: 'GOOD ROD', 264: 'SUPER ROD', 265: 'S.S. TICKET', 266: 'CONTEST PASS', 268: 'WAILMER PAIL', 269: 'DEVON GOODS', 270: 'SOOT SACK', 271: 'BASEMENT KEY', 272: 'ACRO BIKE', 273: '{POKEBLOCK} CASE', 274: 'LETTER', 275: 'EON TICKET', 276: 'RED ORB', 277: 'BLUE ORB', 278: 'SCANNER', 279: 'GO-GOGGLES', 280: 'METEORITE', 281: 'RM. 1 KEY', 282: 'RM. 2 KEY', 283: 'RM. 4 KEY', 284: 'RM. 6 KEY', 285: 'STORAGE KEY', 286: 'ROOT FOSSIL', 287: 'CLAW FOSSIL', 288: 'DEVON SCOPE', 289: 'TM01 Focus Punch', 290: 'TM02 Dragon Claw', 291: 'TM03 Water Pulse', 292: 'TM04 Calm Mind', 293: 'TM05 Roar', 294: 'TM06 Toxic', 295: 'TM07 Hail', 296: 'TM08 Bulk Up', 297: 'TM09 Bullet Seed', 298: 'TM10 Hidden Power', 299: 'TM11 Sunny Day', 300: 'TM12 Taunt', 301: 'TM13 Ice Beam', 302: 'TM14 Blizzard', 303: 'TM15 Hyper Beam', 304: 'TM16 Light Screen', 305: 'TM17 Protect', 306: 'TM18 Rain Dance', 307: 'TM19 Giga Drain', 308: 'TM20 Safeguard', 309: 'TM21 Frustration', 310: 'TM22 Solarbeam', 311: 'TM23 Iron Tail', 312: 'TM24 Thunderbolt', 313: 'TM25 Thunder', 314: 'TM26 Earthquake', 315: 'TM27 Return', 316: 'TM28 Dig', 317: 'TM29 Psychic', 318: 'TM30 Shadow Ball', 319: 'TM31 Brick Break', 320: 'TM32 Double Team', 321: 'TM33 Reflect', 322: 'TM34 Shock Wave', 323: 'TM35 Flamethrower', 324: 'TM36 Sludge Bomb', 325: 'TM37 Sandstorm', 326: 'TM38 Fire Blast', 327: 'TM39 Rock Tomb', 328: 'TM40 Aerial Ace', 329: 'TM41 Torment', 330: 'TM42 Facade', 331: 'TM43 Secret Power', 332: 'TM44 Rest', 333: 'TM45 Attract', 334: 'TM46 Thief', 335: 'TM47 Steel Wing', 336: 'TM48 Skill Swap', 337: 'TM49 Snatch', 338: 'TM50 Overheat', 339: 'HM01 Cut', 340: 'HM02 Fly', 341: 'HM03 Surf', 342: 'HM04 Strength', 343: 'HM05 Flash', 344: 'HM06 Rock Smash', 345: 'HM07 Waterfall', 346: 'HM08 Dive', 349: "OAK'S PARCEL", 350: 'POKé FLUTE', 351: 'SECRET KEY', 352: 'BIKE VOUCHER', 353: 'GOLD TEETH', 354: 'OLD AMBER', 355: 'CARD KEY', 356: 'LIFT KEY', 357: 'HELIX FOSSIL', 358: 'DOME FOSSIL', 359: 'SILPH SCOPE', 360: 'BICYCLE', 361: 'TOWN MAP', 362: 'VS SEEKER', 363: 'FAME CHECKER', 364: 'TM CASE', 365: 'BERRY POUCH', 366: 'TEACHY TV', 367: 'TRI-PASS', 368: 'RAINBOW PASS', 369: 'TEA', 370: 'MYSTICTICKET', 371: 'AURORATICKET', 372: 'POWDER JAR', 373: 'RUBY', 374: 'SAPPHIRE', 375: 'MAGMA EMBLEM', 376: 'OLD SEA MAP'}

nid_index =  {1: 'Bulbasaur', 2: 'Ivysaur', 3: 'Venusaur', 4: 'Charmander', 5: 'Charmeleon', 6: 'Charizard', 7: 'Squirtle', 8: 'Wartortle', 9: 'Blastoise', 10: 'Caterpie', 11: 'Metapod', 12: 'Butterfree', 13: 'Weedle', 14: 'Kakuna', 15: 'Beedrill', 16: 'Pidgey', 17: 'Pidgeotto', 18: 'Pidgeot', 19: 'Rattata', 20: 'Raticate', 21: 'Spearow', 22: 'Fearow', 23: 'Ekans', 24: 'Arbok', 25: 'Pikachu', 26: 'Raichu', 27: 'Sandshrew', 28: 'Sandslash', 29: 'Nidoran-F', 30: 'Nidorina', 31: 'Nidoqueen', 32: 'Nidoran-M', 33: 'Nidorino', 34: 'Nidoking', 35: 'Clefairy', 36: 'Clefable', 37: 'Vulpix', 38: 'Ninetales', 39: 'Jigglypuff', 40: 'Wigglytuff', 41: 'Zubat', 42: 'Golbat', 43: 'Oddish', 44: 'Gloom', 45: 'Vileplume', 46: 'Paras', 47: 'Parasect', 48: 'Venonat', 49: 'Venomoth', 50: 'Diglett', 51: 'Dugtrio', 52: 'Meowth', 53: 'Persian', 54: 'Psyduck', 55: 'Golduck', 56: 'Mankey', 57: 'Primeape', 58: 'Growlithe', 59: 'Arcanine', 60: 'Poliwag', 61: 'Poliwhirl', 62: 'Poliwrath', 63: 'Abra', 64: 'Kadabra', 65: 'Alakazam', 66: 'Machop', 67: 'Machoke', 68: 'Machamp', 69: 'Bellsprout', 70: 'Weepinbell', 71: 'Victreebel', 72: 'Tentacool', 73: 'Tentacruel', 74: 'Geodude', 75: 'Graveler', 76: 'Golem', 77: 'Ponyta', 78: 'Rapidash', 79: 'Slowpoke', 80: 'Slowbro', 81: 'Magnemite', 82: 'Magneton', 83: 'Farfetchd', 84: 'Doduo', 85: 'Dodrio', 86: 'Seel', 87: 'Dewgong', 88: 'Grimer', 89: 'Muk', 90: 'Shellder', 91: 'Cloyster', 92: 'Gastly', 93: 'Haunter', 94: 'Gengar', 95: 'Onix', 96: 'Drowzee', 97: 'Hypno', 98: 'Krabby', 99: 'Kingler', 100: 'Voltorb', 101: 'Electrode', 102: 'Exeggcute', 103: 'Exeggutor', 104: 'Cubone', 105: 'Marowak', 106: 'Hitmonlee', 107: 'Hitmonchan', 108: 'Lickitung', 109: 'Koffing', 110: 'Weezing', 111: 'Rhyhorn', 112: 'Rhydon', 113: 'Chansey', 114: 'Tangela', 115: 'Kangaskhan', 116: 'Horsea', 117: 'Seadra', 118: 'Goldeen', 119: 'Seaking', 120: 'Staryu', 121: 'Starmie', 122: 'Mr-Mime', 123: 'Scyther', 124: 'Jynx', 125: 'Electabuzz', 126: 'Magmar', 127: 'Pinsir', 128: 'Tauros', 129: 'Magikarp', 130: 'Gyarados', 131: 'Lapras', 132: 'Ditto', 133: 'Eevee', 134: 'Vaporeon', 135: 'Jolteon', 136: 'Flareon', 137: 'Porygon', 138: 'Omanyte', 139: 'Omastar', 140: 'Kabuto', 141: 'Kabutops', 142: 'Aerodactyl', 143: 'Snorlax', 144: 'Articuno', 145: 'Zapdos', 146: 'Moltres', 147: 'Dratini', 148: 'Dragonair', 149: 'Dragonite', 150: 'Mewtwo', 151: 'Mew', 152: 'Chikorita', 153: 'Bayleef', 154: 'Meganium', 155: 'Cyndaquil', 156: 'Quilava', 157: 'Typhlosion', 158: 'Totodile', 159: 'Croconaw', 160: 'Feraligatr', 161: 'Sentret', 162: 'Furret', 163: 'Hoothoot', 164: 'Noctowl', 165: 'Ledyba', 166: 'Ledian', 167: 'Spinarak', 168: 'Ariados', 169: 'Crobat', 170: 'Chinchou', 171: 'Lanturn', 172: 'Pichu', 173: 'Cleffa', 174: 'Igglybuff', 175: 'Togepi', 176: 'Togetic', 177: 'Natu', 178: 'Xatu', 179: 'Mareep', 180: 'Flaaffy', 181: 'Ampharos', 182: 'Bellossom', 183: 'Marill', 184: 'Azumarill', 185: 'Sudowoodo', 186: 'Politoed', 187: 'Hoppip', 188: 'Skiploom', 189: 'Jumpluff', 190: 'Aipom', 191: 'Sunkern', 192: 'Sunflora', 193: 'Yanma', 194: 'Wooper', 195: 'Quagsire', 196: 'Espeon', 197: 'Umbreon', 198: 'Murkrow', 199: 'Slowking', 200: 'Misdreavus', 201: 'Unown', 202: 'Wobbuffet', 203: 'Girafarig', 204: 'Pineco', 205: 'Forretress', 206: 'Dunsparce', 207: 'Gligar', 208: 'Steelix', 209: 'Snubbull', 210: 'Granbull', 211: 'Qwilfish', 212: 'Scizor', 213: 'Shuckle', 214: 'Heracross', 215: 'Sneasel', 216: 'Teddiursa', 217: 'Ursaring', 218: 'Slugma', 219: 'Magcargo', 220: 'Swinub', 221: 'Piloswine', 222: 'Corsola', 223: 'Remoraid', 224: 'Octillery', 225: 'Delibird', 226: 'Mantine', 227: 'Skarmory', 228: 'Houndour', 229: 'Houndoom', 230: 'Kingdra', 231: 'Phanpy', 232: 'Donphan', 233: 'Porygon2', 234: 'Stantler', 235: 'Smeargle', 236: 'Tyrogue', 237: 'Hitmontop', 238: 'Smoochum', 239: 'Elekid', 240: 'Magby', 241: 'Miltank', 242: 'Blissey', 243: 'Raikou', 244: 'Entei', 245: 'Suicune', 246: 'Larvitar', 247: 'Pupitar', 248: 'Tyranitar', 249: 'Lugia', 250: 'Ho-Oh', 251: 'Celebi', 252: 'Treecko', 253: 'Grovyle', 254: 'Sceptile', 255: 'Torchic', 256: 'Combusken', 257: 'Blaziken', 258: 'Mudkip', 259: 'Marshtomp', 260: 'Swampert', 261: 'Poochyena', 262: 'Mightyena', 263: 'Zigzagoon', 264: 'Linoone', 265: 'Wurmple', 266: 'Silcoon', 267: 'Beautifly', 268: 'Cascoon', 269: 'Dustox', 270: 'Lotad', 271: 'Lombre', 272: 'Ludicolo', 273: 'Seedot', 274: 'Nuzleaf', 275: 'Shiftry', 276: 'Taillow', 277: 'Swellow', 278: 'Wingull', 279: 'Pelipper', 280: 'Ralts', 281: 'Kirlia', 282: 'Gardevoir', 283: 'Surskit', 284: 'Masquerain', 285: 'Shroomish', 286: 'Breloom', 287: 'Slakoth', 288: 'Vigoroth', 289: 'Slaking', 290: 'Nincada', 291: 'Ninjask', 292: 'Shedinja', 293: 'Whismur', 294: 'Loudred', 295: 'Exploud', 296: 'Makuhita', 297: 'Hariyama', 298: 'Azurill', 299: 'Nosepass', 300: 'Skitty', 301: 'Delcatty', 302: 'Sableye', 303: 'Mawile', 304: 'Aron', 305: 'Lairon', 306: 'Aggron', 307: 'Meditite', 308: 'Medicham', 309: 'Electrike', 310: 'Manectric', 311: 'Plusle', 312: 'Minun', 313: 'Volbeat', 314: 'Illumise', 315: 'Roselia', 316: 'Gulpin', 317: 'Swalot', 318: 'Carvanha', 319: 'Sharpedo', 320: 'Wailmer', 321: 'Wailord', 322: 'Numel', 323: 'Camerupt', 324: 'Torkoal', 325: 'Spoink', 326: 'Grumpig', 327: 'Spinda', 328: 'Trapinch', 329: 'Vibrava', 330: 'Flygon', 331: 'Cacnea', 332: 'Cacturne', 333: 'Swablu', 334: 'Altaria', 335: 'Zangoose', 336: 'Seviper', 337: 'Lunatone', 338: 'Solrock', 339: 'Barboach', 340: 'Whiscash', 341: 'Corphish', 342: 'Crawdaunt', 343: 'Baltoy', 344: 'Claydol', 345: 'Lileep', 346: 'Cradily', 347: 'Anorith', 348: 'Armaldo', 349: 'Feebas', 350: 'Milotic', 351: 'Castform', 352: 'Kecleon', 353: 'Shuppet', 354: 'Banette', 355: 'Duskull', 356: 'Dusclops', 357: 'Tropius', 358: 'Chimecho', 359: 'Absol', 360: 'Wynaut', 361: 'Snorunt', 362: 'Glalie', 363: 'Spheal', 364: 'Sealeo', 365: 'Walrein', 366: 'Clamperl', 367: 'Huntail', 368: 'Gorebyss', 369: 'Relicanth', 370: 'Luvdisc', 371: 'Bagon', 372: 'Shelgon', 373: 'Salamence', 374: 'Beldum', 375: 'Metang', 376: 'Metagross', 377: 'Regirock', 378: 'Regice', 379: 'Registeel', 380: 'Latias', 381: 'Latios', 382: 'Kyogre', 383: 'Groudon', 384: 'Rayquaza', 385: 'Jirachi', 386: 'Deoxys'}

nid_name =  {'Bulbasaur': 1, 'Ivysaur': 2, 'Venusaur': 3, 'Charmander': 4, 'Charmeleon': 5, 'Charizard': 6, 'Squirtle': 7, 'Wartortle': 8, 'Blastoise': 9, 'Caterpie': 10, 'Metapod': 11, 'Butterfree': 12, 'Weedle': 13, 'Kakuna': 14, 'Beedrill': 15, 'Pidgey': 16, 'Pidgeotto': 17, 'Pidgeot': 18, 'Rattata': 19, 'Raticate': 20, 'Spearow': 21, 'Fearow': 22, 'Ekans': 23, 'Arbok': 24, 'Pikachu': 25, 'Raichu': 26, 'Sandshrew': 27, 'Sandslash': 28, 'Nidoran-F': 29, 'Nidorina': 30, 'Nidoqueen': 31, 'Nidoran-M': 32, 'Nidorino': 33, 'Nidoking': 34, 'Clefairy': 35, 'Clefable': 36, 'Vulpix': 37, 'Ninetales': 38, 'Jigglypuff': 39, 'Wigglytuff': 40, 'Zubat': 41, 'Golbat': 42, 'Oddish': 43, 'Gloom': 44, 'Vileplume': 45, 'Paras': 46, 'Parasect': 47, 'Venonat': 48, 'Venomoth': 49, 'Diglett': 50, 'Dugtrio': 51, 'Meowth': 52, 'Persian': 53, 'Psyduck': 54, 'Golduck': 55, 'Mankey': 56, 'Primeape': 57, 'Growlithe': 58, 'Arcanine': 59, 'Poliwag': 60, 'Poliwhirl': 61, 'Poliwrath': 62, 'Abra': 63, 'Kadabra': 64, 'Alakazam': 65, 'Machop': 66, 'Machoke': 67, 'Machamp': 68, 'Bellsprout': 69, 'Weepinbell': 70, 'Victreebel': 71, 'Tentacool': 72, 'Tentacruel': 73, 'Geodude': 74, 'Graveler': 75, 'Golem': 76, 'Ponyta': 77, 'Rapidash': 78, 'Slowpoke': 79, 'Slowbro': 80, 'Magnemite': 81, 'Magneton': 82, 'Farfetchd': 83, 'Doduo': 84, 'Dodrio': 85, 'Seel': 86, 'Dewgong': 87, 'Grimer': 88, 'Muk': 89, 'Shellder': 90, 'Cloyster': 91, 'Gastly': 92, 'Haunter': 93, 'Gengar': 94, 'Onix': 95, 'Drowzee': 96, 'Hypno': 97, 'Krabby': 98, 'Kingler': 99, 'Voltorb': 100, 'Electrode': 101, 'Exeggcute': 102, 'Exeggutor': 103, 'Cubone': 104, 'Marowak': 105, 'Hitmonlee': 106, 'Hitmonchan': 107, 'Lickitung': 108, 'Koffing': 109, 'Weezing': 110, 'Rhyhorn': 111, 'Rhydon': 112, 'Chansey': 113, 'Tangela': 114, 'Kangaskhan': 115, 'Horsea': 116, 'Seadra': 117, 'Goldeen': 118, 'Seaking': 119, 'Staryu': 120, 'Starmie': 121, 'Mr-Mime': 122, 'Scyther': 123, 'Jynx': 124, 'Electabuzz': 125, 'Magmar': 126, 'Pinsir': 127, 'Tauros': 128, 'Magikarp': 129, 'Gyarados': 130, 'Lapras': 131, 'Ditto': 132, 'Eevee': 133, 'Vaporeon': 134, 'Jolteon': 135, 'Flareon': 136, 'Porygon': 137, 'Omanyte': 138, 'Omastar': 139, 'Kabuto': 140, 'Kabutops': 141, 'Aerodactyl': 142, 'Snorlax': 143, 'Articuno': 144, 'Zapdos': 145, 'Moltres': 146, 'Dratini': 147, 'Dragonair': 148, 'Dragonite': 149, 'Mewtwo': 150, 'Mew': 151, 'Chikorita': 152, 'Bayleef': 153, 'Meganium': 154, 'Cyndaquil': 155, 'Quilava': 156, 'Typhlosion': 157, 'Totodile': 158, 'Croconaw': 159, 'Feraligatr': 160, 'Sentret': 161, 'Furret': 162, 'Hoothoot': 163, 'Noctowl': 164, 'Ledyba': 165, 'Ledian': 166, 'Spinarak': 167, 'Ariados': 168, 'Crobat': 169, 'Chinchou': 170, 'Lanturn': 171, 'Pichu': 172, 'Cleffa': 173, 'Igglybuff': 174, 'Togepi': 175, 'Togetic': 176, 'Natu': 177, 'Xatu': 178, 'Mareep': 179, 'Flaaffy': 180, 'Ampharos': 181, 'Bellossom': 182, 'Marill': 183, 'Azumarill': 184, 'Sudowoodo': 185, 'Politoed': 186, 'Hoppip': 187, 'Skiploom': 188, 'Jumpluff': 189, 'Aipom': 190, 'Sunkern': 191, 'Sunflora': 192, 'Yanma': 193, 'Wooper': 194, 'Quagsire': 195, 'Espeon': 196, 'Umbreon': 197, 'Murkrow': 198, 'Slowking': 199, 'Misdreavus': 200, 'Unown': 201, 'Wobbuffet': 202, 'Girafarig': 203, 'Pineco': 204, 'Forretress': 205, 'Dunsparce': 206, 'Gligar': 207, 'Steelix': 208, 'Snubbull': 209, 'Granbull': 210, 'Qwilfish': 211, 'Scizor': 212, 'Shuckle': 213, 'Heracross': 214, 'Sneasel': 215, 'Teddiursa': 216, 'Ursaring': 217, 'Slugma': 218, 'Magcargo': 219, 'Swinub': 220, 'Piloswine': 221, 'Corsola': 222, 'Remoraid': 223, 'Octillery': 224, 'Delibird': 225, 'Mantine': 226, 'Skarmory': 227, 'Houndour': 228, 'Houndoom': 229, 'Kingdra': 230, 'Phanpy': 231, 'Donphan': 232, 'Porygon2': 233, 'Stantler': 234, 'Smeargle': 235, 'Tyrogue': 236, 'Hitmontop': 237, 'Smoochum': 238, 'Elekid': 239, 'Magby': 240, 'Miltank': 241, 'Blissey': 242, 'Raikou': 243, 'Entei': 244, 'Suicune': 245, 'Larvitar': 246, 'Pupitar': 247, 'Tyranitar': 248, 'Lugia': 249, 'Ho-Oh': 250, 'Celebi': 251, 'Treecko': 252, 'Grovyle': 253, 'Sceptile': 254, 'Torchic': 255, 'Combusken': 256, 'Blaziken': 257, 'Mudkip': 258, 'Marshtomp': 259, 'Swampert': 260, 'Poochyena': 261, 'Mightyena': 262, 'Zigzagoon': 263, 'Linoone': 264, 'Wurmple': 265, 'Silcoon': 266, 'Beautifly': 267, 'Cascoon': 268, 'Dustox': 269, 'Lotad': 270, 'Lombre': 271, 'Ludicolo': 272, 'Seedot': 273, 'Nuzleaf': 274, 'Shiftry': 275, 'Taillow': 276, 'Swellow': 277, 'Wingull': 278, 'Pelipper': 279, 'Ralts': 280, 'Kirlia': 281, 'Gardevoir': 282, 'Surskit': 283, 'Masquerain': 284, 'Shroomish': 285, 'Breloom': 286, 'Slakoth': 287, 'Vigoroth': 288, 'Slaking': 289, 'Nincada': 290, 'Ninjask': 291, 'Shedinja': 292, 'Whismur': 293, 'Loudred': 294, 'Exploud': 295, 'Makuhita': 296, 'Hariyama': 297, 'Azurill': 298, 'Nosepass': 299, 'Skitty': 300, 'Delcatty': 301, 'Sableye': 302, 'Mawile': 303, 'Aron': 304, 'Lairon': 305, 'Aggron': 306, 'Meditite': 307, 'Medicham': 308, 'Electrike': 309, 'Manectric': 310, 'Plusle': 311, 'Minun': 312, 'Volbeat': 313, 'Illumise': 314, 'Roselia': 315, 'Gulpin': 316, 'Swalot': 317, 'Carvanha': 318, 'Sharpedo': 319, 'Wailmer': 320, 'Wailord': 321, 'Numel': 322, 'Camerupt': 323, 'Torkoal': 324, 'Spoink': 325, 'Grumpig': 326, 'Spinda': 327, 'Trapinch': 328, 'Vibrava': 329, 'Flygon': 330, 'Cacnea': 331, 'Cacturne': 332, 'Swablu': 333, 'Altaria': 334, 'Zangoose': 335, 'Seviper': 336, 'Lunatone': 337, 'Solrock': 338, 'Barboach': 339, 'Whiscash': 340, 'Corphish': 341, 'Crawdaunt': 342, 'Baltoy': 343, 'Claydol': 344, 'Lileep': 345, 'Cradily': 346, 'Anorith': 347, 'Armaldo': 348, 'Feebas': 349, 'Milotic': 350, 'Castform': 351, 'Kecleon': 352, 'Shuppet': 353, 'Banette': 354, 'Duskull': 355, 'Dusclops': 356, 'Tropius': 357, 'Chimecho': 358, 'Absol': 359, 'Wynaut': 360, 'Snorunt': 361, 'Glalie': 362, 'Spheal': 363, 'Sealeo': 364, 'Walrein': 365, 'Clamperl': 366, 'Huntail': 367, 'Gorebyss': 368, 'Relicanth': 369, 'Luvdisc': 370, 'Bagon': 371, 'Shelgon': 372, 'Salamence': 373, 'Beldum': 374, 'Metang': 375, 'Metagross': 376, 'Regirock': 377, 'Regice': 378, 'Registeel': 379, 'Latias': 380, 'Latios': 381, 'Kyogre': 382, 'Groudon': 383, 'Rayquaza': 384, 'Jirachi': 385, 'Deoxys': 386}

nid_obtainable =  {1: 'No', 2: 'No', 3: 'No', 4: 'No', 5: 'No', 6: 'No', 7: 'No', 8: 'No', 9: 'No', 10: 'No', 11: 'No', 12: 'No', 13: 'No', 14: 'No', 15: 'No', 16: 'No', 17: 'No', 18: 'No', 19: 'No', 20: 'No', 21: 'No', 22: 'No', 23: 'No', 24: 'No', 25: 'Yes', 26: 'Yes', 27: 'Yes', 28: 'Yes', 29: 'No', 30: 'No', 31: 'No', 32: 'No', 33: 'No', 34: 'No', 35: 'No', 36: 'No', 37: 'Yes', 38: 'Yes', 39: 'Yes', 40: 'Yes', 41: 'Yes', 42: 'Yes', 43: 'Yes', 44: 'Yes', 45: 'Yes', 46: 'No', 47: 'No', 48: 'No', 49: 'No', 50: 'No', 51: 'No', 52: 'Yes', 53: 'Yes', 54: 'Yes', 55: 'Yes', 56: 'No', 57: 'No', 58: 'No', 59: 'No', 60: 'No', 61: 'No', 62: 'No', 63: 'Yes', 64: 'Yes', 65: 'No', 66: 'Yes', 67: 'Yes', 68: 'No', 69: 'No', 70: 'No', 71: 'No', 72: 'Yes', 73: 'Yes', 74: 'Yes', 75: 'Yes', 76: 'No', 77: 'No', 78: 'No', 79: 'No', 80: 'No', 81: 'Yes', 82: 'Yes', 83: 'No', 84: 'Yes', 85: 'Yes', 86: 'No', 87: 'No', 88: 'Yes', 89: 'Yes', 90: 'No', 91: 'No', 92: 'No', 93: 'No', 94: 'No', 95: 'No', 96: 'No', 97: 'No', 98: 'No', 99: 'No', 100: 'Yes', 101: 'Yes', 102: 'No', 103: 'No', 104: 'No', 105: 'No', 106: 'No', 107: 'No', 108: 'No', 109: 'Yes', 110: 'Yes', 111: 'Yes', 112: 'Yes', 113: 'No', 114: 'No', 115: 'No', 116: 'Yes', 117: 'Yes', 118: 'Yes', 119: 'Yes', 120: 'Yes', 121: 'Yes', 122: 'No', 123: 'No', 124: 'No', 125: 'No', 126: 'No', 127: 'Yes', 128: 'No', 129: 'Yes', 130: 'Yes', 131: 'No', 132: 'Yes', 133: 'No', 134: 'No', 135: 'No', 136: 'No', 137: 'No', 138: 'No', 139: 'No', 140: 'No', 141: 'No', 142: 'No', 143: 'No', 144: 'No', 145: 'No', 146: 'No', 147: 'No', 148: 'No', 149: 'No', 150: 'No', 151: 'No', 152: 'No', 153: 'No', 154: 'No', 155: 'No', 156: 'No', 157: 'No', 158: 'No', 159: 'No', 160: 'No', 161: 'No', 162: 'No', 163: 'Yes', 164: 'Yes', 165: 'Yes', 166: 'Yes', 167: 'Yes', 168: 'Yes', 169: 'Yes', 170: 'Yes', 171: 'Yes', 172: 'Yes', 173: 'No', 174: 'Yes', 175: 'No', 176: 'No', 177: 'Yes', 178: 'Yes', 179: 'Yes', 180: 'Yes', 181: 'Yes', 182: 'Yes', 183: 'Yes', 184: 'Yes', 185: 'Yes', 186: 'No', 187: 'No', 188: 'No', 189: 'No', 190: 'Yes', 191: 'Yes', 192: 'Yes', 193: 'No', 194: 'Yes', 195: 'Yes', 196: 'No', 197: 'No', 198: 'No', 199: 'No', 200: 'No', 201: 'No', 202: 'Yes', 203: 'Yes', 204: 'Yes', 205: 'Yes', 206: 'No', 207: 'Yes', 208: 'No', 209: 'Yes', 210: 'Yes', 211: 'No', 212: 'No', 213: 'Yes', 214: 'Yes', 215: 'No', 216: 'Yes', 217: 'Yes', 218: 'Yes', 219: 'Yes', 220: 'No', 221: 'No', 222: 'Yes', 223: 'Yes', 224: 'Yes', 225: 'No', 226: 'No', 227: 'Yes', 228: 'Yes', 229: 'Yes', 230: 'No', 231: 'Yes', 232: 'Yes', 233: 'No', 234: 'Yes', 235: 'Yes', 236: 'No', 237: 'No', 238: 'No', 239: 'No', 240: 'No', 241: 'Yes', 242: 'No', 243: 'No', 244: 'No', 245: 'No', 246: 'No', 247: 'No', 248: 'No', 249: 'No', 250: 'No', 251: 'No', 252: 'Yes', 253: 'Yes', 254: 'Yes', 255: 'No', 256: 'No', 257: 'No', 258: 'No', 259: 'No', 260: 'No', 261: 'Yes', 262: 'Yes', 263: 'Yes', 264: 'Yes', 265: 'Yes', 266: 'Yes', 267: 'Yes', 268: 'Yes', 269: 'Yes', 270: 'Yes', 271: 'Yes', 272: 'Yes', 273: 'Yes', 274: 'Yes', 275: 'Yes', 276: 'Yes', 277: 'Yes', 278: 'Yes', 279: 'Yes', 280: 'Yes', 281: 'Yes', 282: 'Yes', 283: 'No', 284: 'No', 285: 'Yes', 286: 'Yes', 287: 'Yes', 288: 'Yes', 289: 'Yes', 290: 'Yes', 291: 'Yes', 292: 'Yes', 293: 'Yes', 294: 'Yes', 295: 'Yes', 296: 'Yes', 297: 'Yes', 298: 'Yes', 299: 'Yes', 300: 'Yes', 301: 'No', 302: 'Yes', 303: 'Yes', 304: 'Yes', 305: 'Yes', 306: 'Yes', 307: 'No', 308: 'No', 309: 'Yes', 310: 'Yes', 311: 'Yes', 312: 'Yes', 313: 'Yes', 314: 'Yes', 315: 'No', 316: 'Yes', 317: 'Yes', 318: 'Yes', 319: 'Yes', 320: 'Yes', 321: 'Yes', 322: 'Yes', 323: 'Yes', 324: 'Yes', 325: 'Yes', 326: 'Yes', 327: 'Yes', 328: 'Yes', 329: 'Yes', 330: 'Yes', 331: 'Yes', 332: 'Yes', 333: 'Yes', 334: 'Yes', 335: 'No', 336: 'Yes', 337: 'No', 338: 'Yes', 339: 'Yes', 340: 'Yes', 341: 'Yes', 342: 'Yes', 343: 'Yes', 344: 'Yes', 345: 'Yes', 346: 'Yes', 347: 'Yes', 348: 'Yes', 349: 'Yes', 350: 'Yes', 351: 'Yes', 352: 'Yes', 353: 'Yes', 354: 'Yes', 355: 'Yes', 356: 'Yes', 357: 'Yes', 358: 'Yes', 359: 'Yes', 360: 'Yes', 361: 'Yes', 362: 'Yes', 363: 'Yes', 364: 'Yes', 365: 'Yes', 366: 'Yes', 367: 'No', 368: 'No', 369: 'Yes', 370: 'Yes', 371: 'Yes', 372: 'Yes', 373: 'Yes', 374: 'Yes', 375: 'Yes', 376: 'Yes', 377: 'Yes', 378: 'Yes', 379: 'Yes', 380: 'Yes', 381: 'No', 382: 'Yes', 383: 'Yes', 384: 'Yes', 385: 'No', 386: 'No'}

nid_method =  {1: 'Trade', 2: 'Trade', 3: 'Trade', 4: 'Trade', 5: 'Trade', 6: 'Trade', 7: 'Trade', 8: 'Trade', 9: 'Trade', 10: 'Trade', 11: 'Trade', 12: 'Trade', 13: 'Trade', 14: 'Trade', 15: 'Trade', 16: 'Trade', 17: 'Trade', 18: 'Trade', 19: 'Trade', 20: 'Trade', 21: 'Trade', 22: 'Trade', 23: 'Trade', 24: 'Trade', 25: 'Catch', 26: 'Evolve', 27: 'Catch', 28: 'Evolve', 29: 'Trade', 30: 'Trade', 31: 'Trade', 32: 'Trade', 33: 'Trade', 34: 'Trade', 35: 'Trade', 36: 'Trade', 37: 'Catch', 38: 'Evolve', 39: 'Catch', 40: 'Evolve - Only 1 Moon Stone (Delcatty or Wigglytuff)', 41: 'Catch', 42: 'Catch,Evolve', 43: 'Catch', 44: 'Catch,Evolve', 45: 'Evolve', 46: 'Trade', 47: 'Trade', 48: 'Trade', 49: 'Trade', 50: 'Trade', 51: 'Trade', 52: 'Trade NPC', 53: 'Evolve', 54: 'Catch', 55: 'Catch,Evolve', 56: 'Trade', 57: 'Trade', 58: 'Trade', 59: 'Trade', 60: 'Trade', 61: 'Trade', 62: 'Trade', 63: 'Catch', 64: 'Evolve', 65: 'Trade Evo', 66: 'Catch', 67: 'Evolve', 68: 'Trade Evo', 69: 'Trade', 70: 'Trade', 71: 'Trade', 72: 'Catch', 73: 'Catch,Evolve', 74: 'Catch', 75: 'Catch,Evolve', 76: 'Trade Evo', 77: 'Trade', 78: 'Trade', 79: 'Trade', 80: 'Trade', 81: 'Catch', 82: 'Catch,Evolve', 83: 'Trade', 84: 'Catch', 85: 'Catch,Evolve', 86: 'Trade', 87: 'Trade', 88: 'Catch', 89: 'Evolve', 90: 'Trade', 91: 'Trade', 92: 'Trade', 93: 'Trade', 94: 'Trade', 95: 'Trade', 96: 'Trade', 97: 'Trade', 98: 'Trade', 99: 'Trade', 100: 'Catch', 101: 'Catch,Evolve', 102: 'Trade', 103: 'Trade', 104: 'Trade', 105: 'Trade', 106: 'Trade', 107: 'Trade', 108: 'Trade', 109: 'Catch', 110: 'Evolve', 111: 'Catch', 112: 'Evolve', 113: 'Trade', 114: 'Trade', 115: 'Trade', 116: 'Catch', 117: 'Evolve', 118: 'Catch', 119: 'Catch,Evolve', 120: 'Catch', 121: 'Evolve', 122: 'Trade', 123: 'Trade', 124: 'Trade', 125: 'Trade', 126: 'Trade', 127: 'Catch', 128: 'Trade', 129: 'Catch', 130: 'Catch,Evolve', 131: 'Trade', 132: 'Catch', 133: 'Trade', 134: 'Trade', 135: 'Trade', 136: 'Trade', 137: 'Trade', 138: 'Trade', 139: 'Trade', 140: 'Trade', 141: 'Trade', 142: 'Trade', 143: 'Trade', 144: 'Trade', 145: 'Trade', 146: 'Trade', 147: 'Trade', 148: 'Trade', 149: 'Trade', 150: 'Trade', 151: 'Event Item required (Japan only)', 152: 'Trade, Complete Regional Dex', 153: 'Trade', 154: 'Trade', 155: 'Trade, Complete Regional Dex', 156: 'Trade', 157: 'Trade', 158: 'Trade, Complete Regional Dex', 159: 'Trade', 160: 'Trade', 161: 'Trade', 162: 'Trade', 163: 'Catch', 164: 'Evolve', 165: 'Catch', 166: 'Evolve', 167: 'Catch', 168: 'Evolve', 169: 'Evolve', 170: 'Catch', 171: 'Evolve', 172: 'Breed', 173: 'Trade', 174: 'Breed', 175: 'Trade', 176: 'Trade', 177: 'Catch', 178: 'Catch,Evolve', 179: 'Catch', 180: 'Evolve', 181: 'Evolve', 182: 'Evolve', 183: 'Catch', 184: 'Evolve', 185: 'Catch', 186: 'Trade,Trade Evo', 187: 'Trade', 188: 'Trade', 189: 'Trade', 190: 'Catch', 191: 'Catch', 192: 'Evolve', 193: 'Trade', 194: 'Catch', 195: 'Catch,Evolve', 196: 'Trade', 197: 'Trade', 198: 'Trade', 199: 'Trade', 200: 'Trade', 201: 'Trade', 202: 'Catch', 203: 'Catch', 204: 'Catch', 205: 'Evolve', 206: 'Trade', 207: 'Catch', 208: 'Trade', 209: 'Catch', 210: 'Evolve', 211: 'Trade', 212: 'Trade', 213: 'Catch', 214: 'Catch', 215: 'Trade', 216: 'Catch', 217: 'Evolve', 218: 'Catch', 219: 'Evolve', 220: 'Trade', 221: 'Trade', 222: 'Catch', 223: 'Catch', 224: 'Catch,Evolve', 225: 'Trade', 226: 'Trade', 227: 'Catch', 228: 'Catch', 229: 'Evolve', 230: 'Trade Evo', 231: 'Catch', 232: 'Evolve', 233: 'Trade,Trade Evo', 234: 'Catch', 235: 'Catch', 236: 'Trade', 237: 'Trade', 238: 'Trade', 239: 'Trade', 240: 'Trade', 241: 'Catch', 242: 'Trade', 243: 'Trade', 244: 'Trade', 245: 'Trade', 246: 'Trade', 247: 'Trade', 248: 'Trade', 249: 'Event Item required', 250: 'Event Item required', 251: 'Trade, Event', 252: 'Starter - 1 evo line only', 253: 'Starter - 1 evo line only', 254: 'Starter - 1 evo line only', 255: 'Starter - 1 evo line only', 256: 'Starter - 1 evo line only', 257: 'Starter - 1 evo line only', 258: 'Starter - 1 evo line only', 259: 'Starter - 1 evo line only', 260: 'Starter - 1 evo line only', 261: 'Catch', 262: 'Catch,Evolve', 263: 'Catch', 264: 'Catch,Evolve', 265: 'Catch', 266: 'Catch,Evolve', 267: 'Evolve', 268: 'Catch,Evolve', 269: 'Evolve', 270: 'Catch', 271: 'Catch,Evolve', 272: 'Evolve', 273: 'Catch', 274: 'Catch,Evolve', 275: 'Evolve', 276: 'Catch', 277: 'Catch,Evolve', 278: 'Catch', 279: 'Catch,Evolve', 280: 'Catch', 281: 'Evolve', 282: 'Evolve', 283: 'Swarm - Only after record mixing with Ruby/Sapphire', 284: 'Evolve', 285: 'Catch', 286: 'Evolve', 287: 'Catch', 288: 'Evolve', 289: 'Evolve', 290: 'Catch', 291: 'Evolve', 292: 'Evolve', 293: 'Catch', 294: 'Catch,Evolve', 295: 'Evolve', 296: 'Catch', 297: 'Catch,Evolve', 298: 'Breed Marill holding Sea Incense', 299: 'Catch', 300: 'Catch', 301: 'Evolve - Only 1 Moon Stone (Delcatty or Wigglytuff)', 302: 'Catch', 303: 'Catch', 304: 'Catch', 305: 'Catch,Evolve', 306: 'Evolve', 307: 'Trade', 308: 'Trade', 309: 'Catch', 310: 'Catch,Evolve', 311: 'Catch, Trade NPC', 312: 'Catch', 313: 'Catch', 314: 'Catch', 315: 'Trade', 316: 'Catch', 317: 'Evolve', 318: 'Catch', 319: 'Catch,Evolve', 320: 'Catch', 321: 'Catch,Evolve', 322: 'Catch', 323: 'Evolve', 324: 'Catch', 325: 'Catch', 326: 'Evolve', 327: 'Catch', 328: 'Catch', 329: 'Evolve', 330: 'Evolve', 331: 'Catch', 332: 'Evolve', 333: 'Catch', 334: 'Catch,Evolve', 335: 'Trade', 336: 'Catch', 337: 'Trade', 338: 'Catch', 339: 'Catch', 340: 'Catch,Evolve', 341: 'Catch', 342: 'Evolve', 343: 'Catch', 344: 'Catch,Evolve', 345: 'Fossil', 346: 'Evolve', 347: 'Fossil', 348: 'Evolve', 349: 'Catch', 350: 'Evolve (High Beauty Level Up)', 351: 'Story Reward', 352: 'Catch', 353: 'Catch', 354: 'Catch', 355: 'Catch', 356: 'Evolve', 357: 'Catch', 358: 'Catch', 359: 'Catch', 360: 'Hatch Gift Egg', 361: 'Catch', 362: 'Evolve', 363: 'Catch', 364: 'Evolve', 365: 'Evolve', 366: 'Catch', 367: 'Trade Evo', 368: 'Trade Evo', 369: 'Catch', 370: 'Catch', 371: 'Catch', 372: 'Evolve', 373: 'Evolve', 374: 'Story Reward', 375: 'Evolve', 376: 'Evolve', 377: 'Catch', 378: 'Catch', 379: 'Catch', 380: 'Catch Roaming (Only one, other is event)', 381: 'Catch Roaming (Only one, other is event)', 382: 'Catch', 383: 'Catch', 384: 'Catch', 385: 'Event', 386: 'Event'}


### functions

def init_dicts_arrays():

	for i in range(256):
		if not i in eng_index:
			eng_index[i]='@'
			continue
		eng_letter[eng_index[i]] = i

	return

def menu(title, menu_items, orientation, left, count):
	print(title)
	print()
	if orientation == 0:
		for i in range(len(menu_items)):
			print(str(i) + '. ', end='')
			if len(menu_items) > 9 and i < 10: print(' ', end='')
			if len(menu_items) > 99 and i < 100: print(' ', end='')
			print(menu_items[i])
	else:
		cols = os.get_terminal_size().columns
		menu_item_len = len(menu_items[1]) + 2 + len(str(len(menu_items))) + 3
		menu_cols = cols // menu_item_len
		menu_lines = len(menu_items) // menu_cols
		if menu_lines * menu_cols < len(menu_items): menu_lines += 1
		format_string = '{:' + str(len(str(len(menu_items)))) +  '}. ' +'{:' + str(len(menu_items[1]) + 3) + '}'
		for i in range(menu_lines):
			for j in range(menu_cols):
				if i + j*menu_lines < len(menu_items):
					print(format_string.format(i + j*menu_lines, menu_items[i + j*menu_lines]), end='')
			print()

	print()
	while True:
		try:
			sel = int(input('Selection: '))
			if sel >= len(menu_items):
				print("\nOut of range. Try again...\n")
				continue
			if left == 0 and sel != 0 and count[sel] == 0:
				print("\nOut of new item space, try again...\n")
				continue
			break
		except ValueError:
			print("\nNot a number. Try again...\n")
		except Exception as err:
			print(f"Unexpected {err=}, {type(err)=}")
			raise
	print()
	return sel

def writeout():
	game_blocks = [0x000000, 0x00E000]

	for block in game_blocks:
		for section in range(14):
			address = block + section * 0x1000
			ck = 0
			for i in range(address,address + 0x0FF4,4): ck += int.from_bytes(sav[i:i+4], byteorder='little')
			ck &= 0xFFFFFFFF
			ck = (ck >> 16) + (ck & 0xFFFF)
			ck &= 0xFFFF
			for i, j in enumerate(ck.to_bytes(2, 'little')): sav[address+0x0FF6+i] = j

	try:
		f = open(outputfilename,'wb')
		f.write(sav)
		f.close()
	except Exception as err:
		print(f"Unexpected {err=}, {type(err)=}")
		raise

	print(outputfilename + "' written out, enjoy!\n")

	return

def dev_dump():
	game_blocks = [0x000000, 0x00E000]

	print('{0:8s} {1:2s} {2:8s} {3:4s} {4:4s} {5:8s} {6:8s}'.format('block','sc','addr','sid','ck','sig','index'))
	for block in game_blocks:
		for section in range(14):
			address = block + section * 0x1000
			sid = int.from_bytes(sav[address+0x0FF4:address+0x0FF4+2], byteorder='little')
			ck = int.from_bytes(sav[address+0x0FF6:address+0x0FF6+2], byteorder='little')
			sig = int.from_bytes(sav[address+0x0FF8:address+0x0FF8+4], byteorder='little')
			index = int.from_bytes(sav[address+0x0FFC:address+0x0FFC+4], byteorder='little')
			print('{0:08x} {1:02d} {2:08x} {3:04x} {4:04x} {5:08x} {6:08x}'.format(block,section,address,sid,ck,sig,index))

	print()

	return

def section_address(s):
	game_blocks = [0x000000, 0x00E000]
	i = 0

	for block in game_blocks:
		for section in range(14):
			address = block + section * 0x1000
			sid = int.from_bytes(sav[address+0x0FF4:address+0x0FF4+2], byteorder='little')
			if sid != s: continue
			index = int.from_bytes(sav[address+0x0FFC:address+0x0FFC+4], byteorder='little')
			if index > i:
				i = index
				a = address

	return(a)

def get_security_key():
	address = section_address(0)
	key = int.from_bytes(sav[address+0x00AC:address+0x00AC+4], byteorder='little')

	return(key)

def items(pocket):
	address = section_address(1)
	key = get_security_key() & 0xFFFF

	sub_sel = -1
	while (sub_sel != 0):
		items_count = {}
		menu_index = {}
		sub_menu = ['Return']
		count = [0] * len(items_index)

		for item in items_name: items_count[item] = 0

		slots = 0
		for i in range(0,max_q[pocket]*4,4):
			item = int.from_bytes(sav[address+offset[pocket]+i:address+offset[pocket]+i+2], byteorder='little')
			if item == 0: break # assume game compacts zeros
			q = int.from_bytes(sav[address+offset[pocket]+i+2:address+offset[pocket]+i+4], byteorder='little')
			if pocket != 'PC_ITEMS': q ^= key
			items_count[item] = q
			slots += 1

		long = 0
		for item in items_name:
			if items_pocket[item] != pocket and pocket != 'PC_ITEMS': continue
			if len(items_name[item]) > long: long = len(items_name[item])

		i = 0
		#for item in items_name:
		for item in dict(sorted(items_name.items(), key=lambda item: item[1])):
			if items_pocket[item] != pocket and pocket != 'PC_ITEMS': continue
			if item == 0: continue
			format_string = '{0:' + str(long) + 's}  {1:2d}'
			s = format_string.format(items_name[item],items_count[item])
			sub_menu.append(s)
			i += 1
			menu_index[i] = item
			count[i] = items_count[item]

		o = 1
		if pocket == 'POKE_BALLS': o = 0
		sub_sel = menu(main_menu[sel] + ' Menu (Select ' + main_menu[sel] + ' to Edit, ' + str(slots) + ' of ' + str(max_q[pocket]) + ' array elements assigned',sub_menu,o,max_q[pocket] - slots,count)

		if sub_sel == 0: break

		while True:
			try:
				q = int(input('Quantity (0-99): '))
				if q > 99 or q < 0:
					print("\nOut of range. Try again...\n")
					continue
				break
			except ValueError:
				print("\nNot a number. Try again...\n")
			except Exception as err:
				print(f"Unexpected {err=}, {type(err)=}")
				raise

		target_item = menu_index[sub_sel]

		# linear search
		for i in range(0,max_q[pocket]*4,4):
			item = int.from_bytes(sav[address+offset[pocket]+i:address+offset[pocket]+i+2], byteorder='little')
			if item == 0: break # assume game compacts zeros
			if target_item == item: break

		# delete
		if q == 0:
			if item == 0: continue # assume game compacts zeros
			for i in range(i,max_q[pocket]*4-4,4):
				for j in range(4):
					sav[address+offset[pocket] + i + j] = sav[address+offset[pocket] + i + j + 4]
			if i != max_q[pocket]*4-4: i += 4
			target_item = 0

		# update/append/delete
		if pocket != 'PC_ITEMS': q ^= key
		for k, j in enumerate(target_item.to_bytes(2, 'little')): sav[address+offset[pocket]+i+k] = j
		for k, j in enumerate(q.to_bytes(2, 'little')): sav[address+offset[pocket]+i+k+2] = j

		print()
	
	return

def sort_items(pocket):
	address = section_address(1)
	key = get_security_key() & 0xFFFF
	items_unsorted_q = {}
	items_unsorted_id = {}
	long = 0

	for i in range(0,max_q[pocket]*4,4):
		item = int.from_bytes(sav[address+offset[pocket]+i:address+offset[pocket]+i+2], byteorder='little')
		if item == 0: break # assume game compacts zeros
		q = int.from_bytes(sav[address+offset[pocket]+i+2:address+offset[pocket]+i+4], byteorder='little')
		if pocket != 'PC_ITEMS': q ^= key
		items_unsorted_q[items_name[item]] = q
		items_unsorted_id[items_name[item]] = item
		if len(items_name[item]) > long: long = len(items_name[item])

	format_string = '{0:' + str(long) + '}  {1:2d}'

	print('Current ' + pocket + ' Order:\n')
	for name in items_unsorted_q:
		print(format_string.format(name,items_unsorted_q[name]))

	print('\nNew ' + pocket + ' Order:\n')
	for i, name in enumerate(dict(sorted(items_unsorted_q.items()))):
		q = items_unsorted_q[name]
		print(format_string.format(name,q))
		if pocket != 'PC_ITEMS': q ^= key
		for k, j in enumerate(items_unsorted_id[name].to_bytes(2, 'little')): sav[address+offset[pocket]+i*4+k] = j
		for k, j in enumerate(q.to_bytes(2, 'little')): sav[address+offset[pocket]+i*4+k+2] = j

	print()

	return

def read_number(address, length, key):
	return(int.from_bytes(sav[address:address+length], byteorder='little') ^ key)

def edit_number(label, address, length, key):
	mx = (2 ** (8 * length)) - 1

	print('Current ' + label + ': ',end='')
	print(read_number(address, length, key))
	print()

	while True:
		try:
			new = int(input('New ' + label + ' range(0-' + str(mx) + '): '))
			if new > mx or new < 0:
				print("\nOut of range. Try again...\n")
				continue
			break
		except ValueError:
			print("\nNot a number. Try again...\n")
		except Exception as err:
			print(f"Unexpected {err=}, {type(err)=}")
			raise

	new ^= key
	for i, j in enumerate(new.to_bytes(length, 'little')): sav[address+i] = j
	print()

	return

def edit_party_names():
	party_size = read_number(section_address(1) + team_size_offset,4,0)

	while True:
		party_list = ['Return']

		for i in range(party_size):
			address = section_address(1) + team_size_offset + 4 + i * 100
			name = address + 0x08
			party_list.append(poketoascii(name,10))

		sel = menu('Select Pokémon to Rename:',party_list,0,1,[])
		if sel == 0: return
		text_edit(section_address(1) + team_size_offset + 4 + (sel - 1) * 100 + 0x08, 10, 'Name')

	return

def text_edit(address, length, label):
	letters = list(eng_index.values())
	letters = [l for l in letters if l != '@']
	allowed = ''.join(letters)
	letters = [l.replace('[', '\\[') for l in letters]
	letters = [l.replace(']', '\\]') for l in letters]
	letters = [l.replace('-', '\\-') for l in letters]

	print('Allowed letters: \n\n' + allowed)
	print('\nUse: + for ♀ (female), ^ for ♂ (male), _ for … (ellipsis)')
	print("\nMax length: " + str(length))
	print('\nCurrent ' + label + ': ',end='')
	print(poketoascii(address,length))
	print()

	while True:
		try:
			new = input('New ' + label + ': ')
			if len(new) == 0:
				print("\nNo Change\n\n")
				return
			if len(new) > length:
				print("\nToo long, max length: " + str(length) + "\n")
				continue
			if not re.match("^[" + "".join(letters) + "]{1," + str(length) + "}$", new):
				print("\nInvalid character(s)\n")
				continue
			break
		except Exception as err:
			print(f"Unexpected {err=}, {type(err)=}")
			raise

	for i in range(len(new)): sav[address+i] = eng_letter[new[i]]
	if i < length - 1:
		sav[address+i+1] = 0xFF
		for i in range(i+2,length): sav[address+i] = 0x0

	print()

	return

def poketoascii(address,length):
	s = ''
	for i in range(length):
		if sav[address+i] == 0xFF: break
		if sav[address+i] == 0x00: break
		s += eng_index[sav[address+i]]
	s = s.replace('+','♀')
	s = s.replace('^','♂')
	s = s.replace('_','…')

	return s

def sort_all(item_types):
	for i in item_types: sort_items(i)
	return

def pokedex(compact):
	address = section_address(0)
	owned  = int.from_bytes(sav[address+pokedex_owned_offset:address+pokedex_owned_offset+49], byteorder='little')
	seen = int.from_bytes(sav[address+pokedex_seen_offset:address+pokedex_seen_offset+49], byteorder='little')
	nid_list = []
	name_list = []

	print("Seen: {0:d} Owned: {1:d}\n".format(seen.bit_count(),owned.bit_count()))

	for nid in dict(nid_index):
		o = s = " "
		if owned & 1: o = pokeball
		if seen & 1: s = "S"
		owned >>= 1
		seen >>= 1
		if compact and o == " " and s == " ": continue
		format_string = '{0:03d}. {1} {2} {3}'
		nid_list.append(format_string.format(nid,s,o,nid_index[nid]))

	name_list = nid_list.copy()
	name_list.sort(key = lambda x: x[9:])

	maxlen = len(max(nid_list, key=len))
	for i,j in zip(nid_list, name_list):
		print("%s\t%s" % (i.ljust(maxlen, " "), j))

	print()
	return

def dump_section_data(s):
	a = section_address(s)
	with open('section.dump', 'wb') as f: f.write(sav[a:a+3968])
	return


### main

init_dicts_arrays()

if len(sys.argv) != 2:
	print("\nUsage: " + sys.argv[0] + " [.sav filename]\n")
	sys.exit(1)

try:
	sav = bytearray(open(sys.argv[1],'rb').read())
except Exception as err:
	print(f"Unexpected {err=}, {type(err)=}")
	raise

game_code = read_number(section_address(1) + 0x00AC,4,0)
if game_code == RUBY_SAPPHIRE or game_code == FIRERED_LEAFGREEN:
	print("\nOnly Emerald Saves Supported.\n")
	sys.exit(1)
game_code = EMERALD

print("\nPokémon Gen III (Emerald only for now) Offline Store v" + version)
print("""
Tested Roms:

c9a195879eae869dff1a87ebe3735342  Pokemon - Emerald Final 7.41 (USA, Europe).gba
605b89b67018abcea91e693a4dd25be3  Pokemon - Emerald Version (USA, Europe).gba
""")
print("USE AT YOUR OWN PERIL!!!\n")
print("Let's go shopping!\n")

sel = -1
while sel != 0:
	menu_array = [
		(
			'Exit (and [over]write "' + outputfilename + '")',
			writeout,
			[]
		),
		(
			'Items',
			items,
			['ITEMS']
		),
		(
			'Sort Items',
			sort_items,
			['ITEMS']
		),
		(
			'Poké Balls',
			items,
			['POKE_BALLS']
		),
		(
			'Sort Poké Balls',
			sort_items,
			['POKE_BALLS']
		),
		(
			'TMs & HMs',
			items,
			['TM_HM']
		),
		(
			'Sort TMs & HMs',
			sort_items,
			['TM_HM']
		),
		(
			'Berries',
			items,
			['BERRIES']
		),
		(
			'Sort Berries',
			sort_items,
			['BERRIES']
		),
		(
			'Key Items',
			items,
			['KEY_ITEMS']
		),
		(
			'Sort Key Items',
			sort_items,
			['KEY_ITEMS']
		),
		(
			'PC Items',
			items,
			['PC_ITEMS']
		),
		(
			'Sort PC Items',
			sort_items,
			['PC_ITEMS']
		),
		(
			'Sort All Items',
			sort_all,
			[['ITEMS','POKE_BALLS','TM_HM','PC_ITEMS','BERRIES','KEY_ITEMS','PC_ITEMS']]
		),
		(
			'Money: ' + str(read_number(section_address(1) + money_offset,4,get_security_key())),
			edit_number,
			['Money',section_address(1) + money_offset,4,get_security_key()]
		),
		(
			'Coins: ' + str(read_number(section_address(1) + coins_offset,2,get_security_key() & 0xFFFF)),
			edit_number,
			['Coins',section_address(1) + coins_offset,2,get_security_key() & 0xFFFF]
		),
		(
			'Soot Sack Steps: ' + str(read_number(section_address(2) + soot_sack_steps_offset,2,0x0)),
			edit_number,
			['Soot Sack Steps',section_address(2) + soot_sack_steps_offset,2,0x0]
		),
		(
			'Edit Party Names',
			edit_party_names,
			[]
		),
		(
			'Pokédex (read-only)',
			pokedex,
			[False]
		),
		(
			'Pokédex Compact (read-only)',
			pokedex,
			[True]
		),
		(
			'[Over]write "' + outputfilename + '" and continue editing',
			writeout,
			[]
		),
		(
			'Abort! (all changes since last write lost)',
			sys.exit,
			[0]
		),
	]

	main_menu = [x[0] for x in menu_array]
	sel = menu('Main Menu',main_menu,0,1,[])
	menu_array[sel][1](*menu_array[sel][2])

sys.exit(0)


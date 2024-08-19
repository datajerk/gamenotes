#!/usr/bin/env python3

import sys
import os
import re
import binascii


### globals

outputfilename = 'newbag.sav'
version = "0.22.0"
money_offset = 0x0490
coins_offset = 0x0494
soot_sack_steps_offset = 0x04AC
team_size_offset = 0x0234
pokedex_owned_offset = 0x0028
pokedex_seen_offset_a = 0x005C
pokedex_seen_offset_b = 0x0988
pokedex_seen_offset_c = 0x0CA4
flags_offset = 0x1270 - 3968
dewford_rand_offset = 0xf68 + 2
mirage_island_offset = 0x464
pokeblocks_offset = 0x848
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

nid_index =  {1: 'Bulbasaur', 2: 'Ivysaur', 3: 'Venusaur', 4: 'Charmander', 5: 'Charmeleon', 6: 'Charizard', 7: 'Squirtle', 8: 'Wartortle', 9: 'Blastoise', 10: 'Caterpie', 11: 'Metapod', 12: 'Butterfree', 13: 'Weedle', 14: 'Kakuna', 15: 'Beedrill', 16: 'Pidgey', 17: 'Pidgeotto', 18: 'Pidgeot', 19: 'Rattata', 20: 'Raticate', 21: 'Spearow', 22: 'Fearow', 23: 'Ekans', 24: 'Arbok', 25: 'Pikachu', 26: 'Raichu', 27: 'Sandshrew', 28: 'Sandslash', 29: 'Nidoran♀', 30: 'Nidorina', 31: 'Nidoqueen', 32: 'Nidoran♂', 33: 'Nidorino', 34: 'Nidoking', 35: 'Clefairy', 36: 'Clefable', 37: 'Vulpix', 38: 'Ninetales', 39: 'Jigglypuff', 40: 'Wigglytuff', 41: 'Zubat', 42: 'Golbat', 43: 'Oddish', 44: 'Gloom', 45: 'Vileplume', 46: 'Paras', 47: 'Parasect', 48: 'Venonat', 49: 'Venomoth', 50: 'Diglett', 51: 'Dugtrio', 52: 'Meowth', 53: 'Persian', 54: 'Psyduck', 55: 'Golduck', 56: 'Mankey', 57: 'Primeape', 58: 'Growlithe', 59: 'Arcanine', 60: 'Poliwag', 61: 'Poliwhirl', 62: 'Poliwrath', 63: 'Abra', 64: 'Kadabra', 65: 'Alakazam', 66: 'Machop', 67: 'Machoke', 68: 'Machamp', 69: 'Bellsprout', 70: 'Weepinbell', 71: 'Victreebel', 72: 'Tentacool', 73: 'Tentacruel', 74: 'Geodude', 75: 'Graveler', 76: 'Golem', 77: 'Ponyta', 78: 'Rapidash', 79: 'Slowpoke', 80: 'Slowbro', 81: 'Magnemite', 82: 'Magneton', 83: 'Farfetchd', 84: 'Doduo', 85: 'Dodrio', 86: 'Seel', 87: 'Dewgong', 88: 'Grimer', 89: 'Muk', 90: 'Shellder', 91: 'Cloyster', 92: 'Gastly', 93: 'Haunter', 94: 'Gengar', 95: 'Onix', 96: 'Drowzee', 97: 'Hypno', 98: 'Krabby', 99: 'Kingler', 100: 'Voltorb', 101: 'Electrode', 102: 'Exeggcute', 103: 'Exeggutor', 104: 'Cubone', 105: 'Marowak', 106: 'Hitmonlee', 107: 'Hitmonchan', 108: 'Lickitung', 109: 'Koffing', 110: 'Weezing', 111: 'Rhyhorn', 112: 'Rhydon', 113: 'Chansey', 114: 'Tangela', 115: 'Kangaskhan', 116: 'Horsea', 117: 'Seadra', 118: 'Goldeen', 119: 'Seaking', 120: 'Staryu', 121: 'Starmie', 122: 'Mr Mime', 123: 'Scyther', 124: 'Jynx', 125: 'Electabuzz', 126: 'Magmar', 127: 'Pinsir', 128: 'Tauros', 129: 'Magikarp', 130: 'Gyarados', 131: 'Lapras', 132: 'Ditto', 133: 'Eevee', 134: 'Vaporeon', 135: 'Jolteon', 136: 'Flareon', 137: 'Porygon', 138: 'Omanyte', 139: 'Omastar', 140: 'Kabuto', 141: 'Kabutops', 142: 'Aerodactyl', 143: 'Snorlax', 144: 'Articuno', 145: 'Zapdos', 146: 'Moltres', 147: 'Dratini', 148: 'Dragonair', 149: 'Dragonite', 150: 'Mewtwo', 151: 'Mew', 152: 'Chikorita', 153: 'Bayleef', 154: 'Meganium', 155: 'Cyndaquil', 156: 'Quilava', 157: 'Typhlosion', 158: 'Totodile', 159: 'Croconaw', 160: 'Feraligatr', 161: 'Sentret', 162: 'Furret', 163: 'Hoothoot', 164: 'Noctowl', 165: 'Ledyba', 166: 'Ledian', 167: 'Spinarak', 168: 'Ariados', 169: 'Crobat', 170: 'Chinchou', 171: 'Lanturn', 172: 'Pichu', 173: 'Cleffa', 174: 'Igglybuff', 175: 'Togepi', 176: 'Togetic', 177: 'Natu', 178: 'Xatu', 179: 'Mareep', 180: 'Flaaffy', 181: 'Ampharos', 182: 'Bellossom', 183: 'Marill', 184: 'Azumarill', 185: 'Sudowoodo', 186: 'Politoed', 187: 'Hoppip', 188: 'Skiploom', 189: 'Jumpluff', 190: 'Aipom', 191: 'Sunkern', 192: 'Sunflora', 193: 'Yanma', 194: 'Wooper', 195: 'Quagsire', 196: 'Espeon', 197: 'Umbreon', 198: 'Murkrow', 199: 'Slowking', 200: 'Misdreavus', 201: 'Unown', 202: 'Wobbuffet', 203: 'Girafarig', 204: 'Pineco', 205: 'Forretress', 206: 'Dunsparce', 207: 'Gligar', 208: 'Steelix', 209: 'Snubbull', 210: 'Granbull', 211: 'Qwilfish', 212: 'Scizor', 213: 'Shuckle', 214: 'Heracross', 215: 'Sneasel', 216: 'Teddiursa', 217: 'Ursaring', 218: 'Slugma', 219: 'Magcargo', 220: 'Swinub', 221: 'Piloswine', 222: 'Corsola', 223: 'Remoraid', 224: 'Octillery', 225: 'Delibird', 226: 'Mantine', 227: 'Skarmory', 228: 'Houndour', 229: 'Houndoom', 230: 'Kingdra', 231: 'Phanpy', 232: 'Donphan', 233: 'Porygon2', 234: 'Stantler', 235: 'Smeargle', 236: 'Tyrogue', 237: 'Hitmontop', 238: 'Smoochum', 239: 'Elekid', 240: 'Magby', 241: 'Miltank', 242: 'Blissey', 243: 'Raikou', 244: 'Entei', 245: 'Suicune', 246: 'Larvitar', 247: 'Pupitar', 248: 'Tyranitar', 249: 'Lugia', 250: 'Ho-Oh', 251: 'Celebi', 252: 'Treecko', 253: 'Grovyle', 254: 'Sceptile', 255: 'Torchic', 256: 'Combusken', 257: 'Blaziken', 258: 'Mudkip', 259: 'Marshtomp', 260: 'Swampert', 261: 'Poochyena', 262: 'Mightyena', 263: 'Zigzagoon', 264: 'Linoone', 265: 'Wurmple', 266: 'Silcoon', 267: 'Beautifly', 268: 'Cascoon', 269: 'Dustox', 270: 'Lotad', 271: 'Lombre', 272: 'Ludicolo', 273: 'Seedot', 274: 'Nuzleaf', 275: 'Shiftry', 276: 'Taillow', 277: 'Swellow', 278: 'Wingull', 279: 'Pelipper', 280: 'Ralts', 281: 'Kirlia', 282: 'Gardevoir', 283: 'Surskit', 284: 'Masquerain', 285: 'Shroomish', 286: 'Breloom', 287: 'Slakoth', 288: 'Vigoroth', 289: 'Slaking', 290: 'Nincada', 291: 'Ninjask', 292: 'Shedinja', 293: 'Whismur', 294: 'Loudred', 295: 'Exploud', 296: 'Makuhita', 297: 'Hariyama', 298: 'Azurill', 299: 'Nosepass', 300: 'Skitty', 301: 'Delcatty', 302: 'Sableye', 303: 'Mawile', 304: 'Aron', 305: 'Lairon', 306: 'Aggron', 307: 'Meditite', 308: 'Medicham', 309: 'Electrike', 310: 'Manectric', 311: 'Plusle', 312: 'Minun', 313: 'Volbeat', 314: 'Illumise', 315: 'Roselia', 316: 'Gulpin', 317: 'Swalot', 318: 'Carvanha', 319: 'Sharpedo', 320: 'Wailmer', 321: 'Wailord', 322: 'Numel', 323: 'Camerupt', 324: 'Torkoal', 325: 'Spoink', 326: 'Grumpig', 327: 'Spinda', 328: 'Trapinch', 329: 'Vibrava', 330: 'Flygon', 331: 'Cacnea', 332: 'Cacturne', 333: 'Swablu', 334: 'Altaria', 335: 'Zangoose', 336: 'Seviper', 337: 'Lunatone', 338: 'Solrock', 339: 'Barboach', 340: 'Whiscash', 341: 'Corphish', 342: 'Crawdaunt', 343: 'Baltoy', 344: 'Claydol', 345: 'Lileep', 346: 'Cradily', 347: 'Anorith', 348: 'Armaldo', 349: 'Feebas', 350: 'Milotic', 351: 'Castform', 352: 'Kecleon', 353: 'Shuppet', 354: 'Banette', 355: 'Duskull', 356: 'Dusclops', 357: 'Tropius', 358: 'Chimecho', 359: 'Absol', 360: 'Wynaut', 361: 'Snorunt', 362: 'Glalie', 363: 'Spheal', 364: 'Sealeo', 365: 'Walrein', 366: 'Clamperl', 367: 'Huntail', 368: 'Gorebyss', 369: 'Relicanth', 370: 'Luvdisc', 371: 'Bagon', 372: 'Shelgon', 373: 'Salamence', 374: 'Beldum', 375: 'Metang', 376: 'Metagross', 377: 'Regirock', 378: 'Regice', 379: 'Registeel', 380: 'Latias', 381: 'Latios', 382: 'Kyogre', 383: 'Groudon', 384: 'Rayquaza', 385: 'Jirachi', 386: 'Deoxys'}

nid_name =  {'Bulbasaur': 1, 'Ivysaur': 2, 'Venusaur': 3, 'Charmander': 4, 'Charmeleon': 5, 'Charizard': 6, 'Squirtle': 7, 'Wartortle': 8, 'Blastoise': 9, 'Caterpie': 10, 'Metapod': 11, 'Butterfree': 12, 'Weedle': 13, 'Kakuna': 14, 'Beedrill': 15, 'Pidgey': 16, 'Pidgeotto': 17, 'Pidgeot': 18, 'Rattata': 19, 'Raticate': 20, 'Spearow': 21, 'Fearow': 22, 'Ekans': 23, 'Arbok': 24, 'Pikachu': 25, 'Raichu': 26, 'Sandshrew': 27, 'Sandslash': 28, 'Nidoran♀': 29, 'Nidorina': 30, 'Nidoqueen': 31, 'Nidoran♂': 32, 'Nidorino': 33, 'Nidoking': 34, 'Clefairy': 35, 'Clefable': 36, 'Vulpix': 37, 'Ninetales': 38, 'Jigglypuff': 39, 'Wigglytuff': 40, 'Zubat': 41, 'Golbat': 42, 'Oddish': 43, 'Gloom': 44, 'Vileplume': 45, 'Paras': 46, 'Parasect': 47, 'Venonat': 48, 'Venomoth': 49, 'Diglett': 50, 'Dugtrio': 51, 'Meowth': 52, 'Persian': 53, 'Psyduck': 54, 'Golduck': 55, 'Mankey': 56, 'Primeape': 57, 'Growlithe': 58, 'Arcanine': 59, 'Poliwag': 60, 'Poliwhirl': 61, 'Poliwrath': 62, 'Abra': 63, 'Kadabra': 64, 'Alakazam': 65, 'Machop': 66, 'Machoke': 67, 'Machamp': 68, 'Bellsprout': 69, 'Weepinbell': 70, 'Victreebel': 71, 'Tentacool': 72, 'Tentacruel': 73, 'Geodude': 74, 'Graveler': 75, 'Golem': 76, 'Ponyta': 77, 'Rapidash': 78, 'Slowpoke': 79, 'Slowbro': 80, 'Magnemite': 81, 'Magneton': 82, 'Farfetchd': 83, 'Doduo': 84, 'Dodrio': 85, 'Seel': 86, 'Dewgong': 87, 'Grimer': 88, 'Muk': 89, 'Shellder': 90, 'Cloyster': 91, 'Gastly': 92, 'Haunter': 93, 'Gengar': 94, 'Onix': 95, 'Drowzee': 96, 'Hypno': 97, 'Krabby': 98, 'Kingler': 99, 'Voltorb': 100, 'Electrode': 101, 'Exeggcute': 102, 'Exeggutor': 103, 'Cubone': 104, 'Marowak': 105, 'Hitmonlee': 106, 'Hitmonchan': 107, 'Lickitung': 108, 'Koffing': 109, 'Weezing': 110, 'Rhyhorn': 111, 'Rhydon': 112, 'Chansey': 113, 'Tangela': 114, 'Kangaskhan': 115, 'Horsea': 116, 'Seadra': 117, 'Goldeen': 118, 'Seaking': 119, 'Staryu': 120, 'Starmie': 121, 'Mr Mime': 122, 'Scyther': 123, 'Jynx': 124, 'Electabuzz': 125, 'Magmar': 126, 'Pinsir': 127, 'Tauros': 128, 'Magikarp': 129, 'Gyarados': 130, 'Lapras': 131, 'Ditto': 132, 'Eevee': 133, 'Vaporeon': 134, 'Jolteon': 135, 'Flareon': 136, 'Porygon': 137, 'Omanyte': 138, 'Omastar': 139, 'Kabuto': 140, 'Kabutops': 141, 'Aerodactyl': 142, 'Snorlax': 143, 'Articuno': 144, 'Zapdos': 145, 'Moltres': 146, 'Dratini': 147, 'Dragonair': 148, 'Dragonite': 149, 'Mewtwo': 150, 'Mew': 151, 'Chikorita': 152, 'Bayleef': 153, 'Meganium': 154, 'Cyndaquil': 155, 'Quilava': 156, 'Typhlosion': 157, 'Totodile': 158, 'Croconaw': 159, 'Feraligatr': 160, 'Sentret': 161, 'Furret': 162, 'Hoothoot': 163, 'Noctowl': 164, 'Ledyba': 165, 'Ledian': 166, 'Spinarak': 167, 'Ariados': 168, 'Crobat': 169, 'Chinchou': 170, 'Lanturn': 171, 'Pichu': 172, 'Cleffa': 173, 'Igglybuff': 174, 'Togepi': 175, 'Togetic': 176, 'Natu': 177, 'Xatu': 178, 'Mareep': 179, 'Flaaffy': 180, 'Ampharos': 181, 'Bellossom': 182, 'Marill': 183, 'Azumarill': 184, 'Sudowoodo': 185, 'Politoed': 186, 'Hoppip': 187, 'Skiploom': 188, 'Jumpluff': 189, 'Aipom': 190, 'Sunkern': 191, 'Sunflora': 192, 'Yanma': 193, 'Wooper': 194, 'Quagsire': 195, 'Espeon': 196, 'Umbreon': 197, 'Murkrow': 198, 'Slowking': 199, 'Misdreavus': 200, 'Unown': 201, 'Wobbuffet': 202, 'Girafarig': 203, 'Pineco': 204, 'Forretress': 205, 'Dunsparce': 206, 'Gligar': 207, 'Steelix': 208, 'Snubbull': 209, 'Granbull': 210, 'Qwilfish': 211, 'Scizor': 212, 'Shuckle': 213, 'Heracross': 214, 'Sneasel': 215, 'Teddiursa': 216, 'Ursaring': 217, 'Slugma': 218, 'Magcargo': 219, 'Swinub': 220, 'Piloswine': 221, 'Corsola': 222, 'Remoraid': 223, 'Octillery': 224, 'Delibird': 225, 'Mantine': 226, 'Skarmory': 227, 'Houndour': 228, 'Houndoom': 229, 'Kingdra': 230, 'Phanpy': 231, 'Donphan': 232, 'Porygon2': 233, 'Stantler': 234, 'Smeargle': 235, 'Tyrogue': 236, 'Hitmontop': 237, 'Smoochum': 238, 'Elekid': 239, 'Magby': 240, 'Miltank': 241, 'Blissey': 242, 'Raikou': 243, 'Entei': 244, 'Suicune': 245, 'Larvitar': 246, 'Pupitar': 247, 'Tyranitar': 248, 'Lugia': 249, 'Ho-Oh': 250, 'Celebi': 251, 'Treecko': 252, 'Grovyle': 253, 'Sceptile': 254, 'Torchic': 255, 'Combusken': 256, 'Blaziken': 257, 'Mudkip': 258, 'Marshtomp': 259, 'Swampert': 260, 'Poochyena': 261, 'Mightyena': 262, 'Zigzagoon': 263, 'Linoone': 264, 'Wurmple': 265, 'Silcoon': 266, 'Beautifly': 267, 'Cascoon': 268, 'Dustox': 269, 'Lotad': 270, 'Lombre': 271, 'Ludicolo': 272, 'Seedot': 273, 'Nuzleaf': 274, 'Shiftry': 275, 'Taillow': 276, 'Swellow': 277, 'Wingull': 278, 'Pelipper': 279, 'Ralts': 280, 'Kirlia': 281, 'Gardevoir': 282, 'Surskit': 283, 'Masquerain': 284, 'Shroomish': 285, 'Breloom': 286, 'Slakoth': 287, 'Vigoroth': 288, 'Slaking': 289, 'Nincada': 290, 'Ninjask': 291, 'Shedinja': 292, 'Whismur': 293, 'Loudred': 294, 'Exploud': 295, 'Makuhita': 296, 'Hariyama': 297, 'Azurill': 298, 'Nosepass': 299, 'Skitty': 300, 'Delcatty': 301, 'Sableye': 302, 'Mawile': 303, 'Aron': 304, 'Lairon': 305, 'Aggron': 306, 'Meditite': 307, 'Medicham': 308, 'Electrike': 309, 'Manectric': 310, 'Plusle': 311, 'Minun': 312, 'Volbeat': 313, 'Illumise': 314, 'Roselia': 315, 'Gulpin': 316, 'Swalot': 317, 'Carvanha': 318, 'Sharpedo': 319, 'Wailmer': 320, 'Wailord': 321, 'Numel': 322, 'Camerupt': 323, 'Torkoal': 324, 'Spoink': 325, 'Grumpig': 326, 'Spinda': 327, 'Trapinch': 328, 'Vibrava': 329, 'Flygon': 330, 'Cacnea': 331, 'Cacturne': 332, 'Swablu': 333, 'Altaria': 334, 'Zangoose': 335, 'Seviper': 336, 'Lunatone': 337, 'Solrock': 338, 'Barboach': 339, 'Whiscash': 340, 'Corphish': 341, 'Crawdaunt': 342, 'Baltoy': 343, 'Claydol': 344, 'Lileep': 345, 'Cradily': 346, 'Anorith': 347, 'Armaldo': 348, 'Feebas': 349, 'Milotic': 350, 'Castform': 351, 'Kecleon': 352, 'Shuppet': 353, 'Banette': 354, 'Duskull': 355, 'Dusclops': 356, 'Tropius': 357, 'Chimecho': 358, 'Absol': 359, 'Wynaut': 360, 'Snorunt': 361, 'Glalie': 362, 'Spheal': 363, 'Sealeo': 364, 'Walrein': 365, 'Clamperl': 366, 'Huntail': 367, 'Gorebyss': 368, 'Relicanth': 369, 'Luvdisc': 370, 'Bagon': 371, 'Shelgon': 372, 'Salamence': 373, 'Beldum': 374, 'Metang': 375, 'Metagross': 376, 'Regirock': 377, 'Regice': 378, 'Registeel': 379, 'Latias': 380, 'Latios': 381, 'Kyogre': 382, 'Groudon': 383, 'Rayquaza': 384, 'Jirachi': 385, 'Deoxys': 386}

nid_obtainable =  {1: 'No', 2: 'No', 3: 'No', 4: 'No', 5: 'No', 6: 'No', 7: 'No', 8: 'No', 9: 'No', 10: 'No', 11: 'No', 12: 'No', 13: 'No', 14: 'No', 15: 'No', 16: 'No', 17: 'No', 18: 'No', 19: 'No', 20: 'No', 21: 'No', 22: 'No', 23: 'No', 24: 'No', 25: 'Yes', 26: 'Yes', 27: 'Yes', 28: 'Yes', 29: 'No', 30: 'No', 31: 'No', 32: 'No', 33: 'No', 34: 'No', 35: 'No', 36: 'No', 37: 'Yes', 38: 'Yes', 39: 'Yes', 40: 'Yes', 41: 'Yes', 42: 'Yes', 43: 'Yes', 44: 'Yes', 45: 'Yes', 46: 'No', 47: 'No', 48: 'No', 49: 'No', 50: 'No', 51: 'No', 52: 'Yes', 53: 'Yes', 54: 'Yes', 55: 'Yes', 56: 'No', 57: 'No', 58: 'No', 59: 'No', 60: 'No', 61: 'No', 62: 'No', 63: 'Yes', 64: 'Yes', 65: 'No', 66: 'Yes', 67: 'Yes', 68: 'No', 69: 'No', 70: 'No', 71: 'No', 72: 'Yes', 73: 'Yes', 74: 'Yes', 75: 'Yes', 76: 'No', 77: 'No', 78: 'No', 79: 'No', 80: 'No', 81: 'Yes', 82: 'Yes', 83: 'No', 84: 'Yes', 85: 'Yes', 86: 'No', 87: 'No', 88: 'Yes', 89: 'Yes', 90: 'No', 91: 'No', 92: 'No', 93: 'No', 94: 'No', 95: 'No', 96: 'No', 97: 'No', 98: 'No', 99: 'No', 100: 'Yes', 101: 'Yes', 102: 'No', 103: 'No', 104: 'No', 105: 'No', 106: 'No', 107: 'No', 108: 'No', 109: 'Yes', 110: 'Yes', 111: 'Yes', 112: 'Yes', 113: 'No', 114: 'No', 115: 'No', 116: 'Yes', 117: 'Yes', 118: 'Yes', 119: 'Yes', 120: 'Yes', 121: 'Yes', 122: 'No', 123: 'No', 124: 'No', 125: 'No', 126: 'No', 127: 'Yes', 128: 'No', 129: 'Yes', 130: 'Yes', 131: 'No', 132: 'Yes', 133: 'No', 134: 'No', 135: 'No', 136: 'No', 137: 'No', 138: 'No', 139: 'No', 140: 'No', 141: 'No', 142: 'No', 143: 'No', 144: 'No', 145: 'No', 146: 'No', 147: 'No', 148: 'No', 149: 'No', 150: 'No', 151: 'No', 152: 'No', 153: 'No', 154: 'No', 155: 'No', 156: 'No', 157: 'No', 158: 'No', 159: 'No', 160: 'No', 161: 'No', 162: 'No', 163: 'Yes', 164: 'Yes', 165: 'Yes', 166: 'Yes', 167: 'Yes', 168: 'Yes', 169: 'Yes', 170: 'Yes', 171: 'Yes', 172: 'Yes', 173: 'No', 174: 'Yes', 175: 'No', 176: 'No', 177: 'Yes', 178: 'Yes', 179: 'Yes', 180: 'Yes', 181: 'Yes', 182: 'Yes', 183: 'Yes', 184: 'Yes', 185: 'Yes', 186: 'No', 187: 'No', 188: 'No', 189: 'No', 190: 'Yes', 191: 'Yes', 192: 'Yes', 193: 'No', 194: 'Yes', 195: 'Yes', 196: 'No', 197: 'No', 198: 'No', 199: 'No', 200: 'No', 201: 'No', 202: 'Yes', 203: 'Yes', 204: 'Yes', 205: 'Yes', 206: 'No', 207: 'Yes', 208: 'No', 209: 'Yes', 210: 'Yes', 211: 'No', 212: 'No', 213: 'Yes', 214: 'Yes', 215: 'No', 216: 'Yes', 217: 'Yes', 218: 'Yes', 219: 'Yes', 220: 'No', 221: 'No', 222: 'Yes', 223: 'Yes', 224: 'Yes', 225: 'No', 226: 'No', 227: 'Yes', 228: 'Yes', 229: 'Yes', 230: 'No', 231: 'Yes', 232: 'Yes', 233: 'No', 234: 'Yes', 235: 'Yes', 236: 'No', 237: 'No', 238: 'No', 239: 'No', 240: 'No', 241: 'Yes', 242: 'No', 243: 'No', 244: 'No', 245: 'No', 246: 'No', 247: 'No', 248: 'No', 249: 'No', 250: 'No', 251: 'No', 252: 'Yes', 253: 'Yes', 254: 'Yes', 255: 'No', 256: 'No', 257: 'No', 258: 'No', 259: 'No', 260: 'No', 261: 'Yes', 262: 'Yes', 263: 'Yes', 264: 'Yes', 265: 'Yes', 266: 'Yes', 267: 'Yes', 268: 'Yes', 269: 'Yes', 270: 'Yes', 271: 'Yes', 272: 'Yes', 273: 'Yes', 274: 'Yes', 275: 'Yes', 276: 'Yes', 277: 'Yes', 278: 'Yes', 279: 'Yes', 280: 'Yes', 281: 'Yes', 282: 'Yes', 283: 'No', 284: 'No', 285: 'Yes', 286: 'Yes', 287: 'Yes', 288: 'Yes', 289: 'Yes', 290: 'Yes', 291: 'Yes', 292: 'Yes', 293: 'Yes', 294: 'Yes', 295: 'Yes', 296: 'Yes', 297: 'Yes', 298: 'Yes', 299: 'Yes', 300: 'Yes', 301: 'No', 302: 'Yes', 303: 'Yes', 304: 'Yes', 305: 'Yes', 306: 'Yes', 307: 'No', 308: 'No', 309: 'Yes', 310: 'Yes', 311: 'Yes', 312: 'Yes', 313: 'Yes', 314: 'Yes', 315: 'No', 316: 'Yes', 317: 'Yes', 318: 'Yes', 319: 'Yes', 320: 'Yes', 321: 'Yes', 322: 'Yes', 323: 'Yes', 324: 'Yes', 325: 'Yes', 326: 'Yes', 327: 'Yes', 328: 'Yes', 329: 'Yes', 330: 'Yes', 331: 'Yes', 332: 'Yes', 333: 'Yes', 334: 'Yes', 335: 'No', 336: 'Yes', 337: 'No', 338: 'Yes', 339: 'Yes', 340: 'Yes', 341: 'Yes', 342: 'Yes', 343: 'Yes', 344: 'Yes', 345: 'Yes', 346: 'Yes', 347: 'Yes', 348: 'Yes', 349: 'Yes', 350: 'Yes', 351: 'Yes', 352: 'Yes', 353: 'Yes', 354: 'Yes', 355: 'Yes', 356: 'Yes', 357: 'Yes', 358: 'Yes', 359: 'Yes', 360: 'Yes', 361: 'Yes', 362: 'Yes', 363: 'Yes', 364: 'Yes', 365: 'Yes', 366: 'Yes', 367: 'No', 368: 'No', 369: 'Yes', 370: 'Yes', 371: 'Yes', 372: 'Yes', 373: 'Yes', 374: 'Yes', 375: 'Yes', 376: 'Yes', 377: 'Yes', 378: 'Yes', 379: 'Yes', 380: 'Yes', 381: 'Yes', 382: 'Yes', 383: 'Yes', 384: 'Yes', 385: 'No', 386: 'No'}

nid_method =  {1: 'Trade', 2: 'Trade', 3: 'Trade', 4: 'Trade', 5: 'Trade', 6: 'Trade', 7: 'Trade', 8: 'Trade', 9: 'Trade', 10: 'Trade', 11: 'Trade', 12: 'Trade', 13: 'Trade', 14: 'Trade', 15: 'Trade', 16: 'Trade', 17: 'Trade', 18: 'Trade', 19: 'Trade', 20: 'Trade', 21: 'Trade', 22: 'Trade', 23: 'Trade', 24: 'Trade', 25: 'Catch', 26: 'Evolve', 27: 'Catch', 28: 'Evolve', 29: 'Trade', 30: 'Trade', 31: 'Trade', 32: 'Trade', 33: 'Trade', 34: 'Trade', 35: 'Trade', 36: 'Trade', 37: 'Catch', 38: 'Evolve', 39: 'Catch', 40: 'Evolve - Only 1 Moon Stone (Delcatty or Wigglytuff)', 41: 'Catch', 42: 'Catch,Evolve', 43: 'Catch', 44: 'Catch,Evolve', 45: 'Evolve', 46: 'Trade', 47: 'Trade', 48: 'Trade', 49: 'Trade', 50: 'Trade', 51: 'Trade', 52: 'Trade NPC', 53: 'Evolve', 54: 'Catch', 55: 'Catch,Evolve', 56: 'Trade', 57: 'Trade', 58: 'Trade', 59: 'Trade', 60: 'Trade', 61: 'Trade', 62: 'Trade', 63: 'Catch', 64: 'Evolve', 65: 'Trade Evo', 66: 'Catch', 67: 'Evolve', 68: 'Trade Evo', 69: 'Trade', 70: 'Trade', 71: 'Trade', 72: 'Catch', 73: 'Catch,Evolve', 74: 'Catch', 75: 'Catch,Evolve', 76: 'Trade Evo', 77: 'Trade', 78: 'Trade', 79: 'Trade', 80: 'Trade', 81: 'Catch', 82: 'Catch,Evolve', 83: 'Trade', 84: 'Catch', 85: 'Catch,Evolve', 86: 'Trade', 87: 'Trade', 88: 'Catch', 89: 'Evolve', 90: 'Trade', 91: 'Trade', 92: 'Trade', 93: 'Trade', 94: 'Trade', 95: 'Trade', 96: 'Trade', 97: 'Trade', 98: 'Trade', 99: 'Trade', 100: 'Catch', 101: 'Catch,Evolve', 102: 'Trade', 103: 'Trade', 104: 'Trade', 105: 'Trade', 106: 'Trade', 107: 'Trade', 108: 'Trade', 109: 'Catch', 110: 'Evolve', 111: 'Catch', 112: 'Evolve', 113: 'Trade', 114: 'Trade', 115: 'Trade', 116: 'Catch', 117: 'Evolve', 118: 'Catch', 119: 'Catch,Evolve', 120: 'Catch', 121: 'Evolve', 122: 'Trade', 123: 'Trade', 124: 'Trade', 125: 'Trade', 126: 'Trade', 127: 'Catch', 128: 'Trade', 129: 'Catch', 130: 'Catch,Evolve', 131: 'Trade', 132: 'Catch', 133: 'Trade', 134: 'Trade', 135: 'Trade', 136: 'Trade', 137: 'Trade', 138: 'Trade', 139: 'Trade', 140: 'Trade', 141: 'Trade', 142: 'Trade', 143: 'Trade', 144: 'Trade', 145: 'Trade', 146: 'Trade', 147: 'Trade', 148: 'Trade', 149: 'Trade', 150: 'Trade', 151: 'Event Item required (Japan only)', 152: 'Trade, Complete Regional Dex', 153: 'Trade', 154: 'Trade', 155: 'Trade, Complete Regional Dex', 156: 'Trade', 157: 'Trade', 158: 'Trade, Complete Regional Dex', 159: 'Trade', 160: 'Trade', 161: 'Trade', 162: 'Trade', 163: 'Catch', 164: 'Evolve', 165: 'Catch', 166: 'Evolve', 167: 'Catch', 168: 'Evolve', 169: 'Evolve', 170: 'Catch', 171: 'Evolve', 172: 'Breed', 173: 'Trade', 174: 'Breed', 175: 'Trade', 176: 'Trade', 177: 'Catch', 178: 'Catch,Evolve', 179: 'Catch', 180: 'Evolve', 181: 'Evolve', 182: 'Evolve', 183: 'Catch', 184: 'Evolve', 185: 'Catch', 186: 'Trade,Trade Evo', 187: 'Trade', 188: 'Trade', 189: 'Trade', 190: 'Catch', 191: 'Catch', 192: 'Evolve', 193: 'Trade', 194: 'Catch', 195: 'Catch,Evolve', 196: 'Trade', 197: 'Trade', 198: 'Trade', 199: 'Trade', 200: 'Trade', 201: 'Trade', 202: 'Catch', 203: 'Catch', 204: 'Catch', 205: 'Evolve', 206: 'Trade', 207: 'Catch', 208: 'Trade', 209: 'Catch', 210: 'Evolve', 211: 'Trade', 212: 'Trade', 213: 'Catch', 214: 'Catch', 215: 'Trade', 216: 'Catch', 217: 'Evolve', 218: 'Catch', 219: 'Evolve', 220: 'Trade', 221: 'Trade', 222: 'Catch', 223: 'Catch', 224: 'Catch,Evolve', 225: 'Trade', 226: 'Trade', 227: 'Catch', 228: 'Catch', 229: 'Evolve', 230: 'Trade Evo', 231: 'Catch', 232: 'Evolve', 233: 'Trade,Trade Evo', 234: 'Catch', 235: 'Catch', 236: 'Trade', 237: 'Trade', 238: 'Trade', 239: 'Trade', 240: 'Trade', 241: 'Catch', 242: 'Trade', 243: 'Trade', 244: 'Trade', 245: 'Trade', 246: 'Trade', 247: 'Trade', 248: 'Trade', 249: 'Event Item required', 250: 'Event Item required', 251: 'Trade, Event', 252: 'Starter - 1 evo line only', 253: 'Starter - 1 evo line only', 254: 'Starter - 1 evo line only', 255: 'Starter - 1 evo line only', 256: 'Starter - 1 evo line only', 257: 'Starter - 1 evo line only', 258: 'Starter - 1 evo line only', 259: 'Starter - 1 evo line only', 260: 'Starter - 1 evo line only', 261: 'Catch', 262: 'Catch,Evolve', 263: 'Catch', 264: 'Catch,Evolve', 265: 'Catch', 266: 'Catch,Evolve', 267: 'Evolve', 268: 'Catch,Evolve', 269: 'Evolve', 270: 'Catch', 271: 'Catch,Evolve', 272: 'Evolve', 273: 'Catch', 274: 'Catch,Evolve', 275: 'Evolve', 276: 'Catch', 277: 'Catch,Evolve', 278: 'Catch', 279: 'Catch,Evolve', 280: 'Catch', 281: 'Evolve', 282: 'Evolve', 283: 'Swarm - Only after record mixing with Ruby/Sapphire', 284: 'Evolve', 285: 'Catch', 286: 'Evolve', 287: 'Catch', 288: 'Evolve', 289: 'Evolve', 290: 'Catch', 291: 'Evolve', 292: 'Evolve', 293: 'Catch', 294: 'Catch,Evolve', 295: 'Evolve', 296: 'Catch', 297: 'Catch,Evolve', 298: 'Breed Marill holding Sea Incense', 299: 'Catch', 300: 'Catch', 301: 'Evolve - Only 1 Moon Stone (Delcatty or Wigglytuff)', 302: 'Catch', 303: 'Catch', 304: 'Catch', 305: 'Catch,Evolve', 306: 'Evolve', 307: 'Trade', 308: 'Trade', 309: 'Catch', 310: 'Catch,Evolve', 311: 'Catch, Trade NPC', 312: 'Catch', 313: 'Catch', 314: 'Catch', 315: 'Trade', 316: 'Catch', 317: 'Evolve', 318: 'Catch', 319: 'Catch,Evolve', 320: 'Catch', 321: 'Catch,Evolve', 322: 'Catch', 323: 'Evolve', 324: 'Catch', 325: 'Catch', 326: 'Evolve', 327: 'Catch', 328: 'Catch', 329: 'Evolve', 330: 'Evolve', 331: 'Catch', 332: 'Evolve', 333: 'Catch', 334: 'Catch,Evolve', 335: 'Trade', 336: 'Catch', 337: 'Trade', 338: 'Catch', 339: 'Catch', 340: 'Catch,Evolve', 341: 'Catch', 342: 'Evolve', 343: 'Catch', 344: 'Catch,Evolve', 345: 'Fossil', 346: 'Evolve', 347: 'Fossil', 348: 'Evolve', 349: 'Catch', 350: 'Evolve (High Beauty Level Up)', 351: 'Story Reward', 352: 'Catch', 353: 'Catch', 354: 'Catch', 355: 'Catch', 356: 'Evolve', 357: 'Catch', 358: 'Catch', 359: 'Catch', 360: 'Hatch Gift Egg', 361: 'Catch', 362: 'Evolve', 363: 'Catch', 364: 'Evolve', 365: 'Evolve', 366: 'Catch', 367: 'Trade Evo', 368: 'Trade Evo', 369: 'Catch', 370: 'Catch', 371: 'Catch', 372: 'Evolve', 373: 'Evolve', 374: 'Story Reward', 375: 'Evolve', 376: 'Evolve', 377: 'Catch', 378: 'Catch', 379: 'Catch', 380: 'Catch Roaming (Only one, other is event)', 381: 'Catch Roaming (Only one, other is event)', 382: 'Catch', 383: 'Catch', 384: 'Catch', 385: 'Event', 386: 'Event'}

flags = {0: '_UNUSED', 1: 'TEMP_SKIP_GABBY_INTERVIEW', 2: 'TEMP_REGICE_PUZZLE_STARTED', 3: 'TEMP_REGICE_PUZZLE_FAILED', 4: 'TEMP_4', 5: 'TEMP_5', 6: 'TEMP_6', 7: 'TEMP_7', 8: 'TEMP_8', 9: 'TEMP_9', 10: 'TEMP_A', 11: 'TEMP_B', 12: 'TEMP_C', 13: 'TEMP_D', 14: 'TEMP_E', 15: 'TEMP_F', 16: 'TEMP_10', 17: 'TEMP_HIDE_MIRAGE_ISLAND_BERRY_TREE', 18: 'TEMP_12', 19: 'TEMP_13', 20: 'TEMP_14', 21: 'TEMP_15', 22: 'TEMP_16', 23: 'TEMP_17', 24: 'TEMP_18', 25: 'TEMP_19', 26: 'TEMP_1A', 27: 'TEMP_1B', 28: 'TEMP_1C', 29: 'TEMP_1D', 30: 'TEMP_1E', 31: 'TEMP_1F', 32: '_UNUSED', 33: '_UNUSED', 34: '_UNUSED', 35: '_UNUSED', 36: '_UNUSED', 37: '_UNUSED', 38: '_UNUSED', 39: '_UNUSED', 40: '_UNUSED', 41: '_UNUSED', 42: '_UNUSED', 43: '_UNUSED', 44: '_UNUSED', 45: '_UNUSED', 46: '_UNUSED', 47: '_UNUSED', 48: '_UNUSED', 49: '_UNUSED', 50: '_UNUSED', 51: '_UNUSED', 52: '_UNUSED', 53: '_UNUSED', 54: '_UNUSED', 55: '_UNUSED', 56: '_UNUSED', 57: '_UNUSED', 58: '_UNUSED', 59: '_UNUSED', 60: '_UNUSED', 61: '_UNUSED', 62: '_UNUSED', 63: '_UNUSED', 64: '_UNUSED', 65: '_UNUSED', 66: '_UNUSED', 67: '_UNUSED', 68: '_UNUSED', 69: '_UNUSED', 70: '_UNUSED', 71: '_UNUSED', 72: '_UNUSED', 73: '_UNUSED', 74: '_UNUSED', 75: '_UNUSED', 76: '_UNUSED', 77: '_UNUSED', 78: '_UNUSED', 79: '_UNUSED', 80: 'HIDE_SKY_PILLAR_TOP_RAYQUAZA_STILL', 81: 'SET_WALL_CLOCK', 82: 'RESCUED_BIRCH', 83: 'LEGENDARIES_IN_SOOTOPOLIS', 84: '_UNUSED', 85: '_UNUSED', 86: 'HIDE_CONTEST_POKE_BALL', 87: 'MET_RIVAL_MOM', 88: 'BIRCH_AIDE_MET', 89: 'DECLINED_BIKE', 90: 'RECEIVED_BIKE', 91: 'WATTSON_REMATCH_AVAILABLE', 92: 'COLLECTED_ALL_SILVER_SYMBOLS', 93: 'GOOD_LUCK_SAFARI_ZONE', 94: 'RECEIVED_WAILMER_PAIL', 95: 'RECEIVED_POKEBLOCK_CASE', 96: 'RECEIVED_SECRET_POWER', 97: 'MET_TEAM_AQUA_HARBOR', 98: 'TV_EXPLAINED', 99: 'MAUVILLE_GYM_BARRIERS_STATE', 100: '_UNUSED', 101: '_UNUSED', 102: '_UNUSED', 103: '_UNUSED', 104: '_UNUSED', 105: 'OCEANIC_MUSEUM_MET_REPORTER', 106: 'RECEIVED_HM04', 107: 'RECEIVED_HM06', 108: 'WHITEOUT_TO_LAVARIDGE', 109: 'RECEIVED_HM05', 110: 'RECEIVED_HM02', 111: 'GROUDON_AWAKENED_MAGMA_HIDEOUT', 112: 'TEAM_AQUA_ESCAPED_IN_SUBMARINE', 113: '_UNUSED', 114: 'SCOTT_CALL_BATTLE_FRONTIER', 115: 'RECEIVED_METEORITE', 116: 'ADVENTURE_STARTED', 117: 'DEFEATED_MAGMA_SPACE_CENTER', 118: 'MET_HIDDEN_POWER_GIVER', 119: 'CANCEL_BATTLE_ROOM_CHALLENGE', 120: 'LANDMARK_MIRAGE_TOWER', 121: 'RECEIVED_TM31', 122: 'RECEIVED_HM03', 123: 'RECEIVED_HM08', 124: 'REGISTER_RIVAL_POKENAV', 125: 'DEFEATED_RIVAL_ROUTE_104', 126: 'DEFEATED_WALLY_VICTORY_ROAD', 127: 'MET_PRETTY_PETAL_SHOP_OWNER', 128: 'ENABLE_ROXANNE_FIRST_CALL', 129: 'KYOGRE_ESCAPED_SEAFLOOR_CAVERN', 130: 'DEFEATED_RIVAL_ROUTE103', 131: 'RECEIVED_DOLL_LANETTE', 132: 'RECEIVED_POTION_OLDALE', 133: 'RECEIVED_AMULET_COIN', 134: 'PENDING_DAYCARE_EGG', 135: 'THANKED_FOR_PLAYING_WITH_WALLY', 136: 'ENABLE_FIRST_WALLY_POKENAV_CALL', 137: 'RECEIVED_HM01', 138: 'SCOTT_CALL_FORTREE_GYM', 139: 'DEFEATED_EVIL_TEAM_MT_CHIMNEY', 140: 'RECEIVED_6_SODA_POP', 141: 'DEFEATED_SEASHORE_HOUSE', 142: 'DEVON_GOODS_STOLEN', 143: 'RECOVERED_DEVON_GOODS', 144: 'RETURNED_DEVON_GOODS', 145: 'CAUGHT_LUGIA', 146: 'CAUGHT_HO_OH', 147: 'MR_BRINEY_SAILING_INTRO', 148: 'DOCK_REJECTED_DEVON_GOODS', 149: 'DELIVERED_DEVON_GOODS', 150: '_UNUSED', 151: 'RECEIVED_CASTFORM', 152: 'RECEIVED_SUPER_ROD', 153: 'RUSTBORO_NPC_TRADE_COMPLETED', 154: 'PACIFIDLOG_NPC_TRADE_COMPLETED', 155: 'FORTREE_NPC_TRADE_COMPLETED', 156: 'BATTLE_FRONTIER_TRADE_DONE', 157: 'FORCE_MIRAGE_TOWER_VISIBLE', 158: 'SOOTOPOLIS_ARCHIE_MAXIE_LEAVE', 159: 'INTERACTED_WITH_DEVON_EMPLOYEE_GOODS_STOLEN', 160: 'COOL_PAINTING_MADE', 161: 'BEAUTY_PAINTING_MADE', 162: 'CUTE_PAINTING_MADE', 163: 'SMART_PAINTING_MADE', 164: 'TOUGH_PAINTING_MADE', 165: 'RECEIVED_TM39', 166: 'RECEIVED_TM08', 167: 'RECEIVED_TM34', 168: 'RECEIVED_TM50', 169: 'RECEIVED_TM42', 170: 'RECEIVED_TM40', 171: 'RECEIVED_TM04', 172: 'RECEIVED_TM03', 173: 'DECORATION_0', 174: 'DECORATION_1', 175: 'DECORATION_2', 176: 'DECORATION_3', 177: 'DECORATION_4', 178: 'DECORATION_5', 179: 'DECORATION_6', 180: 'DECORATION_7', 181: 'DECORATION_8', 182: 'DECORATION_9', 183: 'DECORATION_10', 184: 'DECORATION_11', 185: 'DECORATION_12', 186: 'DECORATION_13', 187: 'DECORATION_14', 188: 'RECEIVED_POKENAV', 189: 'DELIVERED_STEVEN_LETTER', 190: 'DEFEATED_WALLY_MAUVILLE', 191: 'DEFEATED_GRUNT_SPACE_CENTER_1F', 192: 'RECEIVED_SUN_STONE_MOSSDEEP', 193: 'WALLY_SPEECH', 194: '_UNUSED', 195: '_UNUSED', 196: '_UNUSED', 197: '_UNUSED', 198: '_UNUSED', 199: 'RUSTURF_TUNNEL_OPENED', 200: 'RECEIVED_RED_SCARF', 201: 'RECEIVED_BLUE_SCARF', 202: 'RECEIVED_PINK_SCARF', 203: 'RECEIVED_GREEN_SCARF', 204: 'RECEIVED_YELLOW_SCARF', 205: 'INTERACTED_WITH_STEVEN_SPACE_CENTER', 206: 'ENCOUNTERED_LATIAS_OR_LATIOS', 207: 'MET_ARCHIE_METEOR_FALLS', 208: 'GOT_BASEMENT_KEY_FROM_WATTSON', 209: 'GOT_TM24_FROM_WATTSON', 210: 'FAN_CLUB_STRENGTH_SHARED', 211: 'DEFEATED_RIVAL_RUSTBORO', 212: 'RECEIVED_RED_OR_BLUE_ORB', 213: 'RECEIVED_PREMIER_BALL_RUSTBORO', 214: 'ENABLE_WALLY_MATCH_CALL', 215: 'ENABLE_SCOTT_MATCH_CALL', 216: 'ENABLE_MOM_MATCH_CALL', 217: 'MET_DIVING_TREASURE_HUNTER', 218: 'MET_WAILMER_TRAINER', 219: 'EVIL_LEADER_PLEASE_STOP', 220: 'NEVER_SET_0x0DC', 221: 'RECEIVED_GO_GOGGLES', 222: 'WINGULL_SENT_ON_ERRAND', 223: 'RECEIVED_MENTAL_HERB', 224: 'WINGULL_DELIVERED_MAIL', 225: 'RECEIVED_20_COINS', 226: 'RECEIVED_STARTER_DOLL', 227: 'RECEIVED_GOOD_ROD', 228: 'REGI_DOORS_OPENED', 229: 'RECEIVED_TM27', 230: 'RECEIVED_TM36', 231: 'RECEIVED_TM05', 232: 'RECEIVED_TM19', 233: '_UNUSED', 234: 'RECEIVED_TM44', 235: 'RECEIVED_TM45', 236: 'RECEIVED_GLASS_ORNAMENT', 237: 'RECEIVED_SILVER_SHIELD', 238: 'RECEIVED_GOLD_SHIELD', 239: 'USED_STORAGE_KEY', 240: 'USED_ROOM_1_KEY', 241: 'USED_ROOM_2_KEY', 242: 'USED_ROOM_4_KEY', 243: 'USED_ROOM_6_KEY', 244: 'MET_PROF_COZMO', 245: 'RECEIVED_WAILMER_DOLL', 246: 'RECEIVED_CHESTO_BERRY_ROUTE_104', 247: 'DEFEATED_SS_TIDAL_TRAINERS', 248: 'RECEIVED_SPELON_BERRY', 249: 'RECEIVED_PAMTRE_BERRY', 250: 'RECEIVED_WATMEL_BERRY', 251: 'RECEIVED_DURIN_BERRY', 252: 'RECEIVED_BELUE_BERRY', 253: 'ENABLE_RIVAL_MATCH_CALL', 254: 'RECEIVED_CHARCOAL', 255: 'LATIOS_OR_LATIAS_ROAMING', 256: 'RECEIVED_REPEAT_BALL', 257: 'RECEIVED_OLD_ROD', 258: 'RECEIVED_COIN_CASE', 259: 'RETURNED_RED_OR_BLUE_ORB', 260: 'RECEIVED_TM49', 261: 'RECEIVED_TM28', 262: 'RECEIVED_TM09', 263: 'ENTERED_ELITE_FOUR', 264: 'RECEIVED_TM10', 265: 'RECEIVED_TM41', 266: 'RECEIVED_LAVARIDGE_EGG', 267: 'RECEIVED_REVIVED_FOSSIL_MON', 268: 'SECRET_BASE_REGISTRY_ENABLED', 269: 'RECEIVED_TM46', 270: 'CONTEST_SKETCH_CREATED', 271: 'EVIL_TEAM_ESCAPED_STERN_SPOKE', 272: 'RECEIVED_EXP_SHARE', 273: 'POKERUS_EXPLAINED', 274: 'RECEIVED_RUNNING_SHOES', 275: 'RECEIVED_QUICK_CLAW', 276: 'RECEIVED_KINGS_ROCK', 277: 'RECEIVED_MACHO_BRACE', 278: 'RECEIVED_SOOTHE_BELL', 279: 'RECEIVED_WHITE_HERB', 280: 'RECEIVED_SOFT_SAND', 281: 'ENABLE_PROF_BIRCH_MATCH_CALL', 282: 'RECEIVED_CLEANSE_TAG', 283: 'RECEIVED_FOCUS_BAND', 284: 'DECLINED_WALLY_BATTLE_MAUVILLE', 285: 'RECEIVED_DEVON_SCOPE', 286: 'DECLINED_RIVAL_BATTLE_LILYCOVE', 287: 'MET_DEVON_EMPLOYEE', 288: 'MET_RIVAL_RUSTBORO', 289: 'RECEIVED_SILK_SCARF', 290: 'NOT_READY_FOR_BATTLE_ROUTE_120', 291: 'RECEIVED_SS_TICKET', 292: 'MET_RIVAL_LILYCOVE', 293: 'MET_RIVAL_IN_HOUSE_AFTER_LILYCOVE', 294: 'EXCHANGED_SCANNER', 295: 'KECLEON_FLED_FORTREE', 296: 'PETALBURG_MART_EXPANDED_ITEMS', 297: 'RECEIVED_MIRACLE_SEED', 298: 'RECEIVED_BELDUM', 299: 'RECEIVED_FANCLUB_TM_THIS_WEEK', 300: 'MET_FANCLUB_YOUNGER_BROTHER', 301: 'RIVAL_LEFT_FOR_ROUTE103', 302: 'OMIT_DIVE_FROM_STEVEN_LETTER', 303: 'HAS_MATCH_CALL', 304: 'ADDED_MATCH_CALL_TO_POKENAV', 305: 'REGISTERED_STEVEN_POKENAV', 306: 'ENABLE_NORMAN_MATCH_CALL', 307: 'STEVEN_GUIDES_TO_CAVE_OF_ORIGIN', 308: 'MET_ARCHIE_SOOTOPOLIS', 309: 'MET_MAXIE_SOOTOPOLIS', 310: 'MET_SCOTT_RUSTBORO', 311: 'WALLACE_GOES_TO_SKY_PILLAR', 312: 'RECEIVED_HM07', 313: 'BEAT_MAGMA_GRUNT_JAGGED_PASS', 314: 'RECEIVED_AURORA_TICKET', 315: 'RECEIVED_MYSTIC_TICKET', 316: 'RECEIVED_OLD_SEA_MAP', 317: 'WONDER_CARD_UNUSED_1', 318: 'WONDER_CARD_UNUSED_2', 319: 'WONDER_CARD_UNUSED_3', 320: 'WONDER_CARD_UNUSED_4', 321: 'WONDER_CARD_UNUSED_5', 322: 'WONDER_CARD_UNUSED_6', 323: 'WONDER_CARD_UNUSED_7', 324: 'WONDER_CARD_UNUSED_8', 325: 'WONDER_CARD_UNUSED_9', 326: 'WONDER_CARD_UNUSED_10', 327: 'WONDER_CARD_UNUSED_11', 328: 'WONDER_CARD_UNUSED_12', 329: 'WONDER_CARD_UNUSED_13', 330: 'WONDER_CARD_UNUSED_14', 331: 'WONDER_CARD_UNUSED_15', 332: 'WONDER_CARD_UNUSED_16', 333: 'WONDER_CARD_UNUSED_17', 334: 'MIRAGE_TOWER_VISIBLE', 335: 'CHOSE_ROOT_FOSSIL', 336: 'CHOSE_CLAW_FOSSIL', 337: 'RECEIVED_POWDER_JAR', 338: 'CHOSEN_MULTI_BATTLE_NPC_PARTNER', 339: 'MET_BATTLE_FRONTIER_BREEDER', 340: 'MET_BATTLE_FRONTIER_MANIAC', 341: 'ENTERED_CONTEST', 342: 'MET_SLATEPORT_FANCLUB_CHAIRMAN', 343: 'MET_BATTLE_FRONTIER_GAMBLER', 344: 'ENABLE_MR_STONE_POKENAV', 345: 'NURSE_MENTIONS_GOLD_CARD', 346: 'MET_FRONTIER_BEAUTY_MOVE_TUTOR', 347: 'MET_FRONTIER_SWIMMER_MOVE_TUTOR', 348: 'MATCH_CALL_REGISTERED', 349: 'REMATCH_ROSE', 350: 'REMATCH_ANDRES', 351: 'REMATCH_DUSTY', 352: 'REMATCH_LOLA', 353: 'REMATCH_RICKY', 354: 'REMATCH_LILA_AND_ROY', 355: 'REMATCH_CRISTIN', 356: 'REMATCH_BROOKE', 357: 'REMATCH_WILTON', 358: 'REMATCH_VALERIE', 359: 'REMATCH_CINDY', 360: 'REMATCH_THALIA', 361: 'REMATCH_JESSICA', 362: 'REMATCH_WINSTON', 363: 'REMATCH_STEVE', 364: 'REMATCH_TONY', 365: 'REMATCH_NOB', 366: 'REMATCH_KOJI', 367: 'REMATCH_FERNANDO', 368: 'REMATCH_DALTON', 369: 'REMATCH_BERNIE', 370: 'REMATCH_ETHAN', 371: 'REMATCH_JOHN_AND_JAY', 372: 'REMATCH_JEFFREY', 373: 'REMATCH_CAMERON', 374: 'REMATCH_JACKI', 375: 'REMATCH_WALTER', 376: 'REMATCH_KAREN', 377: 'REMATCH_JERRY', 378: 'REMATCH_ANNA_AND_MEG', 379: 'REMATCH_ISABEL', 380: 'REMATCH_MIGUEL', 381: 'REMATCH_TIMOTHY', 382: 'REMATCH_SHELBY', 383: 'REMATCH_CALVIN', 384: 'REMATCH_ELLIOT', 385: 'REMATCH_ISAIAH', 386: 'REMATCH_MARIA', 387: 'REMATCH_ABIGAIL', 388: 'REMATCH_DYLAN', 389: 'REMATCH_KATELYN', 390: 'REMATCH_BENJAMIN', 391: 'REMATCH_PABLO', 392: 'REMATCH_NICOLAS', 393: 'REMATCH_ROBERT', 394: 'REMATCH_LAO', 395: 'REMATCH_CYNDY', 396: 'REMATCH_MADELINE', 397: 'REMATCH_JENNY', 398: 'REMATCH_DIANA', 399: 'REMATCH_AMY_AND_LIV', 400: 'REMATCH_ERNEST', 401: 'REMATCH_CORY', 402: 'REMATCH_EDWIN', 403: 'REMATCH_LYDIA', 404: 'REMATCH_ISAAC', 405: 'REMATCH_GABRIELLE', 406: 'REMATCH_CATHERINE', 407: 'REMATCH_JACKSON', 408: 'REMATCH_HALEY', 409: 'REMATCH_JAMES', 410: 'REMATCH_TRENT', 411: 'REMATCH_SAWYER', 412: 'REMATCH_KIRA_AND_DAN', 413: 'REMATCH_WALLY', 414: 'REMATCH_ROXANNE', 415: 'REMATCH_BRAWLY', 416: 'REMATCH_WATTSON', 417: 'REMATCH_FLANNERY', 418: 'REMATCH_NORMAN', 419: 'REMATCH_WINONA', 420: 'REMATCH_TATE_AND_LIZA', 421: 'REMATCH_SIDNEY', 422: 'REMATCH_PHOEBE', 423: 'REMATCH_GLACIA', 424: 'REMATCH_DRAKE', 425: 'REMATCH_WALLACE', 426: '_UNUSED', 427: '_UNUSED', 428: 'DEFEATED_DEOXYS', 429: 'BATTLED_DEOXYS', 430: 'SHOWN_EON_TICKET', 431: 'SHOWN_AURORA_TICKET', 432: 'SHOWN_OLD_SEA_MAP', 433: 'MOVE_TUTOR_TAUGHT_SWAGGER', 434: 'MOVE_TUTOR_TAUGHT_ROLLOUT', 435: 'MOVE_TUTOR_TAUGHT_FURY_CUTTER', 436: 'MOVE_TUTOR_TAUGHT_MIMIC', 437: 'MOVE_TUTOR_TAUGHT_METRONOME', 438: 'MOVE_TUTOR_TAUGHT_SLEEP_TALK', 439: 'MOVE_TUTOR_TAUGHT_SUBSTITUTE', 440: 'MOVE_TUTOR_TAUGHT_DYNAMICPUNCH', 441: 'MOVE_TUTOR_TAUGHT_DOUBLE_EDGE', 442: 'MOVE_TUTOR_TAUGHT_EXPLOSION', 443: 'DEFEATED_REGIROCK', 444: 'DEFEATED_REGICE', 445: 'DEFEATED_REGISTEEL', 446: 'DEFEATED_KYOGRE', 447: 'DEFEATED_GROUDON', 448: 'DEFEATED_RAYQUAZA', 449: 'DEFEATED_VOLTORB_1_NEW_MAUVILLE', 450: 'DEFEATED_VOLTORB_2_NEW_MAUVILLE', 451: 'DEFEATED_VOLTORB_3_NEW_MAUVILLE', 452: 'DEFEATED_ELECTRODE_1_AQUA_HIDEOUT', 453: 'DEFEATED_ELECTRODE_2_AQUA_HIDEOUT', 454: 'DEFEATED_SUDOWOODO', 455: 'DEFEATED_MEW', 456: 'DEFEATED_LATIAS_OR_LATIOS', 457: 'CAUGHT_LATIAS_OR_LATIOS', 458: 'CAUGHT_MEW', 459: 'MET_SCOTT_AFTER_OBTAINING_STONE_BADGE', 460: 'MET_SCOTT_IN_VERDANTURF', 461: 'MET_SCOTT_IN_FALLARBOR', 462: 'MET_SCOTT_IN_LILYCOVE', 463: 'MET_SCOTT_IN_EVERGRANDE', 464: 'MET_SCOTT_ON_SS_TIDAL', 465: 'SCOTT_GIVES_BATTLE_POINTS', 466: 'COLLECTED_ALL_GOLD_SYMBOLS', 467: 'ENABLE_ROXANNE_MATCH_CALL', 468: 'ENABLE_BRAWLY_MATCH_CALL', 469: 'ENABLE_WATTSON_MATCH_CALL', 470: 'ENABLE_FLANNERY_MATCH_CALL', 471: 'ENABLE_WINONA_MATCH_CALL', 472: 'ENABLE_TATE_AND_LIZA_MATCH_CALL', 473: 'ENABLE_JUAN_MATCH_CALL', 474: '_UNUSED', 475: 'SHOWN_MYSTIC_TICKET', 476: 'DEFEATED_HO_OH', 477: 'DEFEATED_LUGIA', 478: '_UNUSED', 479: '_UNUSED', 480: '_UNUSED', 481: '_UNUSED', 482: '_UNUSED', 483: '_UNUSED', 484: 'MYSTERY_GIFT_DONE', 485: 'MYSTERY_GIFT_1', 486: 'MYSTERY_GIFT_2', 487: 'MYSTERY_GIFT_3', 488: 'MYSTERY_GIFT_4', 489: 'MYSTERY_GIFT_5', 490: 'MYSTERY_GIFT_6', 491: 'MYSTERY_GIFT_7', 492: 'MYSTERY_GIFT_8', 493: 'MYSTERY_GIFT_9', 494: 'MYSTERY_GIFT_10', 495: 'MYSTERY_GIFT_11', 496: 'MYSTERY_GIFT_12', 497: 'MYSTERY_GIFT_13', 498: 'MYSTERY_GIFT_14', 499: 'MYSTERY_GIFT_15', 500: 'HIDDEN_ITEM_LAVARIDGE_TOWN_ICE_HEAL', 501: 'HIDDEN_ITEM_TRICK_HOUSE_NUGGET', 502: 'HIDDEN_ITEM_ROUTE_111_STARDUST', 503: 'HIDDEN_ITEM_ROUTE_113_ETHER', 504: 'HIDDEN_ITEM_ROUTE_114_CARBOS', 505: 'HIDDEN_ITEM_ROUTE_119_CALCIUM', 506: 'HIDDEN_ITEM_ROUTE_119_ULTRA_BALL', 507: 'HIDDEN_ITEM_ROUTE_123_SUPER_REPEL', 508: 'HIDDEN_ITEM_UNDERWATER_124_CARBOS', 509: 'HIDDEN_ITEM_UNDERWATER_124_GREEN_SHARD', 510: 'HIDDEN_ITEM_UNDERWATER_124_PEARL', 511: 'HIDDEN_ITEM_UNDERWATER_124_BIG_PEARL', 512: 'HIDDEN_ITEM_UNDERWATER_126_BLUE_SHARD', 513: 'HIDDEN_ITEM_UNDERWATER_124_HEART_SCALE_1', 514: 'HIDDEN_ITEM_UNDERWATER_126_HEART_SCALE', 515: 'HIDDEN_ITEM_UNDERWATER_126_ULTRA_BALL', 516: 'HIDDEN_ITEM_UNDERWATER_126_STARDUST', 517: 'HIDDEN_ITEM_UNDERWATER_126_PEARL', 518: 'HIDDEN_ITEM_UNDERWATER_126_YELLOW_SHARD', 519: 'HIDDEN_ITEM_UNDERWATER_126_IRON', 520: 'HIDDEN_ITEM_UNDERWATER_126_BIG_PEARL', 521: 'HIDDEN_ITEM_UNDERWATER_127_STAR_PIECE', 522: 'HIDDEN_ITEM_UNDERWATER_127_HP_UP', 523: 'HIDDEN_ITEM_UNDERWATER_127_HEART_SCALE', 524: 'HIDDEN_ITEM_UNDERWATER_127_RED_SHARD', 525: 'HIDDEN_ITEM_UNDERWATER_128_PROTEIN', 526: 'HIDDEN_ITEM_UNDERWATER_128_PEARL', 527: 'HIDDEN_ITEM_LILYCOVE_CITY_HEART_SCALE', 528: 'HIDDEN_ITEM_FALLARBOR_TOWN_NUGGET', 529: 'HIDDEN_ITEM_MT_PYRE_EXTERIOR_ULTRA_BALL', 530: 'HIDDEN_ITEM_ROUTE_113_TM_32', 531: 'HIDDEN_ITEM_ABANDONED_SHIP_RM_1_KEY', 532: 'HIDDEN_ITEM_ABANDONED_SHIP_RM_2_KEY', 533: 'HIDDEN_ITEM_ABANDONED_SHIP_RM_4_KEY', 534: 'HIDDEN_ITEM_ABANDONED_SHIP_RM_6_KEY', 535: 'HIDDEN_ITEM_SS_TIDAL_LOWER_DECK_LEFTOVERS', 536: 'HIDDEN_ITEM_UNDERWATER_124_CALCIUM', 537: 'HIDDEN_ITEM_ROUTE_104_POTION', 538: 'HIDDEN_ITEM_UNDERWATER_124_HEART_SCALE_2', 539: 'HIDDEN_ITEM_ROUTE_121_HP_UP', 540: 'HIDDEN_ITEM_ROUTE_121_NUGGET', 541: 'HIDDEN_ITEM_ROUTE_123_REVIVE', 542: 'HIDDEN_ITEM_ROUTE_113_REVIVE', 543: 'HIDDEN_ITEM_LILYCOVE_CITY_PP_UP', 544: 'HIDDEN_ITEM_ROUTE_104_SUPER_POTION', 545: 'HIDDEN_ITEM_ROUTE_116_SUPER_POTION', 546: 'HIDDEN_ITEM_ROUTE_106_STARDUST', 547: 'HIDDEN_ITEM_ROUTE_106_HEART_SCALE', 548: 'HIDDEN_ITEM_GRANITE_CAVE_B2F_EVERSTONE_1', 549: 'HIDDEN_ITEM_GRANITE_CAVE_B2F_EVERSTONE_2', 550: 'HIDDEN_ITEM_ROUTE_109_REVIVE', 551: 'HIDDEN_ITEM_ROUTE_109_GREAT_BALL', 552: 'HIDDEN_ITEM_ROUTE_109_HEART_SCALE_1', 553: 'HIDDEN_ITEM_ROUTE_110_GREAT_BALL', 554: 'HIDDEN_ITEM_ROUTE_110_REVIVE', 555: 'HIDDEN_ITEM_ROUTE_110_FULL_HEAL', 556: 'HIDDEN_ITEM_ROUTE_111_PROTEIN', 557: 'HIDDEN_ITEM_ROUTE_111_RARE_CANDY', 558: 'HIDDEN_ITEM_PETALBURG_WOODS_POTION', 559: 'HIDDEN_ITEM_PETALBURG_WOODS_TINY_MUSHROOM_1', 560: 'HIDDEN_ITEM_PETALBURG_WOODS_TINY_MUSHROOM_2', 561: 'HIDDEN_ITEM_PETALBURG_WOODS_POKE_BALL', 562: 'HIDDEN_ITEM_ROUTE_104_POKE_BALL', 563: 'HIDDEN_ITEM_ROUTE_106_POKE_BALL', 564: 'HIDDEN_ITEM_ROUTE_109_ETHER', 565: 'HIDDEN_ITEM_ROUTE_110_POKE_BALL', 566: 'HIDDEN_ITEM_ROUTE_118_HEART_SCALE', 567: 'HIDDEN_ITEM_ROUTE_118_IRON', 568: 'HIDDEN_ITEM_ROUTE_119_FULL_HEAL', 569: 'HIDDEN_ITEM_ROUTE_120_RARE_CANDY_2', 570: 'HIDDEN_ITEM_ROUTE_120_ZINC', 571: 'HIDDEN_ITEM_ROUTE_120_RARE_CANDY_1', 572: 'HIDDEN_ITEM_ROUTE_117_REPEL', 573: 'HIDDEN_ITEM_ROUTE_121_FULL_HEAL', 574: 'HIDDEN_ITEM_ROUTE_123_HYPER_POTION', 575: 'HIDDEN_ITEM_LILYCOVE_CITY_POKE_BALL', 576: 'HIDDEN_ITEM_JAGGED_PASS_GREAT_BALL', 577: 'HIDDEN_ITEM_JAGGED_PASS_FULL_HEAL', 578: 'HIDDEN_ITEM_MT_PYRE_EXTERIOR_MAX_ETHER', 579: 'HIDDEN_ITEM_MT_PYRE_SUMMIT_ZINC', 580: 'HIDDEN_ITEM_MT_PYRE_SUMMIT_RARE_CANDY', 581: 'HIDDEN_ITEM_VICTORY_ROAD_1F_ULTRA_BALL', 582: 'HIDDEN_ITEM_VICTORY_ROAD_B2F_ELIXIR', 583: 'HIDDEN_ITEM_VICTORY_ROAD_B2F_MAX_REPEL', 584: 'HIDDEN_ITEM_ROUTE_120_REVIVE', 585: 'HIDDEN_ITEM_ROUTE_104_ANTIDOTE', 586: 'HIDDEN_ITEM_ROUTE_108_RARE_CANDY', 587: 'HIDDEN_ITEM_ROUTE_119_MAX_ETHER', 588: 'HIDDEN_ITEM_ROUTE_104_HEART_SCALE', 589: 'HIDDEN_ITEM_ROUTE_105_HEART_SCALE', 590: 'HIDDEN_ITEM_ROUTE_109_HEART_SCALE_2', 591: 'HIDDEN_ITEM_ROUTE_109_HEART_SCALE_3', 592: 'HIDDEN_ITEM_ROUTE_128_HEART_SCALE_1', 593: 'HIDDEN_ITEM_ROUTE_128_HEART_SCALE_2', 594: 'HIDDEN_ITEM_ROUTE_128_HEART_SCALE_3', 595: 'HIDDEN_ITEM_PETALBURG_CITY_RARE_CANDY', 596: 'HIDDEN_ITEM_ROUTE_116_BLACK_GLASSES', 597: 'HIDDEN_ITEM_ROUTE_115_HEART_SCALE', 598: 'HIDDEN_ITEM_ROUTE_113_NUGGET', 599: 'HIDDEN_ITEM_ROUTE_123_PP_UP', 600: 'HIDDEN_ITEM_ROUTE_121_MAX_REVIVE', 601: 'HIDDEN_ITEM_ARTISAN_CAVE_B1F_CALCIUM', 602: 'HIDDEN_ITEM_ARTISAN_CAVE_B1F_ZINC', 603: 'HIDDEN_ITEM_ARTISAN_CAVE_B1F_PROTEIN', 604: 'HIDDEN_ITEM_ARTISAN_CAVE_B1F_IRON', 605: 'HIDDEN_ITEM_SAFARI_ZONE_SOUTH_EAST_FULL_RESTORE', 606: 'HIDDEN_ITEM_SAFARI_ZONE_NORTH_EAST_RARE_CANDY', 607: 'HIDDEN_ITEM_SAFARI_ZONE_NORTH_EAST_ZINC', 608: 'HIDDEN_ITEM_SAFARI_ZONE_SOUTH_EAST_PP_UP', 609: 'HIDDEN_ITEM_NAVEL_ROCK_TOP_SACRED_ASH', 610: 'HIDDEN_ITEM_ROUTE_123_RARE_CANDY', 611: 'HIDDEN_ITEM_ROUTE_105_BIG_PEARL', 612: '_UNUSED', 613: '_UNUSED', 614: '_UNUSED', 615: '_UNUSED', 616: '_UNUSED', 617: '_UNUSED', 618: '_UNUSED', 619: '_UNUSED', 620: '_UNUSED', 621: '_UNUSED', 622: '_UNUSED', 623: '_UNUSED', 624: '_UNUSED', 625: '_UNUSED', 626: '_UNUSED', 627: '_UNUSED', 628: '_UNUSED', 629: '_UNUSED', 630: '_UNUSED', 631: '_UNUSED', 632: '_UNUSED', 633: '_UNUSED', 634: '_UNUSED', 635: '_UNUSED', 636: '_UNUSED', 637: '_UNUSED', 638: '_UNUSED', 639: '_UNUSED', 640: '_UNUSED', 641: '_UNUSED', 642: '_UNUSED', 643: '_UNUSED', 644: '_UNUSED', 645: '_UNUSED', 646: '_UNUSED', 647: '_UNUSED', 648: '_UNUSED', 649: '_UNUSED', 650: '_UNUSED', 651: '_UNUSED', 652: '_UNUSED', 653: '_UNUSED', 654: '_UNUSED', 655: '_UNUSED', 656: '_UNUSED', 657: '_UNUSED', 658: '_UNUSED', 659: '_UNUSED', 660: '_UNUSED', 661: '_UNUSED', 662: '_UNUSED', 663: '_UNUSED', 664: '_UNUSED', 665: '_UNUSED', 666: '_UNUSED', 667: '_UNUSED', 668: '_UNUSED', 669: '_UNUSED', 670: '_UNUSED', 671: '_UNUSED', 672: '_UNUSED', 673: '_UNUSED', 674: '_UNUSED', 675: '_UNUSED', 676: '_UNUSED', 677: '_UNUSED', 678: '_UNUSED', 679: '_UNUSED', 680: '_UNUSED', 681: '_UNUSED', 682: '_UNUSED', 683: '_UNUSED', 684: '_UNUSED', 685: '_UNUSED', 686: '_UNUSED', 687: '_UNUSED', 688: '_UNUSED', 689: '_UNUSED', 690: '_UNUSED', 691: '_UNUSED', 692: '_UNUSED', 693: '_UNUSED', 694: '_UNUSED', 695: '_UNUSED', 696: '_UNUSED', 697: '_UNUSED', 698: '_UNUSED', 699: '_UNUSED', 700: 'HIDE_ROUTE_101_BIRCH_STARTERS_BAG', 701: 'HIDE_APPRENTICE', 702: 'HIDE_POKEMON_CENTER_2F_MYSTERY_GIFT_MAN', 703: 'HIDE_UNION_ROOM_PLAYER_1', 704: 'HIDE_UNION_ROOM_PLAYER_2', 705: 'HIDE_UNION_ROOM_PLAYER_3', 706: 'HIDE_UNION_ROOM_PLAYER_4', 707: 'HIDE_UNION_ROOM_PLAYER_5', 708: 'HIDE_UNION_ROOM_PLAYER_6', 709: 'HIDE_UNION_ROOM_PLAYER_7', 710: 'HIDE_UNION_ROOM_PLAYER_8', 711: 'HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_1', 712: 'HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_2', 713: 'HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_3', 714: 'HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_4', 715: 'HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_5', 716: 'HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_6', 717: 'HIDE_SAFARI_ZONE_SOUTH_CONSTRUCTION_WORKERS', 718: 'HIDE_MEW', 719: 'HIDE_ROUTE_104_RIVAL', 720: 'HIDE_ROUTE_101_BIRCH_ZIGZAGOON_BATTLE', 721: 'HIDE_LITTLEROOT_TOWN_BIRCHS_LAB_BIRCH', 722: 'HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_RIVAL_BEDROOM', 723: 'HIDE_ROUTE_103_RIVAL', 724: 'HIDE_PETALBURG_WOODS_DEVON_EMPLOYEE', 725: 'HIDE_PETALBURG_WOODS_AQUA_GRUNT', 726: 'HIDE_PETALBURG_CITY_WALLY', 727: 'HIDE_MOSSDEEP_CITY_STEVENS_HOUSE_INVISIBLE_NINJA_BOY', 728: 'HIDE_PETALBURG_CITY_WALLYS_MOM', 729: '_UNUSED', 730: 'HIDE_LILYCOVE_FAN_CLUB_INTERVIEWER', 731: 'HIDE_RUSTBORO_CITY_AQUA_GRUNT', 732: 'HIDE_RUSTBORO_CITY_DEVON_EMPLOYEE_1', 733: 'HIDE_SEAFLOOR_CAVERN_ROOM_9_KYOGRE_ASLEEP', 734: 'HIDE_PLAYERS_HOUSE_DAD', 735: 'HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_RIVAL_SIBLING', 736: 'HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_RIVAL_SIBLING', 737: 'HIDE_MOSSDEEP_CITY_SPACE_CENTER_MAGMA_NOTE', 738: 'HIDE_ROUTE_104_MR_BRINEY', 739: 'HIDE_BRINEYS_HOUSE_MR_BRINEY', 740: 'HIDE_MR_BRINEY_DEWFORD_TOWN', 741: 'HIDE_ROUTE_109_MR_BRINEY', 742: 'HIDE_ROUTE_104_MR_BRINEY_BOAT', 743: 'HIDE_MR_BRINEY_BOAT_DEWFORD_TOWN', 744: 'HIDE_ROUTE_109_MR_BRINEY_BOAT', 745: 'HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_BRENDAN', 746: 'HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_MAY', 747: 'HIDE_SAFARI_ZONE_SOUTH_EAST_EXPANSION', 748: 'HIDE_LILYCOVE_HARBOR_EVENT_TICKET_TAKER', 749: 'HIDE_SLATEPORT_CITY_SCOTT', 750: 'HIDE_ROUTE_101_ZIGZAGOON', 751: 'HIDE_VICTORY_ROAD_EXIT_WALLY', 752: 'HIDE_LITTLEROOT_TOWN_MOM_OUTSIDE', 753: 'HIDE_MOSSDEEP_CITY_SPACE_CENTER_1F_STEVEN', 754: 'HIDE_LITTLEROOT_TOWN_PLAYERS_HOUSE_VIGOROTH_1', 755: 'HIDE_LITTLEROOT_TOWN_PLAYERS_HOUSE_VIGOROTH_2', 756: 'HIDE_MOSSDEEP_CITY_SPACE_CENTER_1F_TEAM_MAGMA', 757: 'HIDE_LITTLEROOT_TOWN_PLAYERS_BEDROOM_MOM', 758: 'HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_MOM', 759: 'HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_MOM', 760: 'HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_RIVAL_BEDROOM', 761: 'HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_TRUCK', 762: 'HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_TRUCK', 763: 'HIDE_DEOXYS', 764: 'HIDE_BIRTH_ISLAND_DEOXYS_TRIANGLE', 765: 'HIDE_MAUVILLE_CITY_SCOTT', 766: 'HIDE_VERDANTURF_TOWN_SCOTT', 767: 'HIDE_FALLARBOR_TOWN_BATTLE_TENT_SCOTT', 768: 'HIDE_ROUTE_111_VICTOR_WINSTRATE', 769: 'HIDE_ROUTE_111_VICTORIA_WINSTRATE', 770: 'HIDE_ROUTE_111_VIVI_WINSTRATE', 771: 'HIDE_ROUTE_111_VICKY_WINSTRATE', 772: 'HIDE_PETALBURG_GYM_NORMAN', 773: 'HIDE_SKY_PILLAR_TOP_RAYQUAZA', 774: 'HIDE_LILYCOVE_CONTEST_HALL_CONTEST_ATTENDANT_1', 775: 'HIDE_LILYCOVE_MUSEUM_CURATOR', 776: 'HIDE_LILYCOVE_MUSEUM_PATRON_1', 777: 'HIDE_LILYCOVE_MUSEUM_PATRON_2', 778: 'HIDE_LILYCOVE_MUSEUM_PATRON_3', 779: 'HIDE_LILYCOVE_MUSEUM_PATRON_4', 780: 'HIDE_LILYCOVE_MUSEUM_TOURISTS', 781: 'HIDE_PETALBURG_GYM_GREETER', 782: 'HIDE_MARINE_CAVE_KYOGRE', 783: 'HIDE_TERRA_CAVE_GROUDON', 784: 'HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_RIVAL_MOM', 785: 'HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_RIVAL_MOM', 786: 'HIDE_ROUTE_119_SCOTT', 787: 'HIDE_LILYCOVE_MOTEL_SCOTT', 788: 'HIDE_MOSSDEEP_CITY_SCOTT', 789: 'HIDE_FANCLUB_OLD_LADY', 790: 'HIDE_FANCLUB_BOY', 791: 'HIDE_FANCLUB_LITTLE_BOY', 792: 'HIDE_FANCLUB_LADY', 793: 'HIDE_EVER_GRANDE_POKEMON_CENTER_1F_SCOTT', 794: 'HIDE_LITTLEROOT_TOWN_RIVAL', 795: 'HIDE_LITTLEROOT_TOWN_BIRCH', 796: 'HIDE_ROUTE_111_GABBY_AND_TY_1', 797: 'HIDE_ROUTE_118_GABBY_AND_TY_1', 798: 'HIDE_ROUTE_120_GABBY_AND_TY_1', 799: 'HIDE_ROUTE_111_GABBY_AND_TY_3', 800: 'HIDE_LUGIA', 801: 'HIDE_HO_OH', 802: 'HIDE_LILYCOVE_CONTEST_HALL_REPORTER', 803: 'HIDE_SLATEPORT_CITY_CONTEST_REPORTER', 804: 'HIDE_MAUVILLE_CITY_WALLY', 805: 'HIDE_MAUVILLE_CITY_WALLYS_UNCLE', 806: 'HIDE_VERDANTURF_TOWN_WANDAS_HOUSE_WALLY', 807: 'HIDE_RUSTURF_TUNNEL_WANDAS_BOYFRIEND', 808: 'HIDE_VERDANTURF_TOWN_WANDAS_HOUSE_WANDAS_BOYFRIEND', 809: 'HIDE_VERDANTURF_TOWN_WANDAS_HOUSE_WALLYS_UNCLE', 810: 'HIDE_SS_TIDAL_CORRIDOR_SCOTT', 811: 'HIDE_LITTLEROOT_TOWN_BIRCHS_LAB_POKEBALL_CYNDAQUIL', 812: 'HIDE_LITTLEROOT_TOWN_BIRCHS_LAB_POKEBALL_TOTODILE', 813: 'HIDE_ROUTE_116_DROPPED_GLASSES_MAN', 814: 'HIDE_RUSTBORO_CITY_RIVAL', 815: 'HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F_SWABLU_DOLL', 816: 'HIDE_SOOTOPOLIS_CITY_WALLACE', 817: 'HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F_POKE_BALL', 818: 'HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_2F_POKE_BALL', 819: 'HIDE_ROUTE_112_TEAM_MAGMA', 820: 'HIDE_CAVE_OF_ORIGIN_B1F_WALLACE', 821: 'HIDE_AQUA_HIDEOUT_1F_GRUNT_1_BLOCKING_ENTRANCE', 822: 'HIDE_AQUA_HIDEOUT_1F_GRUNT_2_BLOCKING_ENTRANCE', 823: 'HIDE_MOSSDEEP_CITY_TEAM_MAGMA', 824: 'HIDE_PETALBURG_GYM_WALLYS_DAD', 825: '_UNUSED', 826: 'HIDE_SOOTOPOLIS_CITY_ARCHIE', 827: 'HIDE_SOOTOPOLIS_CITY_MAXIE', 828: 'HIDE_SEAFLOOR_CAVERN_ROOM_9_ARCHIE', 829: 'HIDE_SEAFLOOR_CAVERN_ROOM_9_MAXIE', 830: 'HIDE_PETALBURG_CITY_WALLYS_DAD', 831: 'HIDE_SEAFLOOR_CAVERN_ROOM_9_MAGMA_GRUNTS', 832: 'HIDE_LILYCOVE_CONTEST_HALL_BLEND_MASTER', 833: 'HIDE_GRANITE_CAVE_STEVEN', 834: 'HIDE_ROUTE_128_STEVEN', 835: 'HIDE_SLATEPORT_CITY_GABBY_AND_TY', 836: 'HIDE_BATTLE_FRONTIER_RECEPTION_GATE_SCOTT', 837: 'HIDE_ROUTE_110_BIRCH', 838: 'HIDE_LITTLEROOT_TOWN_BIRCHS_LAB_POKEBALL_CHIKORITA', 839: 'HIDE_SOOTOPOLIS_CITY_MAN_1', 840: 'HIDE_SLATEPORT_CITY_CAPTAIN_STERN', 841: 'HIDE_SLATEPORT_CITY_HARBOR_CAPTAIN_STERN', 842: 'HIDE_BATTLE_FRONTIER_SUDOWOODO', 843: 'HIDE_ROUTE_111_ROCK_SMASH_TIP_GUY', 844: 'HIDE_RUSTBORO_CITY_SCIENTIST', 845: 'HIDE_SLATEPORT_CITY_HARBOR_AQUA_GRUNT', 846: 'HIDE_SLATEPORT_CITY_HARBOR_ARCHIE', 847: 'HIDE_JAGGED_PASS_MAGMA_GUARD', 848: 'HIDE_SLATEPORT_CITY_HARBOR_SUBMARINE_SHADOW', 849: 'HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_2F_PICHU_DOLL', 850: 'HIDE_MAGMA_HIDEOUT_4F_GROUDON_ASLEEP', 851: 'HIDE_ROUTE_119_RIVAL', 852: 'HIDE_LILYCOVE_CITY_AQUA_GRUNTS', 853: 'HIDE_MAGMA_HIDEOUT_4F_GROUDON', 854: 'HIDE_SOOTOPOLIS_CITY_RESIDENTS', 855: 'HIDE_SKY_PILLAR_WALLACE', 856: 'HIDE_MT_PYRE_SUMMIT_MAXIE', 857: 'HIDE_MAGMA_HIDEOUT_GRUNTS', 858: 'HIDE_VICTORY_ROAD_ENTRANCE_WALLY', 859: 'HIDE_SEAFLOOR_CAVERN_ROOM_9_KYOGRE', 860: 'HIDE_SLATEPORT_CITY_HARBOR_SS_TIDAL', 861: 'HIDE_LILYCOVE_HARBOR_SSTIDAL', 862: 'HIDE_MOSSDEEP_CITY_SPACE_CENTER_2F_TEAM_MAGMA', 863: 'HIDE_MOSSDEEP_CITY_SPACE_CENTER_2F_STEVEN', 864: 'HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_ALT_1', 865: 'HIDE_BATTLE_TOWER_MULTI_BATTLE_PARTNER_ALT_2', 866: 'HIDE_PETALBURG_GYM_WALLY', 867: 'UNKNOWN_0x363', 868: 'HIDE_LITTLEROOT_TOWN_FAT_MAN', 869: 'HIDE_SLATEPORT_CITY_STERNS_SHIPYARD_MR_BRINEY', 870: 'HIDE_LANETTES_HOUSE_LANETTE', 871: 'HIDE_FALLORBOR_POKEMON_CENTER_LANETTE', 872: 'HIDE_TRICK_HOUSE_ENTRANCE_MAN', 873: 'HIDE_LILYCOVE_CONTEST_HALL_BLEND_MASTER_REPLACEMENT', 874: 'HIDE_DESERT_UNDERPASS_FOSSIL', 875: 'HIDE_ROUTE_111_PLAYER_DESCENT', 876: 'HIDE_ROUTE_111_DESERT_FOSSIL', 877: 'HIDE_MT_CHIMNEY_TRAINERS', 878: 'HIDE_RUSTURF_TUNNEL_AQUA_GRUNT', 879: 'HIDE_RUSTURF_TUNNEL_BRINEY', 880: 'HIDE_RUSTURF_TUNNEL_PEEKO', 881: 'HIDE_BRINEYS_HOUSE_PEEKO', 882: 'HIDE_SLATEPORT_CITY_TEAM_AQUA', 883: 'HIDE_SLATEPORT_CITY_OCEANIC_MUSEUM_AQUA_GRUNTS', 884: 'HIDE_SLATEPORT_CITY_OCEANIC_MUSEUM_2F_AQUA_GRUNT_1', 885: 'HIDE_SLATEPORT_CITY_OCEANIC_MUSEUM_2F_AQUA_GRUNT_2', 886: 'HIDE_SLATEPORT_CITY_OCEANIC_MUSEUM_2F_ARCHIE', 887: 'HIDE_SLATEPORT_CITY_OCEANIC_MUSEUM_2F_CAPTAIN_STERN', 888: 'HIDE_BATTLE_TOWER_OPPONENT', 889: 'HIDE_LITTLEROOT_TOWN_BIRCHS_LAB_RIVAL', 890: 'HIDE_ROUTE_119_TEAM_AQUA', 891: 'HIDE_ROUTE_116_MR_BRINEY', 892: 'HIDE_WEATHER_INSTITUTE_1F_WORKERS', 893: 'HIDE_WEATHER_INSTITUTE_2F_WORKERS', 894: 'HIDE_ROUTE_116_WANDAS_BOYFRIEND', 895: 'HIDE_LILYCOVE_CONTEST_HALL_CONTEST_ATTENDANT_2', 896: 'HIDE_LITTLEROOT_TOWN_BIRCHS_LAB_UNKNOWN_0x380', 897: 'HIDE_ROUTE_101_BIRCH', 898: 'HIDE_ROUTE_103_BIRCH', 899: 'HIDE_TRICK_HOUSE_END_MAN', 900: 'HIDE_ROUTE_110_TEAM_AQUA', 901: 'HIDE_ROUTE_118_GABBY_AND_TY_2', 902: 'HIDE_ROUTE_120_GABBY_AND_TY_2', 903: 'HIDE_ROUTE_111_GABBY_AND_TY_2', 904: 'HIDE_ROUTE_118_GABBY_AND_TY_3', 905: 'HIDE_SLATEPORT_CITY_HARBOR_PATRONS', 906: 'HIDE_ROUTE_104_WHITE_HERB_FLORIST', 907: 'HIDE_FALLARBOR_AZURILL', 908: 'HIDE_LILYCOVE_HARBOR_FERRY_ATTENDANT', 909: 'HIDE_LILYCOVE_HARBOR_FERRY_SAILOR', 910: 'HIDE_SOUTHERN_ISLAND_EON_STONE', 911: 'HIDE_SOUTHERN_ISLAND_UNCHOSEN_EON_DUO_MON', 912: 'HIDE_MAUVILLE_CITY_WATTSON', 913: 'HIDE_MAUVILLE_GYM_WATTSON', 914: 'HIDE_ROUTE_121_TEAM_AQUA_GRUNTS', 915: 'UNKNOWN_0x393', 916: 'HIDE_MT_PYRE_SUMMIT_ARCHIE', 917: 'HIDE_MT_PYRE_SUMMIT_TEAM_AQUA', 918: 'HIDE_BATTLE_TOWER_REPORTER', 919: 'HIDE_ROUTE_110_RIVAL', 920: 'HIDE_CHAMPIONS_ROOM_RIVAL', 921: 'HIDE_CHAMPIONS_ROOM_BIRCH', 922: 'HIDE_ROUTE_110_RIVAL_ON_BIKE', 923: 'HIDE_ROUTE_119_RIVAL_ON_BIKE', 924: 'HIDE_AQUA_HIDEOUT_GRUNTS', 925: 'HIDE_LILYCOVE_MOTEL_GAME_DESIGNERS', 926: 'HIDE_MT_CHIMNEY_TEAM_AQUA', 927: 'HIDE_MT_CHIMNEY_TEAM_MAGMA', 928: 'HIDE_FALLARBOR_HOUSE_PROF_COZMO', 929: 'HIDE_LAVARIDGE_TOWN_RIVAL', 930: 'HIDE_LAVARIDGE_TOWN_RIVAL_ON_BIKE', 931: 'HIDE_RUSTURF_TUNNEL_ROCK_1', 932: 'HIDE_RUSTURF_TUNNEL_ROCK_2', 933: 'HIDE_FORTREE_CITY_HOUSE_4_WINGULL', 934: 'HIDE_MOSSDEEP_CITY_HOUSE_2_WINGULL', 935: 'HIDE_REGIROCK', 936: 'HIDE_REGICE', 937: 'HIDE_REGISTEEL', 938: 'HIDE_METEOR_FALLS_TEAM_AQUA', 939: 'HIDE_METEOR_FALLS_TEAM_MAGMA', 940: 'HIDE_DEWFORD_HALL_SLUDGE_BOMB_MAN', 941: 'HIDE_SEAFLOOR_CAVERN_ENTRANCE_AQUA_GRUNT', 942: 'HIDE_METEOR_FALLS_1F_1R_COZMO', 943: 'HIDE_AQUA_HIDEOUT_B2F_SUBMARINE_SHADOW', 944: 'HIDE_ROUTE_128_ARCHIE', 945: 'HIDE_ROUTE_128_MAXIE', 946: 'HIDE_SEAFLOOR_CAVERN_AQUA_GRUNTS', 947: 'HIDE_ROUTE_116_DEVON_EMPLOYEE', 948: 'HIDE_SLATEPORT_CITY_TM_SALESMAN', 949: 'HIDE_RUSTBORO_CITY_DEVON_CORP_3F_EMPLOYEE', 950: 'HIDE_SS_TIDAL_CORRIDOR_MR_BRINEY', 951: 'HIDE_SS_TIDAL_ROOMS_SNATCH_GIVER', 952: 'RECEIVED_SHOAL_SALT_1', 953: 'RECEIVED_SHOAL_SALT_2', 954: 'RECEIVED_SHOAL_SALT_3', 955: 'RECEIVED_SHOAL_SALT_4', 956: 'RECEIVED_SHOAL_SHELL_1', 957: 'RECEIVED_SHOAL_SHELL_2', 958: 'RECEIVED_SHOAL_SHELL_3', 959: 'RECEIVED_SHOAL_SHELL_4', 960: 'HIDE_ROUTE_111_SECRET_POWER_MAN', 961: 'HIDE_SLATEPORT_MUSEUM_POPULATION', 962: 'HIDE_LILYCOVE_DEPARTMENT_STORE_ROOFTOP_SALE_WOMAN', 963: 'HIDE_MIRAGE_TOWER_ROOT_FOSSIL', 964: 'HIDE_MIRAGE_TOWER_CLAW_FOSSIL', 965: 'HIDE_SLATEPORT_CITY_OCEANIC_MUSEUM_FAMILIAR_AQUA_GRUNT', 966: 'HIDE_ROUTE_118_STEVEN', 967: 'HIDE_MOSSDEEP_CITY_STEVENS_HOUSE_STEVEN', 968: 'HIDE_MOSSDEEP_CITY_STEVENS_HOUSE_BELDUM_POKEBALL', 969: 'HIDE_FORTREE_CITY_KECLEON', 970: 'HIDE_ROUTE_120_KECLEON_BRIDGE', 971: 'HIDE_LILYCOVE_CITY_RIVAL', 972: 'HIDE_ROUTE_120_STEVEN', 973: 'HIDE_SOOTOPOLIS_CITY_STEVEN', 974: 'HIDE_NEW_MAUVILLE_VOLTORB_1', 975: 'HIDE_NEW_MAUVILLE_VOLTORB_2', 976: 'HIDE_NEW_MAUVILLE_VOLTORB_3', 977: 'HIDE_AQUA_HIDEOUT_B1F_ELECTRODE_1', 978: 'HIDE_AQUA_HIDEOUT_B1F_ELECTRODE_2', 979: 'HIDE_OLDALE_TOWN_RIVAL', 980: 'HIDE_UNDERWATER_SEA_FLOOR_CAVERN_STOLEN_SUBMARINE', 981: 'HIDE_ROUTE_120_KECLEON_BRIDGE_SHADOW', 982: 'HIDE_ROUTE_120_KECLEON_1', 983: 'HIDE_RUSTURF_TUNNEL_WANDA', 984: 'HIDE_VERDANTURF_TOWN_WANDAS_HOUSE_WANDA', 985: 'HIDE_ROUTE_120_KECLEON_2', 986: 'HIDE_ROUTE_120_KECLEON_3', 987: 'HIDE_ROUTE_120_KECLEON_4', 988: 'HIDE_ROUTE_120_KECLEON_5', 989: 'HIDE_ROUTE_119_KECLEON_1', 990: 'HIDE_ROUTE_119_KECLEON_2', 991: 'HIDE_ROUTE_101_BOY', 992: 'HIDE_WEATHER_INSTITUTE_2F_AQUA_GRUNT_M', 993: 'HIDE_LILYCOVE_POKEMON_CENTER_CONTEST_LADY_MON', 994: 'HIDE_MT_CHIMNEY_LAVA_COOKIE_LADY', 995: 'HIDE_PETALBURG_CITY_SCOTT', 996: 'HIDE_SOOTOPOLIS_CITY_RAYQUAZA', 997: 'HIDE_SOOTOPOLIS_CITY_KYOGRE', 998: 'HIDE_SOOTOPOLIS_CITY_GROUDON', 999: 'HIDE_RUSTBORO_CITY_POKEMON_SCHOOL_SCOTT', 1000: 'ITEM_ROUTE_102_POTION', 1001: 'ITEM_ROUTE_116_X_SPECIAL', 1002: 'ITEM_ROUTE_104_PP_UP', 1003: 'ITEM_ROUTE_105_IRON', 1004: 'ITEM_ROUTE_106_PROTEIN', 1005: 'ITEM_ROUTE_109_PP_UP', 1006: 'ITEM_ROUTE_109_RARE_CANDY', 1007: 'ITEM_ROUTE_110_DIRE_HIT', 1008: 'ITEM_ROUTE_111_TM_37', 1009: 'ITEM_ROUTE_111_STARDUST', 1010: 'ITEM_ROUTE_111_HP_UP', 1011: 'ITEM_ROUTE_112_NUGGET', 1012: 'ITEM_ROUTE_113_MAX_ETHER', 1013: 'ITEM_ROUTE_113_SUPER_REPEL', 1014: 'ITEM_ROUTE_114_RARE_CANDY', 1015: 'ITEM_ROUTE_114_PROTEIN', 1016: 'ITEM_ROUTE_115_SUPER_POTION', 1017: 'ITEM_ROUTE_115_TM_01', 1018: 'ITEM_ROUTE_115_IRON', 1019: 'ITEM_ROUTE_116_ETHER', 1020: 'ITEM_ROUTE_116_REPEL', 1021: 'ITEM_ROUTE_116_HP_UP', 1022: 'ITEM_ROUTE_117_GREAT_BALL', 1023: 'ITEM_ROUTE_117_REVIVE', 1024: 'ITEM_ROUTE_119_SUPER_REPEL', 1025: 'ITEM_ROUTE_119_ZINC', 1026: 'ITEM_ROUTE_119_ELIXIR_1', 1027: 'ITEM_ROUTE_119_LEAF_STONE', 1028: 'ITEM_ROUTE_119_RARE_CANDY', 1029: 'ITEM_ROUTE_119_HYPER_POTION_1', 1030: 'ITEM_ROUTE_120_NUGGET', 1031: 'ITEM_ROUTE_120_FULL_HEAL', 1032: 'ITEM_ROUTE_123_CALCIUM', 1033: '_UNUSED', 1034: 'ITEM_ROUTE_127_ZINC', 1035: 'ITEM_ROUTE_127_CARBOS', 1036: 'ITEM_ROUTE_132_RARE_CANDY', 1037: 'ITEM_ROUTE_133_BIG_PEARL', 1038: 'ITEM_ROUTE_133_STAR_PIECE', 1039: 'ITEM_PETALBURG_CITY_MAX_REVIVE', 1040: 'ITEM_PETALBURG_CITY_ETHER', 1041: 'ITEM_RUSTBORO_CITY_X_DEFEND', 1042: 'ITEM_LILYCOVE_CITY_MAX_REPEL', 1043: 'ITEM_MOSSDEEP_CITY_NET_BALL', 1044: 'ITEM_METEOR_FALLS_1F_1R_TM_23', 1045: 'ITEM_METEOR_FALLS_1F_1R_FULL_HEAL', 1046: 'ITEM_METEOR_FALLS_1F_1R_MOON_STONE', 1047: 'ITEM_METEOR_FALLS_1F_1R_PP_UP', 1048: 'ITEM_RUSTURF_TUNNEL_POKE_BALL', 1049: 'ITEM_RUSTURF_TUNNEL_MAX_ETHER', 1050: 'ITEM_GRANITE_CAVE_1F_ESCAPE_ROPE', 1051: 'ITEM_GRANITE_CAVE_B1F_POKE_BALL', 1052: 'ITEM_MT_PYRE_5F_LAX_INCENSE', 1053: 'ITEM_GRANITE_CAVE_B2F_REPEL', 1054: 'ITEM_GRANITE_CAVE_B2F_RARE_CANDY', 1055: 'ITEM_PETALBURG_WOODS_X_ATTACK', 1056: 'ITEM_PETALBURG_WOODS_GREAT_BALL', 1057: 'ITEM_ROUTE_104_POKE_BALL', 1058: 'ITEM_PETALBURG_WOODS_ETHER', 1059: 'ITEM_MAGMA_HIDEOUT_3F_3R_ECAPE_ROPE', 1060: 'ITEM_TRICK_HOUSE_PUZZLE_1_ORANGE_MAIL', 1061: 'ITEM_TRICK_HOUSE_PUZZLE_2_HARBOR_MAIL', 1062: 'ITEM_TRICK_HOUSE_PUZZLE_2_WAVE_MAIL', 1063: 'ITEM_TRICK_HOUSE_PUZZLE_3_SHADOW_MAIL', 1064: 'ITEM_TRICK_HOUSE_PUZZLE_3_WOOD_MAIL', 1065: 'ITEM_TRICK_HOUSE_PUZZLE_4_MECH_MAIL', 1066: 'ITEM_ROUTE_124_YELLOW_SHARD', 1067: 'ITEM_TRICK_HOUSE_PUZZLE_6_GLITTER_MAIL', 1068: 'ITEM_TRICK_HOUSE_PUZZLE_7_TROPIC_MAIL', 1069: 'ITEM_TRICK_HOUSE_PUZZLE_8_BEAD_MAIL', 1070: 'ITEM_JAGGED_PASS_BURN_HEAL', 1071: 'ITEM_AQUA_HIDEOUT_B1F_MAX_ELIXIR', 1072: 'ITEM_AQUA_HIDEOUT_B2F_NEST_BALL', 1073: 'ITEM_MT_PYRE_EXTERIOR_MAX_POTION', 1074: 'ITEM_MT_PYRE_EXTERIOR_TM_48', 1075: 'ITEM_NEW_MAUVILLE_ULTRA_BALL', 1076: 'ITEM_NEW_MAUVILLE_ESCAPE_ROPE', 1077: 'ITEM_ABANDONED_SHIP_HIDDEN_FLOOR_ROOM_6_LUXURY_BALL', 1078: 'ITEM_ABANDONED_SHIP_HIDDEN_FLOOR_ROOM_4_SCANNER', 1079: 'ITEM_SCORCHED_SLAB_TM_11', 1080: 'ITEM_METEOR_FALLS_B1F_2R_TM_02', 1081: 'ITEM_SHOAL_CAVE_ENTRANCE_BIG_PEARL', 1082: 'ITEM_SHOAL_CAVE_INNER_ROOM_RARE_CANDY', 1083: 'ITEM_SHOAL_CAVE_STAIRS_ROOM_ICE_HEAL', 1084: 'ITEM_VICTORY_ROAD_1F_MAX_ELIXIR', 1085: 'ITEM_VICTORY_ROAD_1F_PP_UP', 1086: 'ITEM_VICTORY_ROAD_B1F_TM_29', 1087: 'ITEM_VICTORY_ROAD_B1F_FULL_RESTORE', 1088: 'ITEM_VICTORY_ROAD_B2F_FULL_HEAL', 1089: 'ITEM_MT_PYRE_6F_TM_30', 1090: 'ITEM_SEAFLOOR_CAVERN_ROOM_9_TM_26', 1091: 'ITEM_FIERY_PATH_TM06', 1092: 'ITEM_ROUTE_124_RED_SHARD', 1093: 'ITEM_ROUTE_124_BLUE_SHARD', 1094: 'ITEM_SAFARI_ZONE_NORTH_WEST_TM_22', 1095: 'ITEM_ABANDONED_SHIP_ROOMS_1F_HARBOR_MAIL', 1096: 'ITEM_ABANDONED_SHIP_ROOMS_B1F_ESCAPE_ROPE', 1097: 'ITEM_ABANDONED_SHIP_ROOMS_2_B1F_DIVE_BALL', 1098: 'ITEM_ABANDONED_SHIP_ROOMS_B1F_TM_13', 1099: 'ITEM_ABANDONED_SHIP_ROOMS_2_1F_REVIVE', 1100: 'ITEM_ABANDONED_SHIP_CAPTAINS_OFFICE_STORAGE_KEY', 1101: 'ITEM_ABANDONED_SHIP_HIDDEN_FLOOR_ROOM_3_WATER_STONE', 1102: 'ITEM_ABANDONED_SHIP_HIDDEN_FLOOR_ROOM_1_TM_18', 1103: 'ITEM_ROUTE_121_CARBOS', 1104: 'ITEM_ROUTE_123_ULTRA_BALL', 1105: 'ITEM_ROUTE_126_GREEN_SHARD', 1106: 'ITEM_ROUTE_119_HYPER_POTION_2', 1107: 'ITEM_ROUTE_120_HYPER_POTION', 1108: 'ITEM_ROUTE_120_NEST_BALL', 1109: 'ITEM_ROUTE_123_ELIXIR', 1110: 'ITEM_NEW_MAUVILLE_THUNDER_STONE', 1111: 'ITEM_FIERY_PATH_FIRE_STONE', 1112: 'ITEM_SHOAL_CAVE_ICE_ROOM_TM_07', 1113: 'ITEM_SHOAL_CAVE_ICE_ROOM_NEVER_MELT_ICE', 1114: 'ITEM_ROUTE_103_GUARD_SPEC', 1115: 'ITEM_ROUTE_104_X_ACCURACY', 1116: 'ITEM_MAUVILLE_CITY_X_SPEED', 1117: 'ITEM_PETALBURD_WOODS_PARALYZE_HEAL', 1118: 'ITEM_ROUTE_115_GREAT_BALL', 1119: 'ITEM_SAFARI_ZONE_NORTH_CALCIUM', 1120: 'ITEM_MT_PYRE_3F_SUPER_REPEL', 1121: 'ITEM_ROUTE_118_HYPER_POTION', 1122: 'ITEM_NEW_MAUVILLE_FULL_HEAL', 1123: 'ITEM_NEW_MAUVILLE_PARALYZE_HEAL', 1124: 'ITEM_AQUA_HIDEOUT_B1F_MASTER_BALL', 1125: '_UNUSED', 1126: '_UNUSED', 1127: '_UNUSED', 1128: '_UNUSED', 1129: 'ITEM_MT_PYRE_2F_ULTRA_BALL', 1130: 'ITEM_MT_PYRE_4F_SEA_INCENSE', 1131: 'ITEM_SAFARI_ZONE_SOUTH_WEST_MAX_REVIVE', 1132: 'ITEM_AQUA_HIDEOUT_B1F_NUGGET', 1133: '_UNUSED', 1134: 'ITEM_ROUTE_119_NUGGET', 1135: 'ITEM_ROUTE_104_POTION', 1136: '_UNUSED', 1137: 'ITEM_ROUTE_103_PP_UP', 1138: '_UNUSED', 1139: 'ITEM_ROUTE_108_STAR_PIECE', 1140: 'ITEM_ROUTE_109_POTION', 1141: 'ITEM_ROUTE_110_ELIXIR', 1142: 'ITEM_ROUTE_111_ELIXIR', 1143: 'ITEM_ROUTE_113_HYPER_POTION', 1144: 'ITEM_ROUTE_115_HEAL_POWDER', 1145: '_UNUSED', 1146: 'ITEM_ROUTE_116_POTION', 1147: 'ITEM_ROUTE_119_ELIXIR_2', 1148: 'ITEM_ROUTE_120_REVIVE', 1149: 'ITEM_ROUTE_121_REVIVE', 1150: 'ITEM_ROUTE_121_ZINC', 1151: 'ITEM_MAGMA_HIDEOUT_1F_RARE_CANDY', 1152: 'ITEM_ROUTE_123_PP_UP', 1153: 'ITEM_ROUTE_123_REVIVAL_HERB', 1154: 'ITEM_ROUTE_125_BIG_PEARL', 1155: 'ITEM_ROUTE_127_RARE_CANDY', 1156: 'ITEM_ROUTE_132_PROTEIN', 1157: 'ITEM_ROUTE_133_MAX_REVIVE', 1158: 'ITEM_ROUTE_134_CARBOS', 1159: 'ITEM_ROUTE_134_STAR_PIECE', 1160: 'ITEM_ROUTE_114_ENERGY_POWDER', 1161: 'ITEM_ROUTE_115_PP_UP', 1162: 'ITEM_ARTISAN_CAVE_B1F_HP_UP', 1163: 'ITEM_ARTISAN_CAVE_1F_CARBOS', 1164: 'ITEM_MAGMA_HIDEOUT_2F_2R_MAX_ELIXIR', 1165: 'ITEM_MAGMA_HIDEOUT_2F_2R_FULL_RESTORE', 1166: 'ITEM_MAGMA_HIDEOUT_3F_1R_NUGGET', 1167: 'ITEM_MAGMA_HIDEOUT_3F_2R_PP_MAX', 1168: 'ITEM_MAGMA_HIDEOUT_4F_MAX_REVIVE', 1169: 'ITEM_SAFARI_ZONE_NORTH_EAST_NUGGET', 1170: 'ITEM_SAFARI_ZONE_SOUTH_EAST_BIG_PEARL', 1171: '_UNUSED', 1172: '_UNUSED', 1173: '_UNUSED', 1174: '_UNUSED', 1175: '_UNUSED', 1176: '_UNUSED', 1177: '_UNUSED', 1178: '_UNUSED', 1179: '_UNUSED', 1180: '_UNUSED', 1181: '_UNUSED', 1182: '_UNUSED', 1183: '_UNUSED', 1184: '_UNUSED', 1185: '_UNUSED', 1186: '_UNUSED', 1187: '_UNUSED', 1188: '_UNUSED', 1189: '_UNUSED', 1190: '_UNUSED', 1191: '_UNUSED', 1192: '_UNUSED', 1193: '_UNUSED', 1194: '_UNUSED', 1195: '_UNUSED', 1196: '_UNUSED', 1197: '_UNUSED', 1198: '_UNUSED', 1199: '_UNUSED', 1200: '_UNUSED', 1201: '_UNUSED', 1202: '_UNUSED', 1203: '_UNUSED', 1204: '_UNUSED', 1205: '_UNUSED', 1206: '_UNUSED', 1207: '_UNUSED', 1208: '_UNUSED', 1209: '_UNUSED', 1210: '_UNUSED', 1211: '_UNUSED', 1212: '_UNUSED', 1213: '_UNUSED', 1214: '_UNUSED', 1215: '_UNUSED', 1216: '_UNUSED', 1217: '_UNUSED', 1218: '_UNUSED', 1219: '_UNUSED', 1220: '_UNUSED', 1221: '_UNUSED', 1222: '_UNUSED', 1223: '_UNUSED', 1224: '_UNUSED', 1225: '_UNUSED', 1226: '_UNUSED', 1227: '_UNUSED', 1228: '_UNUSED', 1229: '_UNUSED', 1230: '_UNUSED', 1231: '_UNUSED', 1232: '_UNUSED', 1233: '_UNUSED', 1234: '_UNUSED', 1235: '_UNUSED', 1236: '_UNUSED', 1237: '_UNUSED', 1238: '_UNUSED', 1239: '_UNUSED', 1240: '_UNUSED', 1241: '_UNUSED', 1242: '_UNUSED', 1243: '_UNUSED', 1244: '_UNUSED', 1245: '_UNUSED', 1246: '_UNUSED', 1247: '_UNUSED', 1248: '_UNUSED', 1249: '_UNUSED', 1250: '_UNUSED', 1251: '_UNUSED', 1252: '_UNUSED', 1253: '_UNUSED', 1254: '_UNUSED', 1255: '_UNUSED', 1256: '_UNUSED', 1257: '_UNUSED', 1258: '_UNUSED', 1259: '_UNUSED', 1260: '_UNUSED', 1261: '_UNUSED', 1262: '_UNUSED', 1263: '_UNUSED', 1264: 'DEFEATED_RUSTBORO_GYM', 1265: 'DEFEATED_DEWFORD_GYM', 1266: 'DEFEATED_MAUVILLE_GYM', 1267: 'DEFEATED_LAVARIDGE_GYM', 1268: 'DEFEATED_PETALBURG_GYM', 1269: 'DEFEATED_FORTREE_GYM', 1270: 'DEFEATED_MOSSDEEP_GYM', 1271: 'DEFEATED_SOOTOPOLIS_GYM', 1272: 'DEFEATED_METEOR_FALLS_STEVEN', 1273: '_UNUSED', 1274: '_UNUSED', 1275: 'DEFEATED_ELITE_4_SIDNEY', 1276: 'DEFEATED_ELITE_4_PHOEBE', 1277: 'DEFEATED_ELITE_4_GLACIA', 1278: 'DEFEATED_ELITE_4_DRAKE', 1279: '_UNUSED', 1280: 'TRAINER_NONE', 1281: 'TRAINER_SAWYER_1', 1282: 'TRAINER_GRUNT_AQUA_HIDEOUT_1', 1283: 'TRAINER_GRUNT_AQUA_HIDEOUT_2', 1284: 'TRAINER_GRUNT_AQUA_HIDEOUT_3', 1285: 'TRAINER_GRUNT_AQUA_HIDEOUT_4', 1286: 'TRAINER_GRUNT_SEAFLOOR_CAVERN_1', 1287: 'TRAINER_GRUNT_SEAFLOOR_CAVERN_2', 1288: 'TRAINER_GRUNT_SEAFLOOR_CAVERN_3', 1289: 'TRAINER_GABRIELLE_1', 1290: 'TRAINER_GRUNT_PETALBURG_WOODS', 1291: 'TRAINER_MARCEL', 1292: 'TRAINER_ALBERTO', 1293: 'TRAINER_ED', 1294: 'TRAINER_GRUNT_SEAFLOOR_CAVERN_4', 1295: 'TRAINER_DECLAN', 1296: 'TRAINER_GRUNT_RUSTURF_TUNNEL', 1297: 'TRAINER_GRUNT_WEATHER_INST_1', 1298: 'TRAINER_GRUNT_WEATHER_INST_2', 1299: 'TRAINER_GRUNT_WEATHER_INST_3', 1300: 'TRAINER_GRUNT_MUSEUM_1', 1301: 'TRAINER_GRUNT_MUSEUM_2', 1302: 'TRAINER_GRUNT_SPACE_CENTER_1', 1303: 'TRAINER_GRUNT_MT_PYRE_1', 1304: 'TRAINER_GRUNT_MT_PYRE_2', 1305: 'TRAINER_GRUNT_MT_PYRE_3', 1306: 'TRAINER_GRUNT_WEATHER_INST_4', 1307: 'TRAINER_GRUNT_AQUA_HIDEOUT_5', 1308: 'TRAINER_GRUNT_AQUA_HIDEOUT_6', 1309: 'TRAINER_FREDRICK', 1310: 'TRAINER_MATT', 1311: 'TRAINER_ZANDER', 1312: 'TRAINER_SHELLY_WEATHER_INSTITUTE', 1313: 'TRAINER_SHELLY_SEAFLOOR_CAVERN', 1314: 'TRAINER_ARCHIE', 1315: 'TRAINER_LEAH', 1316: 'TRAINER_DAISY', 1317: 'TRAINER_ROSE_1', 1318: 'TRAINER_FELIX', 1319: 'TRAINER_VIOLET', 1320: 'TRAINER_ROSE_2', 1321: 'TRAINER_ROSE_3', 1322: 'TRAINER_ROSE_4', 1323: 'TRAINER_ROSE_5', 1324: 'TRAINER_DUSTY_1', 1325: 'TRAINER_CHIP', 1326: 'TRAINER_FOSTER', 1327: 'TRAINER_DUSTY_2', 1328: 'TRAINER_DUSTY_3', 1329: 'TRAINER_DUSTY_4', 1330: 'TRAINER_DUSTY_5', 1331: 'TRAINER_GABBY_AND_TY_1', 1332: 'TRAINER_GABBY_AND_TY_2', 1333: 'TRAINER_GABBY_AND_TY_3', 1334: 'TRAINER_GABBY_AND_TY_4', 1335: 'TRAINER_GABBY_AND_TY_5', 1336: 'TRAINER_GABBY_AND_TY_6', 1337: 'TRAINER_LOLA_1', 1338: 'TRAINER_AUSTINA', 1339: 'TRAINER_GWEN', 1340: 'TRAINER_LOLA_2', 1341: 'TRAINER_LOLA_3', 1342: 'TRAINER_LOLA_4', 1343: 'TRAINER_LOLA_5', 1344: 'TRAINER_RICKY_1', 1345: 'TRAINER_SIMON', 1346: 'TRAINER_CHARLIE', 1347: 'TRAINER_RICKY_2', 1348: 'TRAINER_RICKY_3', 1349: 'TRAINER_RICKY_4', 1350: 'TRAINER_RICKY_5', 1351: 'TRAINER_RANDALL', 1352: 'TRAINER_PARKER', 1353: 'TRAINER_GEORGE', 1354: 'TRAINER_BERKE', 1355: 'TRAINER_BRAXTON', 1356: 'TRAINER_VINCENT', 1357: 'TRAINER_LEROY', 1358: 'TRAINER_WILTON_1', 1359: 'TRAINER_EDGAR', 1360: 'TRAINER_ALBERT', 1361: 'TRAINER_SAMUEL', 1362: 'TRAINER_VITO', 1363: 'TRAINER_OWEN', 1364: 'TRAINER_WILTON_2', 1365: 'TRAINER_WILTON_3', 1366: 'TRAINER_WILTON_4', 1367: 'TRAINER_WILTON_5', 1368: 'TRAINER_WARREN', 1369: 'TRAINER_MARY', 1370: 'TRAINER_ALEXIA', 1371: 'TRAINER_JODY', 1372: 'TRAINER_WENDY', 1373: 'TRAINER_KEIRA', 1374: 'TRAINER_BROOKE_1', 1375: 'TRAINER_JENNIFER', 1376: 'TRAINER_HOPE', 1377: 'TRAINER_SHANNON', 1378: 'TRAINER_MICHELLE', 1379: 'TRAINER_CAROLINE', 1380: 'TRAINER_JULIE', 1381: 'TRAINER_BROOKE_2', 1382: 'TRAINER_BROOKE_3', 1383: 'TRAINER_BROOKE_4', 1384: 'TRAINER_BROOKE_5', 1385: 'TRAINER_PATRICIA', 1386: 'TRAINER_KINDRA', 1387: 'TRAINER_TAMMY', 1388: 'TRAINER_VALERIE_1', 1389: 'TRAINER_TASHA', 1390: 'TRAINER_VALERIE_2', 1391: 'TRAINER_VALERIE_3', 1392: 'TRAINER_VALERIE_4', 1393: 'TRAINER_VALERIE_5', 1394: 'TRAINER_CINDY_1', 1395: 'TRAINER_DAPHNE', 1396: 'TRAINER_GRUNT_SPACE_CENTER_2', 1397: 'TRAINER_CINDY_2', 1398: 'TRAINER_BRIANNA', 1399: 'TRAINER_NAOMI', 1400: 'TRAINER_CINDY_3', 1401: 'TRAINER_CINDY_4', 1402: 'TRAINER_CINDY_5', 1403: 'TRAINER_CINDY_6', 1404: 'TRAINER_MELISSA', 1405: 'TRAINER_SHEILA', 1406: 'TRAINER_SHIRLEY', 1407: 'TRAINER_JESSICA_1', 1408: 'TRAINER_CONNIE', 1409: 'TRAINER_BRIDGET', 1410: 'TRAINER_OLIVIA', 1411: 'TRAINER_TIFFANY', 1412: 'TRAINER_JESSICA_2', 1413: 'TRAINER_JESSICA_3', 1414: 'TRAINER_JESSICA_4', 1415: 'TRAINER_JESSICA_5', 1416: 'TRAINER_WINSTON_1', 1417: 'TRAINER_MOLLIE', 1418: 'TRAINER_GARRET', 1419: 'TRAINER_WINSTON_2', 1420: 'TRAINER_WINSTON_3', 1421: 'TRAINER_WINSTON_4', 1422: 'TRAINER_WINSTON_5', 1423: 'TRAINER_STEVE_1', 1424: 'TRAINER_THALIA_1', 1425: 'TRAINER_MARK', 1426: 'TRAINER_GRUNT_MT_CHIMNEY_1', 1427: 'TRAINER_STEVE_2', 1428: 'TRAINER_STEVE_3', 1429: 'TRAINER_STEVE_4', 1430: 'TRAINER_STEVE_5', 1431: 'TRAINER_LUIS', 1432: 'TRAINER_DOMINIK', 1433: 'TRAINER_DOUGLAS', 1434: 'TRAINER_DARRIN', 1435: 'TRAINER_TONY_1', 1436: 'TRAINER_JEROME', 1437: 'TRAINER_MATTHEW', 1438: 'TRAINER_DAVID', 1439: 'TRAINER_SPENCER', 1440: 'TRAINER_ROLAND', 1441: 'TRAINER_NOLEN', 1442: 'TRAINER_STAN', 1443: 'TRAINER_BARRY', 1444: 'TRAINER_DEAN', 1445: 'TRAINER_RODNEY', 1446: 'TRAINER_RICHARD', 1447: 'TRAINER_HERMAN', 1448: 'TRAINER_SANTIAGO', 1449: 'TRAINER_GILBERT', 1450: 'TRAINER_FRANKLIN', 1451: 'TRAINER_KEVIN', 1452: 'TRAINER_JACK', 1453: 'TRAINER_DUDLEY', 1454: 'TRAINER_CHAD', 1455: 'TRAINER_TONY_2', 1456: 'TRAINER_TONY_3', 1457: 'TRAINER_TONY_4', 1458: 'TRAINER_TONY_5', 1459: 'TRAINER_TAKAO', 1460: 'TRAINER_HITOSHI', 1461: 'TRAINER_KIYO', 1462: 'TRAINER_KOICHI', 1463: 'TRAINER_NOB_1', 1464: 'TRAINER_NOB_2', 1465: 'TRAINER_NOB_3', 1466: 'TRAINER_NOB_4', 1467: 'TRAINER_NOB_5', 1468: 'TRAINER_YUJI', 1469: 'TRAINER_DAISUKE', 1470: 'TRAINER_ATSUSHI', 1471: 'TRAINER_KIRK', 1472: 'TRAINER_GRUNT_AQUA_HIDEOUT_7', 1473: 'TRAINER_GRUNT_AQUA_HIDEOUT_8', 1474: 'TRAINER_SHAWN', 1475: 'TRAINER_FERNANDO_1', 1476: 'TRAINER_DALTON_1', 1477: 'TRAINER_DALTON_2', 1478: 'TRAINER_DALTON_3', 1479: 'TRAINER_DALTON_4', 1480: 'TRAINER_DALTON_5', 1481: 'TRAINER_COLE', 1482: 'TRAINER_JEFF', 1483: 'TRAINER_AXLE', 1484: 'TRAINER_JACE', 1485: 'TRAINER_KEEGAN', 1486: 'TRAINER_BERNIE_1', 1487: 'TRAINER_BERNIE_2', 1488: 'TRAINER_BERNIE_3', 1489: 'TRAINER_BERNIE_4', 1490: 'TRAINER_BERNIE_5', 1491: 'TRAINER_DREW', 1492: 'TRAINER_BEAU', 1493: 'TRAINER_LARRY', 1494: 'TRAINER_SHANE', 1495: 'TRAINER_JUSTIN', 1496: 'TRAINER_ETHAN_1', 1497: 'TRAINER_AUTUMN', 1498: 'TRAINER_TRAVIS', 1499: 'TRAINER_ETHAN_2', 1500: 'TRAINER_ETHAN_3', 1501: 'TRAINER_ETHAN_4', 1502: 'TRAINER_ETHAN_5', 1503: 'TRAINER_BRENT', 1504: 'TRAINER_DONALD', 1505: 'TRAINER_TAYLOR', 1506: 'TRAINER_JEFFREY_1', 1507: 'TRAINER_DEREK', 1508: 'TRAINER_JEFFREY_2', 1509: 'TRAINER_JEFFREY_3', 1510: 'TRAINER_JEFFREY_4', 1511: 'TRAINER_JEFFREY_5', 1512: 'TRAINER_EDWARD', 1513: 'TRAINER_PRESTON', 1514: 'TRAINER_VIRGIL', 1515: 'TRAINER_BLAKE', 1516: 'TRAINER_WILLIAM', 1517: 'TRAINER_JOSHUA', 1518: 'TRAINER_CAMERON_1', 1519: 'TRAINER_CAMERON_2', 1520: 'TRAINER_CAMERON_3', 1521: 'TRAINER_CAMERON_4', 1522: 'TRAINER_CAMERON_5', 1523: 'TRAINER_JACLYN', 1524: 'TRAINER_HANNAH', 1525: 'TRAINER_SAMANTHA', 1526: 'TRAINER_MAURA', 1527: 'TRAINER_KAYLA', 1528: 'TRAINER_ALEXIS', 1529: 'TRAINER_JACKI_1', 1530: 'TRAINER_JACKI_2', 1531: 'TRAINER_JACKI_3', 1532: 'TRAINER_JACKI_4', 1533: 'TRAINER_JACKI_5', 1534: 'TRAINER_WALTER_1', 1535: 'TRAINER_MICAH', 1536: 'TRAINER_THOMAS', 1537: 'TRAINER_WALTER_2', 1538: 'TRAINER_WALTER_3', 1539: 'TRAINER_WALTER_4', 1540: 'TRAINER_WALTER_5', 1541: 'TRAINER_SIDNEY', 1542: 'TRAINER_PHOEBE', 1543: 'TRAINER_GLACIA', 1544: 'TRAINER_DRAKE', 1545: 'TRAINER_ROXANNE_1', 1546: 'TRAINER_BRAWLY_1', 1547: 'TRAINER_WATTSON_1', 1548: 'TRAINER_FLANNERY_1', 1549: 'TRAINER_NORMAN_1', 1550: 'TRAINER_WINONA_1', 1551: 'TRAINER_TATE_AND_LIZA_1', 1552: 'TRAINER_JUAN_1', 1553: 'TRAINER_JERRY_1', 1554: 'TRAINER_TED', 1555: 'TRAINER_PAUL', 1556: 'TRAINER_JERRY_2', 1557: 'TRAINER_JERRY_3', 1558: 'TRAINER_JERRY_4', 1559: 'TRAINER_JERRY_5', 1560: 'TRAINER_KAREN_1', 1561: 'TRAINER_GEORGIA', 1562: 'TRAINER_KAREN_2', 1563: 'TRAINER_KAREN_3', 1564: 'TRAINER_KAREN_4', 1565: 'TRAINER_KAREN_5', 1566: 'TRAINER_KATE_AND_JOY', 1567: 'TRAINER_ANNA_AND_MEG_1', 1568: 'TRAINER_ANNA_AND_MEG_2', 1569: 'TRAINER_ANNA_AND_MEG_3', 1570: 'TRAINER_ANNA_AND_MEG_4', 1571: 'TRAINER_ANNA_AND_MEG_5', 1572: 'TRAINER_VICTOR', 1573: 'TRAINER_MIGUEL_1', 1574: 'TRAINER_COLTON', 1575: 'TRAINER_MIGUEL_2', 1576: 'TRAINER_MIGUEL_3', 1577: 'TRAINER_MIGUEL_4', 1578: 'TRAINER_MIGUEL_5', 1579: 'TRAINER_VICTORIA', 1580: 'TRAINER_VANESSA', 1581: 'TRAINER_BETHANY', 1582: 'TRAINER_ISABEL_1', 1583: 'TRAINER_ISABEL_2', 1584: 'TRAINER_ISABEL_3', 1585: 'TRAINER_ISABEL_4', 1586: 'TRAINER_ISABEL_5', 1587: 'TRAINER_TIMOTHY_1', 1588: 'TRAINER_TIMOTHY_2', 1589: 'TRAINER_TIMOTHY_3', 1590: 'TRAINER_TIMOTHY_4', 1591: 'TRAINER_TIMOTHY_5', 1592: 'TRAINER_VICKY', 1593: 'TRAINER_SHELBY_1', 1594: 'TRAINER_SHELBY_2', 1595: 'TRAINER_SHELBY_3', 1596: 'TRAINER_SHELBY_4', 1597: 'TRAINER_SHELBY_5', 1598: 'TRAINER_CALVIN_1', 1599: 'TRAINER_BILLY', 1600: 'TRAINER_JOSH', 1601: 'TRAINER_TOMMY', 1602: 'TRAINER_JOEY', 1603: 'TRAINER_BEN', 1604: 'TRAINER_QUINCY', 1605: 'TRAINER_KATELYNN', 1606: 'TRAINER_JAYLEN', 1607: 'TRAINER_DILLON', 1608: 'TRAINER_CALVIN_2', 1609: 'TRAINER_CALVIN_3', 1610: 'TRAINER_CALVIN_4', 1611: 'TRAINER_CALVIN_5', 1612: 'TRAINER_EDDIE', 1613: 'TRAINER_ALLEN', 1614: 'TRAINER_TIMMY', 1615: 'TRAINER_WALLACE', 1616: 'TRAINER_ANDREW', 1617: 'TRAINER_IVAN', 1618: 'TRAINER_CLAUDE', 1619: 'TRAINER_ELLIOT_1', 1620: 'TRAINER_NED', 1621: 'TRAINER_DALE', 1622: 'TRAINER_NOLAN', 1623: 'TRAINER_BARNY', 1624: 'TRAINER_WADE', 1625: 'TRAINER_CARTER', 1626: 'TRAINER_ELLIOT_2', 1627: 'TRAINER_ELLIOT_3', 1628: 'TRAINER_ELLIOT_4', 1629: 'TRAINER_ELLIOT_5', 1630: 'TRAINER_RONALD', 1631: 'TRAINER_JACOB', 1632: 'TRAINER_ANTHONY', 1633: 'TRAINER_BENJAMIN_1', 1634: 'TRAINER_BENJAMIN_2', 1635: 'TRAINER_BENJAMIN_3', 1636: 'TRAINER_BENJAMIN_4', 1637: 'TRAINER_BENJAMIN_5', 1638: 'TRAINER_ABIGAIL_1', 1639: 'TRAINER_JASMINE', 1640: 'TRAINER_ABIGAIL_2', 1641: 'TRAINER_ABIGAIL_3', 1642: 'TRAINER_ABIGAIL_4', 1643: 'TRAINER_ABIGAIL_5', 1644: 'TRAINER_DYLAN_1', 1645: 'TRAINER_DYLAN_2', 1646: 'TRAINER_DYLAN_3', 1647: 'TRAINER_DYLAN_4', 1648: 'TRAINER_DYLAN_5', 1649: 'TRAINER_MARIA_1', 1650: 'TRAINER_MARIA_2', 1651: 'TRAINER_MARIA_3', 1652: 'TRAINER_MARIA_4', 1653: 'TRAINER_MARIA_5', 1654: 'TRAINER_CAMDEN', 1655: 'TRAINER_DEMETRIUS', 1656: 'TRAINER_ISAIAH_1', 1657: 'TRAINER_PABLO_1', 1658: 'TRAINER_CHASE', 1659: 'TRAINER_ISAIAH_2', 1660: 'TRAINER_ISAIAH_3', 1661: 'TRAINER_ISAIAH_4', 1662: 'TRAINER_ISAIAH_5', 1663: 'TRAINER_ISOBEL', 1664: 'TRAINER_DONNY', 1665: 'TRAINER_TALIA', 1666: 'TRAINER_KATELYN_1', 1667: 'TRAINER_ALLISON', 1668: 'TRAINER_KATELYN_2', 1669: 'TRAINER_KATELYN_3', 1670: 'TRAINER_KATELYN_4', 1671: 'TRAINER_KATELYN_5', 1672: 'TRAINER_NICOLAS_1', 1673: 'TRAINER_NICOLAS_2', 1674: 'TRAINER_NICOLAS_3', 1675: 'TRAINER_NICOLAS_4', 1676: 'TRAINER_NICOLAS_5', 1677: 'TRAINER_AARON', 1678: 'TRAINER_PERRY', 1679: 'TRAINER_HUGH', 1680: 'TRAINER_PHIL', 1681: 'TRAINER_JARED', 1682: 'TRAINER_HUMBERTO', 1683: 'TRAINER_PRESLEY', 1684: 'TRAINER_EDWARDO', 1685: 'TRAINER_COLIN', 1686: 'TRAINER_ROBERT_1', 1687: 'TRAINER_BENNY', 1688: 'TRAINER_CHESTER', 1689: 'TRAINER_ROBERT_2', 1690: 'TRAINER_ROBERT_3', 1691: 'TRAINER_ROBERT_4', 1692: 'TRAINER_ROBERT_5', 1693: 'TRAINER_ALEX', 1694: 'TRAINER_BECK', 1695: 'TRAINER_YASU', 1696: 'TRAINER_TAKASHI', 1697: 'TRAINER_DIANNE', 1698: 'TRAINER_JANI', 1699: 'TRAINER_LAO_1', 1700: 'TRAINER_LUNG', 1701: 'TRAINER_LAO_2', 1702: 'TRAINER_LAO_3', 1703: 'TRAINER_LAO_4', 1704: 'TRAINER_LAO_5', 1705: 'TRAINER_JOCELYN', 1706: 'TRAINER_LAURA', 1707: 'TRAINER_CYNDY_1', 1708: 'TRAINER_CORA', 1709: 'TRAINER_PAULA', 1710: 'TRAINER_CYNDY_2', 1711: 'TRAINER_CYNDY_3', 1712: 'TRAINER_CYNDY_4', 1713: 'TRAINER_CYNDY_5', 1714: 'TRAINER_MADELINE_1', 1715: 'TRAINER_CLARISSA', 1716: 'TRAINER_ANGELICA', 1717: 'TRAINER_MADELINE_2', 1718: 'TRAINER_MADELINE_3', 1719: 'TRAINER_MADELINE_4', 1720: 'TRAINER_MADELINE_5', 1721: 'TRAINER_BEVERLY', 1722: 'TRAINER_IMANI', 1723: 'TRAINER_KYLA', 1724: 'TRAINER_DENISE', 1725: 'TRAINER_BETH', 1726: 'TRAINER_TARA', 1727: 'TRAINER_MISSY', 1728: 'TRAINER_ALICE', 1729: 'TRAINER_JENNY_1', 1730: 'TRAINER_GRACE', 1731: 'TRAINER_TANYA', 1732: 'TRAINER_SHARON', 1733: 'TRAINER_NIKKI', 1734: 'TRAINER_BRENDA', 1735: 'TRAINER_KATIE', 1736: 'TRAINER_SUSIE', 1737: 'TRAINER_KARA', 1738: 'TRAINER_DANA', 1739: 'TRAINER_SIENNA', 1740: 'TRAINER_DEBRA', 1741: 'TRAINER_LINDA', 1742: 'TRAINER_KAYLEE', 1743: 'TRAINER_LAUREL', 1744: 'TRAINER_CARLEE', 1745: 'TRAINER_JENNY_2', 1746: 'TRAINER_JENNY_3', 1747: 'TRAINER_JENNY_4', 1748: 'TRAINER_JENNY_5', 1749: 'TRAINER_HEIDI', 1750: 'TRAINER_BECKY', 1751: 'TRAINER_CAROL', 1752: 'TRAINER_NANCY', 1753: 'TRAINER_MARTHA', 1754: 'TRAINER_DIANA_1', 1755: 'TRAINER_CEDRIC', 1756: 'TRAINER_IRENE', 1757: 'TRAINER_DIANA_2', 1758: 'TRAINER_DIANA_3', 1759: 'TRAINER_DIANA_4', 1760: 'TRAINER_DIANA_5', 1761: 'TRAINER_AMY_AND_LIV_1', 1762: 'TRAINER_AMY_AND_LIV_2', 1763: 'TRAINER_GINA_AND_MIA_1', 1764: 'TRAINER_MIU_AND_YUKI', 1765: 'TRAINER_AMY_AND_LIV_3', 1766: 'TRAINER_GINA_AND_MIA_2', 1767: 'TRAINER_AMY_AND_LIV_4', 1768: 'TRAINER_AMY_AND_LIV_5', 1769: 'TRAINER_AMY_AND_LIV_6', 1770: 'TRAINER_HUEY', 1771: 'TRAINER_EDMOND', 1772: 'TRAINER_ERNEST_1', 1773: 'TRAINER_DWAYNE', 1774: 'TRAINER_PHILLIP', 1775: 'TRAINER_LEONARD', 1776: 'TRAINER_DUNCAN', 1777: 'TRAINER_ERNEST_2', 1778: 'TRAINER_ERNEST_3', 1779: 'TRAINER_ERNEST_4', 1780: 'TRAINER_ERNEST_5', 1781: 'TRAINER_ELI', 1782: 'TRAINER_ANNIKA', 1783: 'TRAINER_JAZMYN', 1784: 'TRAINER_JONAS', 1785: 'TRAINER_KAYLEY', 1786: 'TRAINER_AURON', 1787: 'TRAINER_KELVIN', 1788: 'TRAINER_MARLEY', 1789: 'TRAINER_REYNA', 1790: 'TRAINER_HUDSON', 1791: 'TRAINER_CONOR', 1792: 'TRAINER_EDWIN_1', 1793: 'TRAINER_HECTOR', 1794: 'TRAINER_TABITHA_MOSSDEEP', 1795: 'TRAINER_EDWIN_2', 1796: 'TRAINER_EDWIN_3', 1797: 'TRAINER_EDWIN_4', 1798: 'TRAINER_EDWIN_5', 1799: 'TRAINER_WALLY_VR_1', 1800: 'TRAINER_BRENDAN_ROUTE_103_MUDKIP', 1801: 'TRAINER_BRENDAN_ROUTE_110_MUDKIP', 1802: 'TRAINER_BRENDAN_ROUTE_119_MUDKIP', 1803: 'TRAINER_BRENDAN_ROUTE_103_TREECKO', 1804: 'TRAINER_BRENDAN_ROUTE_110_TREECKO', 1805: 'TRAINER_BRENDAN_ROUTE_119_TREECKO', 1806: 'TRAINER_BRENDAN_ROUTE_103_TORCHIC', 1807: 'TRAINER_BRENDAN_ROUTE_110_TORCHIC', 1808: 'TRAINER_BRENDAN_ROUTE_119_TORCHIC', 1809: 'TRAINER_MAY_ROUTE_103_MUDKIP', 1810: 'TRAINER_MAY_ROUTE_110_MUDKIP', 1811: 'TRAINER_MAY_ROUTE_119_MUDKIP', 1812: 'TRAINER_MAY_ROUTE_103_TREECKO', 1813: 'TRAINER_MAY_ROUTE_110_TREECKO', 1814: 'TRAINER_MAY_ROUTE_119_TREECKO', 1815: 'TRAINER_MAY_ROUTE_103_TORCHIC', 1816: 'TRAINER_MAY_ROUTE_110_TORCHIC', 1817: 'TRAINER_MAY_ROUTE_119_TORCHIC', 1818: 'TRAINER_ISAAC_1', 1819: 'TRAINER_DAVIS', 1820: 'TRAINER_MITCHELL', 1821: 'TRAINER_ISAAC_2', 1822: 'TRAINER_ISAAC_3', 1823: 'TRAINER_ISAAC_4', 1824: 'TRAINER_ISAAC_5', 1825: 'TRAINER_LYDIA_1', 1826: 'TRAINER_HALLE', 1827: 'TRAINER_GARRISON', 1828: 'TRAINER_LYDIA_2', 1829: 'TRAINER_LYDIA_3', 1830: 'TRAINER_LYDIA_4', 1831: 'TRAINER_LYDIA_5', 1832: 'TRAINER_JACKSON_1', 1833: 'TRAINER_LORENZO', 1834: 'TRAINER_SEBASTIAN', 1835: 'TRAINER_JACKSON_2', 1836: 'TRAINER_JACKSON_3', 1837: 'TRAINER_JACKSON_4', 1838: 'TRAINER_JACKSON_5', 1839: 'TRAINER_CATHERINE_1', 1840: 'TRAINER_JENNA', 1841: 'TRAINER_SOPHIA', 1842: 'TRAINER_CATHERINE_2', 1843: 'TRAINER_CATHERINE_3', 1844: 'TRAINER_CATHERINE_4', 1845: 'TRAINER_CATHERINE_5', 1846: 'TRAINER_JULIO', 1847: 'TRAINER_GRUNT_SEAFLOOR_CAVERN_5', 1848: 'TRAINER_GRUNT_UNUSED', 1849: 'TRAINER_GRUNT_MT_PYRE_4', 1850: 'TRAINER_GRUNT_JAGGED_PASS', 1851: 'TRAINER_MARC', 1852: 'TRAINER_BRENDEN', 1853: 'TRAINER_LILITH', 1854: 'TRAINER_CRISTIAN', 1855: 'TRAINER_SYLVIA', 1856: 'TRAINER_LEONARDO', 1857: 'TRAINER_ATHENA', 1858: 'TRAINER_HARRISON', 1859: 'TRAINER_GRUNT_MT_CHIMNEY_2', 1860: 'TRAINER_CLARENCE', 1861: 'TRAINER_TERRY', 1862: 'TRAINER_NATE', 1863: 'TRAINER_KATHLEEN', 1864: 'TRAINER_CLIFFORD', 1865: 'TRAINER_NICHOLAS', 1866: 'TRAINER_GRUNT_SPACE_CENTER_3', 1867: 'TRAINER_GRUNT_SPACE_CENTER_4', 1868: 'TRAINER_GRUNT_SPACE_CENTER_5', 1869: 'TRAINER_GRUNT_SPACE_CENTER_6', 1870: 'TRAINER_GRUNT_SPACE_CENTER_7', 1871: 'TRAINER_MACEY', 1872: 'TRAINER_BRENDAN_RUSTBORO_TREECKO', 1873: 'TRAINER_BRENDAN_RUSTBORO_MUDKIP', 1874: 'TRAINER_PAXTON', 1875: 'TRAINER_ISABELLA', 1876: 'TRAINER_GRUNT_WEATHER_INST_5', 1877: 'TRAINER_TABITHA_MT_CHIMNEY', 1878: 'TRAINER_JONATHAN', 1879: 'TRAINER_BRENDAN_RUSTBORO_TORCHIC', 1880: 'TRAINER_MAY_RUSTBORO_MUDKIP', 1881: 'TRAINER_MAXIE_MAGMA_HIDEOUT', 1882: 'TRAINER_MAXIE_MT_CHIMNEY', 1883: 'TRAINER_TIANA', 1884: 'TRAINER_HALEY_1', 1885: 'TRAINER_JANICE', 1886: 'TRAINER_VIVI', 1887: 'TRAINER_HALEY_2', 1888: 'TRAINER_HALEY_3', 1889: 'TRAINER_HALEY_4', 1890: 'TRAINER_HALEY_5', 1891: 'TRAINER_SALLY', 1892: 'TRAINER_ROBIN', 1893: 'TRAINER_ANDREA', 1894: 'TRAINER_CRISSY', 1895: 'TRAINER_RICK', 1896: 'TRAINER_LYLE', 1897: 'TRAINER_JOSE', 1898: 'TRAINER_DOUG', 1899: 'TRAINER_GREG', 1900: 'TRAINER_KENT', 1901: 'TRAINER_JAMES_1', 1902: 'TRAINER_JAMES_2', 1903: 'TRAINER_JAMES_3', 1904: 'TRAINER_JAMES_4', 1905: 'TRAINER_JAMES_5', 1906: 'TRAINER_BRICE', 1907: 'TRAINER_TRENT_1', 1908: 'TRAINER_LENNY', 1909: 'TRAINER_LUCAS_1', 1910: 'TRAINER_ALAN', 1911: 'TRAINER_CLARK', 1912: 'TRAINER_ERIC', 1913: 'TRAINER_LUCAS_2', 1914: 'TRAINER_MIKE_1', 1915: 'TRAINER_MIKE_2', 1916: 'TRAINER_TRENT_2', 1917: 'TRAINER_TRENT_3', 1918: 'TRAINER_TRENT_4', 1919: 'TRAINER_TRENT_5', 1920: 'TRAINER_DEZ_AND_LUKE', 1921: 'TRAINER_LEA_AND_JED', 1922: 'TRAINER_KIRA_AND_DAN_1', 1923: 'TRAINER_KIRA_AND_DAN_2', 1924: 'TRAINER_KIRA_AND_DAN_3', 1925: 'TRAINER_KIRA_AND_DAN_4', 1926: 'TRAINER_KIRA_AND_DAN_5', 1927: 'TRAINER_JOHANNA', 1928: 'TRAINER_GERALD', 1929: 'TRAINER_VIVIAN', 1930: 'TRAINER_DANIELLE', 1931: 'TRAINER_HIDEO', 1932: 'TRAINER_KEIGO', 1933: 'TRAINER_RILEY', 1934: 'TRAINER_FLINT', 1935: 'TRAINER_ASHLEY', 1936: 'TRAINER_WALLY_MAUVILLE', 1937: 'TRAINER_WALLY_VR_2', 1938: 'TRAINER_WALLY_VR_3', 1939: 'TRAINER_WALLY_VR_4', 1940: 'TRAINER_WALLY_VR_5', 1941: 'TRAINER_BRENDAN_LILYCOVE_MUDKIP', 1942: 'TRAINER_BRENDAN_LILYCOVE_TREECKO', 1943: 'TRAINER_BRENDAN_LILYCOVE_TORCHIC', 1944: 'TRAINER_MAY_LILYCOVE_MUDKIP', 1945: 'TRAINER_MAY_LILYCOVE_TREECKO', 1946: 'TRAINER_MAY_LILYCOVE_TORCHIC', 1947: 'TRAINER_JONAH', 1948: 'TRAINER_HENRY', 1949: 'TRAINER_ROGER', 1950: 'TRAINER_ALEXA', 1951: 'TRAINER_RUBEN', 1952: 'TRAINER_KOJI_1', 1953: 'TRAINER_WAYNE', 1954: 'TRAINER_AIDAN', 1955: 'TRAINER_REED', 1956: 'TRAINER_TISHA', 1957: 'TRAINER_TORI_AND_TIA', 1958: 'TRAINER_KIM_AND_IRIS', 1959: 'TRAINER_TYRA_AND_IVY', 1960: 'TRAINER_MEL_AND_PAUL', 1961: 'TRAINER_JOHN_AND_JAY_1', 1962: 'TRAINER_JOHN_AND_JAY_2', 1963: 'TRAINER_JOHN_AND_JAY_3', 1964: 'TRAINER_JOHN_AND_JAY_4', 1965: 'TRAINER_JOHN_AND_JAY_5', 1966: 'TRAINER_RELI_AND_IAN', 1967: 'TRAINER_LILA_AND_ROY_1', 1968: 'TRAINER_LILA_AND_ROY_2', 1969: 'TRAINER_LILA_AND_ROY_3', 1970: 'TRAINER_LILA_AND_ROY_4', 1971: 'TRAINER_LILA_AND_ROY_5', 1972: 'TRAINER_LISA_AND_RAY', 1973: 'TRAINER_CHRIS', 1974: 'TRAINER_DAWSON', 1975: 'TRAINER_SARAH', 1976: 'TRAINER_DARIAN', 1977: 'TRAINER_HAILEY', 1978: 'TRAINER_CHANDLER', 1979: 'TRAINER_KALEB', 1980: 'TRAINER_JOSEPH', 1981: 'TRAINER_ALYSSA', 1982: 'TRAINER_MARCOS', 1983: 'TRAINER_RHETT', 1984: 'TRAINER_TYRON', 1985: 'TRAINER_CELINA', 1986: 'TRAINER_BIANCA', 1987: 'TRAINER_HAYDEN', 1988: 'TRAINER_SOPHIE', 1989: 'TRAINER_COBY', 1990: 'TRAINER_LAWRENCE', 1991: 'TRAINER_WYATT', 1992: 'TRAINER_ANGELINA', 1993: 'TRAINER_KAI', 1994: 'TRAINER_CHARLOTTE', 1995: 'TRAINER_DEANDRE', 1996: 'TRAINER_GRUNT_MAGMA_HIDEOUT_1', 1997: 'TRAINER_GRUNT_MAGMA_HIDEOUT_2', 1998: 'TRAINER_GRUNT_MAGMA_HIDEOUT_3', 1999: 'TRAINER_GRUNT_MAGMA_HIDEOUT_4', 2000: 'TRAINER_GRUNT_MAGMA_HIDEOUT_5', 2001: 'TRAINER_GRUNT_MAGMA_HIDEOUT_6', 2002: 'TRAINER_GRUNT_MAGMA_HIDEOUT_7', 2003: 'TRAINER_GRUNT_MAGMA_HIDEOUT_8', 2004: 'TRAINER_GRUNT_MAGMA_HIDEOUT_9', 2005: 'TRAINER_GRUNT_MAGMA_HIDEOUT_10', 2006: 'TRAINER_GRUNT_MAGMA_HIDEOUT_11', 2007: 'TRAINER_GRUNT_MAGMA_HIDEOUT_12', 2008: 'TRAINER_GRUNT_MAGMA_HIDEOUT_13', 2009: 'TRAINER_GRUNT_MAGMA_HIDEOUT_14', 2010: 'TRAINER_GRUNT_MAGMA_HIDEOUT_15', 2011: 'TRAINER_GRUNT_MAGMA_HIDEOUT_16', 2012: 'TRAINER_TABITHA_MAGMA_HIDEOUT', 2013: 'TRAINER_DARCY', 2014: 'TRAINER_MAXIE_MOSSDEEP', 2015: 'TRAINER_PETE', 2016: 'TRAINER_ISABELLE', 2017: 'TRAINER_ANDRES_1', 2018: 'TRAINER_JOSUE', 2019: 'TRAINER_CAMRON', 2020: 'TRAINER_CORY_1', 2021: 'TRAINER_CAROLINA', 2022: 'TRAINER_ELIJAH', 2023: 'TRAINER_CELIA', 2024: 'TRAINER_BRYAN', 2025: 'TRAINER_BRANDEN', 2026: 'TRAINER_BRYANT', 2027: 'TRAINER_SHAYLA', 2028: 'TRAINER_KYRA', 2029: 'TRAINER_JAIDEN', 2030: 'TRAINER_ALIX', 2031: 'TRAINER_HELENE', 2032: 'TRAINER_MARLENE', 2033: 'TRAINER_DEVAN', 2034: 'TRAINER_JOHNSON', 2035: 'TRAINER_MELINA', 2036: 'TRAINER_BRANDI', 2037: 'TRAINER_AISHA', 2038: 'TRAINER_MAKAYLA', 2039: 'TRAINER_FABIAN', 2040: 'TRAINER_DAYTON', 2041: 'TRAINER_RACHEL', 2042: 'TRAINER_LEONEL', 2043: 'TRAINER_CALLIE', 2044: 'TRAINER_CALE', 2045: 'TRAINER_MYLES', 2046: 'TRAINER_PAT', 2047: 'TRAINER_CRISTIN_1', 2048: 'TRAINER_MAY_RUSTBORO_TREECKO', 2049: 'TRAINER_MAY_RUSTBORO_TORCHIC', 2050: 'TRAINER_ROXANNE_2', 2051: 'TRAINER_ROXANNE_3', 2052: 'TRAINER_ROXANNE_4', 2053: 'TRAINER_ROXANNE_5', 2054: 'TRAINER_BRAWLY_2', 2055: 'TRAINER_BRAWLY_3', 2056: 'TRAINER_BRAWLY_4', 2057: 'TRAINER_BRAWLY_5', 2058: 'TRAINER_WATTSON_2', 2059: 'TRAINER_WATTSON_3', 2060: 'TRAINER_WATTSON_4', 2061: 'TRAINER_WATTSON_5', 2062: 'TRAINER_FLANNERY_2', 2063: 'TRAINER_FLANNERY_3', 2064: 'TRAINER_FLANNERY_4', 2065: 'TRAINER_FLANNERY_5', 2066: 'TRAINER_NORMAN_2', 2067: 'TRAINER_NORMAN_3', 2068: 'TRAINER_NORMAN_4', 2069: 'TRAINER_NORMAN_5', 2070: 'TRAINER_WINONA_2', 2071: 'TRAINER_WINONA_3', 2072: 'TRAINER_WINONA_4', 2073: 'TRAINER_WINONA_5', 2074: 'TRAINER_TATE_AND_LIZA_2', 2075: 'TRAINER_TATE_AND_LIZA_3', 2076: 'TRAINER_TATE_AND_LIZA_4', 2077: 'TRAINER_TATE_AND_LIZA_5', 2078: 'TRAINER_JUAN_2', 2079: 'TRAINER_JUAN_3', 2080: 'TRAINER_JUAN_4', 2081: 'TRAINER_JUAN_5', 2082: 'TRAINER_ANGELO', 2083: 'TRAINER_DARIUS', 2084: 'TRAINER_STEVEN', 2085: 'TRAINER_ANABEL', 2086: 'TRAINER_TUCKER', 2087: 'TRAINER_SPENSER', 2088: 'TRAINER_GRETA', 2089: 'TRAINER_NOLAND', 2090: 'TRAINER_LUCY', 2091: 'TRAINER_BRANDON', 2092: 'TRAINER_ANDRES_2', 2093: 'TRAINER_ANDRES_3', 2094: 'TRAINER_ANDRES_4', 2095: 'TRAINER_ANDRES_5', 2096: 'TRAINER_CORY_2', 2097: 'TRAINER_CORY_3', 2098: 'TRAINER_CORY_4', 2099: 'TRAINER_CORY_5', 2100: 'TRAINER_PABLO_2', 2101: 'TRAINER_PABLO_3', 2102: 'TRAINER_PABLO_4', 2103: 'TRAINER_PABLO_5', 2104: 'TRAINER_KOJI_2', 2105: 'TRAINER_KOJI_3', 2106: 'TRAINER_KOJI_4', 2107: 'TRAINER_KOJI_5', 2108: 'TRAINER_CRISTIN_2', 2109: 'TRAINER_CRISTIN_3', 2110: 'TRAINER_CRISTIN_4', 2111: 'TRAINER_CRISTIN_5', 2112: 'TRAINER_FERNANDO_2', 2113: 'TRAINER_FERNANDO_3', 2114: 'TRAINER_FERNANDO_4', 2115: 'TRAINER_FERNANDO_5', 2116: 'TRAINER_SAWYER_2', 2117: 'TRAINER_SAWYER_3', 2118: 'TRAINER_SAWYER_4', 2119: 'TRAINER_SAWYER_5', 2120: 'TRAINER_GABRIELLE_2', 2121: 'TRAINER_GABRIELLE_3', 2122: 'TRAINER_GABRIELLE_4', 2123: 'TRAINER_GABRIELLE_5', 2124: 'TRAINER_THALIA_2', 2125: 'TRAINER_THALIA_3', 2126: 'TRAINER_THALIA_4', 2127: 'TRAINER_THALIA_5', 2128: 'TRAINER_MARIELA', 2129: 'TRAINER_ALVARO', 2130: 'TRAINER_EVERETT', 2131: 'TRAINER_RED', 2132: 'TRAINER_LEAF', 2133: 'TRAINER_BRENDAN_PLACEHOLDER', 2134: 'TRAINER_MAY_PLACEHOLDER', 2135: '_UNUSED', 2136: '_UNUSED', 2137: '_UNUSED', 2138: '_UNUSED', 2139: '_UNUSED', 2140: '_UNUSED', 2141: '_UNUSED', 2142: '_UNUSED', 2143: '_UNUSED', 2144: 'SYS_POKEMON_GET', 2145: 'SYS_POKEDEX_GET', 2146: 'SYS_POKENAV_GET', 2147: '_UNUSED', 2148: 'SYS_GAME_CLEAR', 2149: 'SYS_CHAT_USED', 2150: 'SYS_HIPSTER_MEET', 2151: 'BADGE01_GET', 2152: 'BADGE02_GET', 2153: 'BADGE03_GET', 2154: 'BADGE04_GET', 2155: 'BADGE05_GET', 2156: 'BADGE06_GET', 2157: 'BADGE07_GET', 2158: 'BADGE08_GET', 2159: 'VISITED_LITTLEROOT_TOWN', 2160: 'VISITED_OLDALE_TOWN', 2161: 'VISITED_DEWFORD_TOWN', 2162: 'VISITED_LAVARIDGE_TOWN', 2163: 'VISITED_FALLARBOR_TOWN', 2164: 'VISITED_VERDANTURF_TOWN', 2165: 'VISITED_PACIFIDLOG_TOWN', 2166: 'VISITED_PETALBURG_CITY', 2167: 'VISITED_SLATEPORT_CITY', 2168: 'VISITED_MAUVILLE_CITY', 2169: 'VISITED_RUSTBORO_CITY', 2170: 'VISITED_FORTREE_CITY', 2171: 'VISITED_LILYCOVE_CITY', 2172: 'VISITED_MOSSDEEP_CITY', 2173: 'VISITED_SOOTOPOLIS_CITY', 2174: 'VISITED_EVER_GRANDE_CITY', 2175: 'IS_CHAMPION', 2176: 'NURSE_UNION_ROOM_REMINDER', 2177: '_UNUSED', 2178: '_UNUSED', 2179: '_UNUSED', 2180: '_UNUSED', 2181: '_UNUSED', 2182: '_UNUSED', 2183: '_UNUSED', 2184: 'SYS_USE_FLASH', 2185: 'SYS_USE_STRENGTH', 2186: 'SYS_WEATHER_CTRL', 2187: 'SYS_CYCLING_ROAD', 2188: 'SYS_SAFARI_MODE', 2189: 'SYS_CRUISE_MODE', 2190: '_UNUSED', 2191: '_UNUSED', 2192: 'SYS_TV_HOME', 2193: 'SYS_TV_WATCH', 2194: 'SYS_TV_START', 2195: 'SYS_CHANGED_DEWFORD_TREND', 2196: 'SYS_MIX_RECORD', 2197: 'SYS_CLOCK_SET', 2198: 'SYS_NATIONAL_DEX', 2199: '_UNUSED', 2200: '_UNUSED', 2201: '_UNUSED', 2202: 'SYS_SHOAL_TIDE', 2203: 'SYS_RIBBON_GET', 2204: 'LANDMARK_FLOWER_SHOP', 2205: 'LANDMARK_MR_BRINEY_HOUSE', 2206: 'LANDMARK_ABANDONED_SHIP', 2207: 'LANDMARK_SEASHORE_HOUSE', 2208: 'LANDMARK_NEW_MAUVILLE', 2209: 'LANDMARK_OLD_LADY_REST_SHOP', 2210: 'LANDMARK_TRICK_HOUSE', 2211: 'LANDMARK_WINSTRATE_FAMILY', 2212: 'LANDMARK_GLASS_WORKSHOP', 2213: 'LANDMARK_LANETTES_HOUSE', 2214: 'LANDMARK_POKEMON_DAYCARE', 2215: 'LANDMARK_SEAFLOOR_CAVERN', 2216: 'LANDMARK_BATTLE_FRONTIER', 2217: 'LANDMARK_SOUTHERN_ISLAND', 2218: 'LANDMARK_FIERY_PATH', 2219: 'SYS_PC_LANETTE', 2220: 'SYS_MYSTERY_EVENT_ENABLE', 2221: 'SYS_ENC_UP_ITEM', 2222: 'SYS_ENC_DOWN_ITEM', 2223: 'SYS_BRAILLE_DIG', 2224: 'SYS_REGIROCK_PUZZLE_COMPLETED', 2225: 'SYS_BRAILLE_REGICE_COMPLETED', 2226: 'SYS_REGISTEEL_PUZZLE_COMPLETED', 2227: 'ENABLE_SHIP_SOUTHERN_ISLAND', 2228: 'LANDMARK_POKEMON_LEAGUE', 2229: 'LANDMARK_ISLAND_CAVE', 2230: 'LANDMARK_DESERT_RUINS', 2231: 'LANDMARK_FOSSIL_MANIACS_HOUSE', 2232: 'LANDMARK_SCORCHED_SLAB', 2233: 'LANDMARK_ANCIENT_TOMB', 2234: 'LANDMARK_TUNNELERS_REST_HOUSE', 2235: 'LANDMARK_HUNTERS_HOUSE', 2236: 'LANDMARK_SEALED_CHAMBER', 2237: 'SYS_TV_LATIAS_LATIOS', 2238: 'LANDMARK_SKY_PILLAR', 2239: 'SYS_SHOAL_ITEM', 2240: 'SYS_B_DASH', 2241: 'SYS_CTRL_OBJ_DELETE', 2242: 'SYS_RESET_RTC_ENABLE', 2243: 'LANDMARK_BERRY_MASTERS_HOUSE', 2244: 'SYS_TOWER_SILVER', 2245: 'SYS_TOWER_GOLD', 2246: 'SYS_DOME_SILVER', 2247: 'SYS_DOME_GOLD', 2248: 'SYS_PALACE_SILVER', 2249: 'SYS_PALACE_GOLD', 2250: 'SYS_ARENA_SILVER', 2251: 'SYS_ARENA_GOLD', 2252: 'SYS_FACTORY_SILVER', 2253: 'SYS_FACTORY_GOLD', 2254: 'SYS_PIKE_SILVER', 2255: 'SYS_PIKE_GOLD', 2256: 'SYS_PYRAMID_SILVER', 2257: 'SYS_PYRAMID_GOLD', 2258: 'SYS_FRONTIER_PASS', 2259: 'MAP_SCRIPT_CHECKED_DEOXYS', 2260: 'DEOXYS_ROCK_COMPLETE', 2261: 'ENABLE_SHIP_BIRTH_ISLAND', 2262: 'ENABLE_SHIP_FARAWAY_ISLAND', 2263: 'SHOWN_BOX_WAS_FULL_MESSAGE', 2264: 'ARRIVED_ON_FARAWAY_ISLAND', 2265: 'ARRIVED_AT_MARINE_CAVE_EMERGE_SPOT', 2266: 'ARRIVED_AT_TERRA_CAVE_ENTRANCE', 2267: 'SYS_MYSTERY_GIFT_ENABLE', 2268: 'ENTERED_MIRAGE_TOWER', 2269: 'LANDMARK_ALTERING_CAVE', 2270: 'LANDMARK_DESERT_UNDERPASS', 2271: 'LANDMARK_ARTISAN_CAVE', 2272: 'ENABLE_SHIP_NAVEL_ROCK', 2273: 'ARRIVED_AT_NAVEL_ROCK', 2274: 'LANDMARK_TRAINER_HILL', 2275: '_UNUSED', 2276: 'RECEIVED_POKEDEX_FROM_BIRCH', 2277: '_UNUSED', 2278: '_UNUSED', 2279: '_UNUSED', 2280: '_UNUSED', 2281: '_UNUSED', 2282: '_UNUSED', 2283: '_UNUSED', 2284: '_UNUSED', 2285: '_UNUSED', 2286: '_UNUSED', 2287: '_UNUSED', 2288: '_UNUSED', 2289: '_UNUSED', 2290: '_UNUSED', 2291: '_UNUSED', 2292: '_UNUSED', 2293: '_UNUSED', 2294: '_UNUSED', 2295: '_UNUSED', 2296: '_UNUSED', 2297: '_UNUSED', 2298: '_UNUSED', 2299: '_UNUSED', 2300: '_UNUSED', 2301: '_UNUSED', 2302: '_UNUSED', 2303: '_UNUSED', 2304: '_UNUSED', 2305: '_UNUSED', 2306: '_UNUSED', 2307: '_UNUSED', 2308: '_UNUSED', 2309: '_UNUSED', 2310: '_UNUSED', 2311: '_UNUSED', 2312: '_UNUSED', 2313: '_UNUSED', 2314: '_UNUSED', 2315: '_UNUSED', 2316: '_UNUSED', 2317: '_UNUSED', 2318: '_UNUSED', 2319: '_UNUSED', 2320: '_UNUSED', 2321: '_UNUSED', 2322: '_UNUSED', 2323: '_UNUSED', 2324: '_UNUSED', 2325: '_UNUSED', 2326: '_UNUSED', 2327: '_UNUSED', 2328: '_UNUSED', 2329: '_UNUSED', 2330: '_UNUSED', 2331: '_UNUSED', 2332: '_UNUSED', 2333: '_UNUSED', 2334: '_UNUSED', 2335: '_UNUSED', 2336: '_UNUSED', 2337: 'DAILY_CONTEST_LOBBY_RECEIVED_BERRY', 2338: 'DAILY_SECRET_BASE', 2339: '_UNUSED', 2340: '_UNUSED', 2341: '_UNUSED', 2342: '_UNUSED', 2343: '_UNUSED', 2344: '_UNUSED', 2345: '_UNUSED', 2346: 'DAILY_PICKED_LOTO_TICKET', 2347: 'DAILY_ROUTE_114_RECEIVED_BERRY', 2348: 'DAILY_ROUTE_111_RECEIVED_BERRY', 2349: 'DAILY_BERRY_MASTER_RECEIVED_BERRY', 2350: 'DAILY_ROUTE_120_RECEIVED_BERRY', 2351: 'DAILY_LILYCOVE_RECEIVED_BERRY', 2352: 'DAILY_FLOWER_SHOP_RECEIVED_BERRY', 2353: 'DAILY_BERRY_MASTERS_WIFE', 2354: 'DAILY_SOOTOPOLIS_RECEIVED_BERRY', 2355: '_UNUSED', 2356: 'DAILY_APPRENTICE_LEAVES', 2357: '_UNUSED', 2358: '_UNUSED', 2359: '_UNUSED', 2360: '_UNUSED', 2361: '_UNUSED', 2362: '_UNUSED', 2363: '_UNUSED', 2364: '_UNUSED', 2365: '_UNUSED', 2366: '_UNUSED', 2367: '_UNUSED', 2368: '_UNUSED', 2369: '_UNUSED', 2370: '_UNUSED', 2371: '_UNUSED', 2372: '_UNUSED', 2373: '_UNUSED', 2374: '_UNUSED', 2375: '_UNUSED', 2376: '_UNUSED', 2377: '_UNUSED', 2378: '_UNUSED', 2379: '_UNUSED', 2380: '_UNUSED', 2381: '_UNUSED', 2382: '_UNUSED', 2383: '_UNUSED', 2384: '_UNUSED', 2385: '_UNUSED', 2386: '_UNUSED', 2387: '_UNUSED', 2388: '_UNUSED', 2389: '_UNUSED', 2390: '_UNUSED', 2391: '_UNUSED', 2392: '_UNUSED', 2393: '_UNUSED', 2394: '_UNUSED', 2395: '_UNUSED', 2396: '_UNUSED', 2397: '_UNUSED', 2398: '_UNUSED', 2399: '_UNUSED'}

sid_index = {0: 'None', 1: 'Bulbasaur', 2: 'Ivysaur', 3: 'Venusaur', 4: 'Charmander', 5: 'Charmeleon', 6: 'Charizard', 7: 'Squirtle', 8: 'Wartortle', 9: 'Blastoise', 10: 'Caterpie', 11: 'Metapod', 12: 'Butterfree', 13: 'Weedle', 14: 'Kakuna', 15: 'Beedrill', 16: 'Pidgey', 17: 'Pidgeotto', 18: 'Pidgeot', 19: 'Rattata', 20: 'Raticate', 21: 'Spearow', 22: 'Fearow', 23: 'Ekans', 24: 'Arbok', 25: 'Pikachu', 26: 'Raichu', 27: 'Sandshrew', 28: 'Sandslash', 29: 'Nidoran♀', 30: 'Nidorina', 31: 'Nidoqueen', 32: 'Nidoran♂', 33: 'Nidorino', 34: 'Nidoking', 35: 'Clefairy', 36: 'Clefable', 37: 'Vulpix', 38: 'Ninetales', 39: 'Jigglypuff', 40: 'Wigglytuff', 41: 'Zubat', 42: 'Golbat', 43: 'Oddish', 44: 'Gloom', 45: 'Vileplume', 46: 'Paras', 47: 'Parasect', 48: 'Venonat', 49: 'Venomoth', 50: 'Diglett', 51: 'Dugtrio', 52: 'Meowth', 53: 'Persian', 54: 'Psyduck', 55: 'Golduck', 56: 'Mankey', 57: 'Primeape', 58: 'Growlithe', 59: 'Arcanine', 60: 'Poliwag', 61: 'Poliwhirl', 62: 'Poliwrath', 63: 'Abra', 64: 'Kadabra', 65: 'Alakazam', 66: 'Machop', 67: 'Machoke', 68: 'Machamp', 69: 'Bellsprout', 70: 'Weepinbell', 71: 'Victreebel', 72: 'Tentacool', 73: 'Tentacruel', 74: 'Geodude', 75: 'Graveler', 76: 'Golem', 77: 'Ponyta', 78: 'Rapidash', 79: 'Slowpoke', 80: 'Slowbro', 81: 'Magnemite', 82: 'Magneton', 83: 'Farfetchd', 84: 'Doduo', 85: 'Dodrio', 86: 'Seel', 87: 'Dewgong', 88: 'Grimer', 89: 'Muk', 90: 'Shellder', 91: 'Cloyster', 92: 'Gastly', 93: 'Haunter', 94: 'Gengar', 95: 'Onix', 96: 'Drowzee', 97: 'Hypno', 98: 'Krabby', 99: 'Kingler', 100: 'Voltorb', 101: 'Electrode', 102: 'Exeggcute', 103: 'Exeggutor', 104: 'Cubone', 105: 'Marowak', 106: 'Hitmonlee', 107: 'Hitmonchan', 108: 'Lickitung', 109: 'Koffing', 110: 'Weezing', 111: 'Rhyhorn', 112: 'Rhydon', 113: 'Chansey', 114: 'Tangela', 115: 'Kangaskhan', 116: 'Horsea', 117: 'Seadra', 118: 'Goldeen', 119: 'Seaking', 120: 'Staryu', 121: 'Starmie', 122: 'Mr Mime', 123: 'Scyther', 124: 'Jynx', 125: 'Electabuzz', 126: 'Magmar', 127: 'Pinsir', 128: 'Tauros', 129: 'Magikarp', 130: 'Gyarados', 131: 'Lapras', 132: 'Ditto', 133: 'Eevee', 134: 'Vaporeon', 135: 'Jolteon', 136: 'Flareon', 137: 'Porygon', 138: 'Omanyte', 139: 'Omastar', 140: 'Kabuto', 141: 'Kabutops', 142: 'Aerodactyl', 143: 'Snorlax', 144: 'Articuno', 145: 'Zapdos', 146: 'Moltres', 147: 'Dratini', 148: 'Dragonair', 149: 'Dragonite', 150: 'Mewtwo', 151: 'Mew', 152: 'Chikorita', 153: 'Bayleef', 154: 'Meganium', 155: 'Cyndaquil', 156: 'Quilava', 157: 'Typhlosion', 158: 'Totodile', 159: 'Croconaw', 160: 'Feraligatr', 161: 'Sentret', 162: 'Furret', 163: 'Hoothoot', 164: 'Noctowl', 165: 'Ledyba', 166: 'Ledian', 167: 'Spinarak', 168: 'Ariados', 169: 'Crobat', 170: 'Chinchou', 171: 'Lanturn', 172: 'Pichu', 173: 'Cleffa', 174: 'Igglybuff', 175: 'Togepi', 176: 'Togetic', 177: 'Natu', 178: 'Xatu', 179: 'Mareep', 180: 'Flaaffy', 181: 'Ampharos', 182: 'Bellossom', 183: 'Marill', 184: 'Azumarill', 185: 'Sudowoodo', 186: 'Politoed', 187: 'Hoppip', 188: 'Skiploom', 189: 'Jumpluff', 190: 'Aipom', 191: 'Sunkern', 192: 'Sunflora', 193: 'Yanma', 194: 'Wooper', 195: 'Quagsire', 196: 'Espeon', 197: 'Umbreon', 198: 'Murkrow', 199: 'Slowking', 200: 'Misdreavus', 201: 'Unown', 202: 'Wobbuffet', 203: 'Girafarig', 204: 'Pineco', 205: 'Forretress', 206: 'Dunsparce', 207: 'Gligar', 208: 'Steelix', 209: 'Snubbull', 210: 'Granbull', 211: 'Qwilfish', 212: 'Scizor', 213: 'Shuckle', 214: 'Heracross', 215: 'Sneasel', 216: 'Teddiursa', 217: 'Ursaring', 218: 'Slugma', 219: 'Magcargo', 220: 'Swinub', 221: 'Piloswine', 222: 'Corsola', 223: 'Remoraid', 224: 'Octillery', 225: 'Delibird', 226: 'Mantine', 227: 'Skarmory', 228: 'Houndour', 229: 'Houndoom', 230: 'Kingdra', 231: 'Phanpy', 232: 'Donphan', 233: 'Porygon2', 234: 'Stantler', 235: 'Smeargle', 236: 'Tyrogue', 237: 'Hitmontop', 238: 'Smoochum', 239: 'Elekid', 240: 'Magby', 241: 'Miltank', 242: 'Blissey', 243: 'Raikou', 244: 'Entei', 245: 'Suicune', 246: 'Larvitar', 247: 'Pupitar', 248: 'Tyranitar', 249: 'Lugia', 250: 'Ho-Oh', 251: 'Celebi', 252: 'Old Unown B', 253: 'Old Unown C', 254: 'Old Unown D', 255: 'Old Unown E', 256: 'Old Unown F', 257: 'Old Unown G', 258: 'Old Unown H', 259: 'Old Unown I', 260: 'Old Unown J', 261: 'Old Unown K', 262: 'Old Unown L', 263: 'Old Unown M', 264: 'Old Unown N', 265: 'Old Unown O', 266: 'Old Unown P', 267: 'Old Unown Q', 268: 'Old Unown R', 269: 'Old Unown S', 270: 'Old Unown T', 271: 'Old Unown U', 272: 'Old Unown V', 273: 'Old Unown W', 274: 'Old Unown X', 275: 'Old Unown Y', 276: 'Old Unown Z', 277: 'Treecko', 278: 'Grovyle', 279: 'Sceptile', 280: 'Torchic', 281: 'Combusken', 282: 'Blaziken', 283: 'Mudkip', 284: 'Marshtomp', 285: 'Swampert', 286: 'Poochyena', 287: 'Mightyena', 288: 'Zigzagoon', 289: 'Linoone', 290: 'Wurmple', 291: 'Silcoon', 292: 'Beautifly', 293: 'Cascoon', 294: 'Dustox', 295: 'Lotad', 296: 'Lombre', 297: 'Ludicolo', 298: 'Seedot', 299: 'Nuzleaf', 300: 'Shiftry', 301: 'Nincada', 302: 'Ninjask', 303: 'Shedinja', 304: 'Taillow', 305: 'Swellow', 306: 'Shroomish', 307: 'Breloom', 308: 'Spinda', 309: 'Wingull', 310: 'Pelipper', 311: 'Surskit', 312: 'Masquerain', 313: 'Wailmer', 314: 'Wailord', 315: 'Skitty', 316: 'Delcatty', 317: 'Kecleon', 318: 'Baltoy', 319: 'Claydol', 320: 'Nosepass', 321: 'Torkoal', 322: 'Sableye', 323: 'Barboach', 324: 'Whiscash', 325: 'Luvdisc', 326: 'Corphish', 327: 'Crawdaunt', 328: 'Feebas', 329: 'Milotic', 330: 'Carvanha', 331: 'Sharpedo', 332: 'Trapinch', 333: 'Vibrava', 334: 'Flygon', 335: 'Makuhita', 336: 'Hariyama', 337: 'Electrike', 338: 'Manectric', 339: 'Numel', 340: 'Camerupt', 341: 'Spheal', 342: 'Sealeo', 343: 'Walrein', 344: 'Cacnea', 345: 'Cacturne', 346: 'Snorunt', 347: 'Glalie', 348: 'Lunatone', 349: 'Solrock', 350: 'Azurill', 351: 'Spoink', 352: 'Grumpig', 353: 'Plusle', 354: 'Minun', 355: 'Mawile', 356: 'Meditite', 357: 'Medicham', 358: 'Swablu', 359: 'Altaria', 360: 'Wynaut', 361: 'Duskull', 362: 'Dusclops', 363: 'Roselia', 364: 'Slakoth', 365: 'Vigoroth', 366: 'Slaking', 367: 'Gulpin', 368: 'Swalot', 369: 'Tropius', 370: 'Whismur', 371: 'Loudred', 372: 'Exploud', 373: 'Clamperl', 374: 'Huntail', 375: 'Gorebyss', 376: 'Absol', 377: 'Shuppet', 378: 'Banette', 379: 'Seviper', 380: 'Zangoose', 381: 'Relicanth', 382: 'Aron', 383: 'Lairon', 384: 'Aggron', 385: 'Castform', 386: 'Volbeat', 387: 'Illumise', 388: 'Lileep', 389: 'Cradily', 390: 'Anorith', 391: 'Armaldo', 392: 'Ralts', 393: 'Kirlia', 394: 'Gardevoir', 395: 'Bagon', 396: 'Shelgon', 397: 'Salamence', 398: 'Beldum', 399: 'Metang', 400: 'Metagross', 401: 'Regirock', 402: 'Regice', 403: 'Registeel', 404: 'Kyogre', 405: 'Groudon', 406: 'Rayquaza', 407: 'Latias', 408: 'Latios', 409: 'Jirachi', 410: 'Deoxys', 411: 'Chimecho', 412: 'Egg', 413: 'Unown B', 414: 'Unown C', 415: 'Unown D', 416: 'Unown E', 417: 'Unown F', 418: 'Unown G', 419: 'Unown H', 420: 'Unown I', 421: 'Unown J', 422: 'Unown K', 423: 'Unown L', 424: 'Unown M', 425: 'Unown N', 426: 'Unown O', 427: 'Unown P', 428: 'Unown Q', 429: 'Unown R', 430: 'Unown S', 431: 'Unown T', 432: 'Unown U', 433: 'Unown V', 434: 'Unown W', 435: 'Unown X', 436: 'Unown Y', 437: 'Unown Z', 438: 'Unown !', 439: 'Unown ?'}

sid_name = {'None': 0, 'Bulbasaur': 1, 'Ivysaur': 2, 'Venusaur': 3, 'Charmander': 4, 'Charmeleon': 5, 'Charizard': 6, 'Squirtle': 7, 'Wartortle': 8, 'Blastoise': 9, 'Caterpie': 10, 'Metapod': 11, 'Butterfree': 12, 'Weedle': 13, 'Kakuna': 14, 'Beedrill': 15, 'Pidgey': 16, 'Pidgeotto': 17, 'Pidgeot': 18, 'Rattata': 19, 'Raticate': 20, 'Spearow': 21, 'Fearow': 22, 'Ekans': 23, 'Arbok': 24, 'Pikachu': 25, 'Raichu': 26, 'Sandshrew': 27, 'Sandslash': 28, 'Nidoran♀': 29, 'Nidorina': 30, 'Nidoqueen': 31, 'Nidoran♂' : 32, 'Nidorino': 33, 'Nidoking': 34, 'Clefairy': 35, 'Clefable': 36, 'Vulpix': 37, 'Ninetales': 38, 'Jigglypuff': 39, 'Wigglytuff': 40, 'Zubat': 41, 'Golbat': 42, 'Oddish': 43, 'Gloom': 44, 'Vileplume': 45, 'Paras': 46, 'Parasect': 47, 'Venonat': 48, 'Venomoth': 49, 'Diglett': 50, 'Dugtrio': 51, 'Meowth': 52, 'Persian': 53, 'Psyduck': 54, 'Golduck': 55, 'Mankey': 56, 'Primeape': 57, 'Growlithe': 58, 'Arcanine': 59, 'Poliwag': 60, 'Poliwhirl': 61, 'Poliwrath': 62, 'Abra': 63, 'Kadabra': 64, 'Alakazam': 65, 'Machop': 66, 'Machoke': 67, 'Machamp': 68, 'Bellsprout': 69, 'Weepinbell': 70, 'Victreebel': 71, 'Tentacool': 72, 'Tentacruel': 73, 'Geodude': 74, 'Graveler': 75, 'Golem': 76, 'Ponyta': 77, 'Rapidash': 78, 'Slowpoke': 79, 'Slowbro': 80, 'Magnemite': 81, 'Magneton': 82, 'Farfetchd': 83, 'Doduo': 84, 'Dodrio': 85, 'Seel': 86, 'Dewgong': 87, 'Grimer': 88, 'Muk': 89, 'Shellder': 90, 'Cloyster': 91, 'Gastly': 92, 'Haunter': 93, 'Gengar': 94, 'Onix': 95, 'Drowzee': 96, 'Hypno': 97, 'Krabby': 98, 'Kingler': 99, 'Voltorb': 100, 'Electrode': 101, 'Exeggcute': 102, 'Exeggutor': 103, 'Cubone': 104, 'Marowak': 105, 'Hitmonlee': 106, 'Hitmonchan': 107, 'Lickitung': 108, 'Koffing': 109, 'Weezing': 110, 'Rhyhorn': 111, 'Rhydon': 112, 'Chansey': 113, 'Tangela': 114, 'Kangaskhan': 115, 'Horsea': 116, 'Seadra': 117, 'Goldeen': 118, 'Seaking': 119, 'Staryu': 120, 'Starmie': 121, 'Mr Mime': 122, 'Scyther': 123, 'Jynx': 124, 'Electabuzz': 125, 'Magmar': 126, 'Pinsir': 127, 'Tauros': 128, 'Magikarp': 129, 'Gyarados': 130, 'Lapras': 131, 'Ditto': 132, 'Eevee': 133, 'Vaporeon': 134, 'Jolteon': 135, 'Flareon': 136, 'Porygon': 137, 'Omanyte': 138, 'Omastar': 139, 'Kabuto': 140, 'Kabutops': 141, 'Aerodactyl': 142, 'Snorlax': 143, 'Articuno': 144, 'Zapdos': 145, 'Moltres': 146, 'Dratini': 147, 'Dragonair': 148, 'Dragonite': 149, 'Mewtwo': 150, 'Mew': 151, 'Chikorita': 152, 'Bayleef': 153, 'Meganium': 154, 'Cyndaquil': 155, 'Quilava': 156, 'Typhlosion': 157, 'Totodile': 158, 'Croconaw': 159, 'Feraligatr': 160, 'Sentret': 161, 'Furret': 162, 'Hoothoot': 163, 'Noctowl': 164, 'Ledyba': 165, 'Ledian': 166, 'Spinarak': 167, 'Ariados': 168, 'Crobat': 169, 'Chinchou': 170, 'Lanturn': 171, 'Pichu': 172, 'Cleffa': 173, 'Igglybuff': 174, 'Togepi': 175, 'Togetic': 176, 'Natu': 177, 'Xatu': 178, 'Mareep': 179, 'Flaaffy': 180, 'Ampharos': 181, 'Bellossom': 182, 'Marill': 183, 'Azumarill': 184, 'Sudowoodo': 185, 'Politoed': 186, 'Hoppip': 187, 'Skiploom': 188, 'Jumpluff': 189, 'Aipom': 190, 'Sunkern': 191, 'Sunflora': 192, 'Yanma': 193, 'Wooper': 194, 'Quagsire': 195, 'Espeon': 196, 'Umbreon': 197, 'Murkrow': 198, 'Slowking': 199, 'Misdreavus': 200, 'Unown': 201, 'Wobbuffet': 202, 'Girafarig': 203, 'Pineco': 204, 'Forretress': 205, 'Dunsparce': 206, 'Gligar': 207, 'Steelix': 208, 'Snubbull': 209, 'Granbull': 210, 'Qwilfish': 211, 'Scizor': 212, 'Shuckle': 213, 'Heracross': 214, 'Sneasel': 215, 'Teddiursa': 216, 'Ursaring': 217, 'Slugma': 218, 'Magcargo': 219, 'Swinub': 220, 'Piloswine': 221, 'Corsola': 222, 'Remoraid': 223, 'Octillery': 224, 'Delibird': 225, 'Mantine': 226, 'Skarmory': 227, 'Houndour': 228, 'Houndoom': 229, 'Kingdra': 230, 'Phanpy': 231, 'Donphan': 232, 'Porygon2': 233, 'Stantler': 234, 'Smeargle': 235, 'Tyrogue': 236, 'Hitmontop': 237, 'Smoochum': 238, 'Elekid': 239, 'Magby': 240, 'Miltank': 241, 'Blissey': 242, 'Raikou': 243, 'Entei': 244, 'Suicune': 245, 'Larvitar': 246, 'Pupitar': 247, 'Tyranitar': 248, 'Lugia': 249, 'Ho-Oh': 250, 'Celebi': 251, 'Old Unown B': 252, 'Old Unown C': 253, 'Old Unown D': 254, 'Old Unown E': 255, 'Old Unown F': 256, 'Old Unown G': 257, 'Old Unown H': 258, 'Old Unown I': 259, 'Old Unown J': 260, 'Old Unown K': 261, 'Old Unown L': 262, 'Old Unown M': 263, 'Old Unown N': 264, 'Old Unown O': 265, 'Old Unown P': 266, 'Old Unown Q': 267, 'Old Unown R': 268, 'Old Unown S': 269, 'Old Unown T': 270, 'Old Unown U': 271, 'Old Unown V': 272, 'Old Unown W': 273, 'Old Unown X': 274, 'Old Unown Y': 275, 'Old Unown Z': 276, 'Treecko': 277, 'Grovyle': 278, 'Sceptile': 279, 'Torchic': 280, 'Combusken': 281, 'Blaziken': 282, 'Mudkip': 283, 'Marshtomp': 284, 'Swampert': 285, 'Poochyena': 286, 'Mightyena': 287, 'Zigzagoon': 288, 'Linoone': 289, 'Wurmple': 290, 'Silcoon': 291, 'Beautifly': 292, 'Cascoon': 293, 'Dustox': 294, 'Lotad': 295, 'Lombre': 296, 'Ludicolo': 297, 'Seedot': 298, 'Nuzleaf': 299, 'Shiftry': 300, 'Nincada': 301, 'Ninjask': 302, 'Shedinja': 303, 'Taillow': 304, 'Swellow': 305, 'Shroomish': 306, 'Breloom': 307, 'Spinda': 308, 'Wingull': 309, 'Pelipper': 310, 'Surskit': 311, 'Masquerain': 312, 'Wailmer': 313, 'Wailord': 314, 'Skitty': 315, 'Delcatty': 316, 'Kecleon': 317, 'Baltoy': 318, 'Claydol': 319, 'Nosepass': 320, 'Torkoal': 321, 'Sableye': 322, 'Barboach': 323, 'Whiscash': 324, 'Luvdisc': 325, 'Corphish': 326, 'Crawdaunt': 327, 'Feebas': 328, 'Milotic': 329, 'Carvanha': 330, 'Sharpedo': 331, 'Trapinch': 332, 'Vibrava': 333, 'Flygon': 334, 'Makuhita': 335, 'Hariyama': 336, 'Electrike': 337, 'Manectric': 338, 'Numel': 339, 'Camerupt': 340, 'Spheal': 341, 'Sealeo': 342, 'Walrein': 343, 'Cacnea': 344, 'Cacturne': 345, 'Snorunt': 346, 'Glalie': 347, 'Lunatone': 348, 'Solrock': 349, 'Azurill': 350, 'Spoink': 351, 'Grumpig': 352, 'Plusle': 353, 'Minun': 354, 'Mawile': 355, 'Meditite': 356, 'Medicham': 357, 'Swablu': 358, 'Altaria': 359, 'Wynaut': 360, 'Duskull': 361, 'Dusclops': 362, 'Roselia': 363, 'Slakoth': 364, 'Vigoroth': 365, 'Slaking': 366, 'Gulpin': 367, 'Swalot': 368, 'Tropius': 369, 'Whismur': 370, 'Loudred': 371, 'Exploud': 372, 'Clamperl': 373, 'Huntail': 374, 'Gorebyss': 375, 'Absol': 376, 'Shuppet': 377, 'Banette': 378, 'Seviper': 379, 'Zangoose': 380, 'Relicanth': 381, 'Aron': 382, 'Lairon': 383, 'Aggron': 384, 'Castform': 385, 'Volbeat': 386, 'Illumise': 387, 'Lileep': 388, 'Cradily': 389, 'Anorith': 390, 'Armaldo': 391, 'Ralts': 392, 'Kirlia': 393, 'Gardevoir': 394, 'Bagon': 395, 'Shelgon': 396, 'Salamence': 397, 'Beldum': 398, 'Metang': 399, 'Metagross': 400, 'Regirock': 401, 'Regice': 402, 'Registeel': 403, 'Kyogre': 404, 'Groudon': 405, 'Rayquaza': 406, 'Latias': 407, 'Latios': 408, 'Jirachi': 409, 'Deoxys': 410, 'Chimecho': 411, 'Egg': 412, 'Unown B': 413, 'Unown C': 414, 'Unown D': 415, 'Unown E': 416, 'Unown F': 417, 'Unown G': 418, 'Unown H': 419, 'Unown I': 420, 'Unown J': 421, 'Unown K': 422, 'Unown L': 423, 'Unown M': 424, 'Unown N': 425, 'Unown O': 426, 'Unown P': 427, 'Unown Q': 428, 'Unown R': 429, 'Unown S': 430, 'Unown T': 431, 'Unown U': 432, 'Unown V': 433, 'Unown W': 434, 'Unown X': 435, 'Unown Y': 436, 'Unown Z': 437, 'Unown !': 438, 'Unown ?': 439}

hton = {1: 252, 2: 253, 3: 254, 4: 255, 5: 256, 6: 257, 7: 258, 8: 259, 9: 260, 10: 261, 11: 262, 12: 263, 13: 264, 14: 265, 15: 266, 16: 267, 17: 268, 18: 269, 19: 270, 20: 271, 21: 272, 22: 273, 23: 274, 24: 275, 25: 276, 26: 277, 27: 278, 28: 279, 29: 280, 30: 281, 31: 282, 32: 283, 33: 284, 34: 285, 35: 286, 36: 287, 37: 288, 38: 289, 39: 63, 40: 64, 41: 65, 42: 290, 43: 291, 44: 292, 45: 293, 46: 294, 47: 295, 48: 296, 49: 297, 50: 118, 51: 119, 52: 129, 53: 130, 54: 298, 55: 183, 56: 184, 57: 74, 58: 75, 59: 76, 60: 299, 61: 300, 62: 301, 63: 41, 64: 42, 65: 169, 66: 72, 67: 73, 68: 302, 69: 303, 70: 304, 71: 305, 72: 306, 73: 66, 74: 67, 75: 68, 76: 307, 77: 308, 78: 309, 79: 310, 80: 311, 81: 312, 82: 81, 83: 82, 84: 100, 85: 101, 86: 313, 87: 314, 88: 43, 89: 44, 90: 45, 91: 182, 92: 84, 93: 85, 94: 315, 95: 316, 96: 317, 97: 318, 98: 319, 99: 320, 100: 321, 101: 322, 102: 323, 103: 218, 104: 219, 105: 324, 106: 88, 107: 89, 108: 109, 109: 110, 110: 325, 111: 326, 112: 27, 113: 28, 114: 327, 115: 227, 116: 328, 117: 329, 118: 330, 119: 331, 120: 332, 121: 333, 122: 334, 123: 335, 124: 336, 125: 337, 126: 338, 127: 339, 128: 340, 129: 341, 130: 342, 131: 343, 132: 344, 133: 345, 134: 346, 135: 347, 136: 348, 137: 174, 138: 39, 139: 40, 140: 349, 141: 350, 142: 351, 143: 120, 144: 121, 145: 352, 146: 353, 147: 354, 148: 355, 149: 356, 150: 357, 151: 358, 152: 359, 153: 37, 154: 38, 155: 172, 156: 25, 157: 26, 158: 54, 159: 55, 160: 360, 161: 202, 162: 177, 163: 178, 164: 203, 165: 231, 166: 232, 167: 127, 168: 214, 169: 111, 170: 112, 171: 361, 172: 362, 173: 363, 174: 364, 175: 365, 176: 366, 177: 367, 178: 368, 179: 369, 180: 222, 181: 170, 182: 171, 183: 370, 184: 116, 185: 117, 186: 230, 187: 371, 188: 372, 189: 373, 190: 374, 191: 375, 192: 376, 193: 377, 194: 378, 195: 379, 196: 380, 197: 381, 198: 382, 199: 383, 200: 384, 201: 385, 202: 386}

ntoh = {252: 1, 253: 2, 254: 3, 255: 4, 256: 5, 257: 6, 258: 7, 259: 8, 260: 9, 261: 10, 262: 11, 263: 12, 264: 13, 265: 14, 266: 15, 267: 16, 268: 17, 269: 18, 270: 19, 271: 20, 272: 21, 273: 22, 274: 23, 275: 24, 276: 25, 277: 26, 278: 27, 279: 28, 280: 29, 281: 30, 282: 31, 283: 32, 284: 33, 285: 34, 286: 35, 287: 36, 288: 37, 289: 38, 63: 39, 64: 40, 65: 41, 290: 42, 291: 43, 292: 44, 293: 45, 294: 46, 295: 47, 296: 48, 297: 49, 118: 50, 119: 51, 129: 52, 130: 53, 298: 54, 183: 55, 184: 56, 74: 57, 75: 58, 76: 59, 299: 60, 300: 61, 301: 62, 41: 63, 42: 64, 169: 65, 72: 66, 73: 67, 302: 68, 303: 69, 304: 70, 305: 71, 306: 72, 66: 73, 67: 74, 68: 75, 307: 76, 308: 77, 309: 78, 310: 79, 311: 80, 312: 81, 81: 82, 82: 83, 100: 84, 101: 85, 313: 86, 314: 87, 43: 88, 44: 89, 45: 90, 182: 91, 84: 92, 85: 93, 315: 94, 316: 95, 317: 96, 318: 97, 319: 98, 320: 99, 321: 100, 322: 101, 323: 102, 218: 103, 219: 104, 324: 105, 88: 106, 89: 107, 109: 108, 110: 109, 325: 110, 326: 111, 27: 112, 28: 113, 327: 114, 227: 115, 328: 116, 329: 117, 330: 118, 331: 119, 332: 120, 333: 121, 334: 122, 335: 123, 336: 124, 337: 125, 338: 126, 339: 127, 340: 128, 341: 129, 342: 130, 343: 131, 344: 132, 345: 133, 346: 134, 347: 135, 348: 136, 174: 137, 39: 138, 40: 139, 349: 140, 350: 141, 351: 142, 120: 143, 121: 144, 352: 145, 353: 146, 354: 147, 355: 148, 356: 149, 357: 150, 358: 151, 359: 152, 37: 153, 38: 154, 172: 155, 25: 156, 26: 157, 54: 158, 55: 159, 360: 160, 202: 161, 177: 162, 178: 163, 203: 164, 231: 165, 232: 166, 127: 167, 214: 168, 111: 169, 112: 170, 361: 171, 362: 172, 363: 173, 364: 174, 365: 175, 366: 176, 367: 177, 368: 178, 369: 179, 222: 180, 170: 181, 171: 182, 370: 183, 116: 184, 117: 185, 230: 186, 371: 187, 372: 188, 373: 189, 374: 190, 375: 191, 376: 192, 377: 193, 378: 194, 379: 195, 380: 196, 381: 197, 382: 198, 383: 199, 384: 200, 385: 201, 386: 202}

pokeblock_colors = {
	0: 'None',
	1: 'Red',
	2: 'Blue',
	3: 'Pink',
	4: 'Green',
	5: 'Yellow',
	6: 'Purple',
	7: 'Indigo',
	8: 'Brown',
	9: 'Lite Blue',
	10: 'Olive',
	11: 'Gray',
	12: 'Black',
	13: 'White',
	14: 'Gold',
}

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
		sub_sel = menu(main_menu[sel] + ' Menu (Select ' + main_menu[sel] + ' to Edit, ' + str(slots) + ' of ' + str(max_q[pocket]) + ' array elements assigned)',sub_menu,o,max_q[pocket] - slots,count)

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

def edit_number(label, address, length, key, mx=None):
	mx = (2 ** (8 * length)) - 1 if mx is None else mx

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
			party_list.append(poketoascii(sav,name,10))

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
	print(poketoascii(sav,address,length))
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

def poketoascii(array,address,length):
	s = ''
	for i in range(length):
		if array[address+i] == 0xFF: break
		if array[address+i] == 0x00: break
		s += eng_index[array[address+i]]
	s = s.replace('+','♀')
	s = s.replace('^','♂')
	s = s.replace('_','…')

	return s

def sort_all(item_types):
	for i in item_types: sort_items(i)
	return

def pokedex(seen_filter,obtainable_filter):
	address = section_address(0)
	owned  = int.from_bytes(sav[address+pokedex_owned_offset:address+pokedex_owned_offset+49], byteorder='little')
	seen = int.from_bytes(sav[address+pokedex_seen_offset_a:address+pokedex_seen_offset_a+49], byteorder='little')
	nid_list = []
	name_list = []
	current_box, box_mons = dump_lanette_pc()
	party_mons = dump_party()

	print("Seen: {0:d} Owned: {1:d}\n".format(seen.bit_count(),owned.bit_count()))

	for nid in dict(nid_index):
		o = s = " "
		if owned & 1: o = pokeball
		if seen & 1: s = "S"
		owned >>= 1
		seen >>= 1
		if seen_filter and s == " ": continue
		obtainable = ' '
		if nid_obtainable[nid][0] == 'Y': obtainable = nid_obtainable[nid][0]
		if obtainable_filter and obtainable == ' ': continue

		# fugly
		box = '☐'
		for mon in box_mons:
			if nid == mon[4]:
				box = '■'
				break

		# fugly too
		for mon in party_mons:
			if nid == mon[3]:
				box = '●'
				break

		hdex = "    "
		if nid in ntoh.keys():
			format_string = 'H{0:03d}'
			hdex = format_string.format(ntoh[nid])

		format_string = '{0:03d}. {6} {4} {1} {5} {2} {3}'
		nid_list.append(format_string.format(nid,s,o,nid_index[nid],obtainable,box,hdex))

	name_list = nid_list.copy()
	name_list.sort(key = lambda x: x[18:])

	maxlen = len(max(nid_list, key=len))
	for i,j in zip(nid_list, name_list):
		print("%s\t%s" % (i.ljust(maxlen, " "), j))

	print()
	return

def dump_section_data(s):
	a = section_address(s)
	with open('section' + str(s) + '.dump', 'wb') as f: f.write(sav[a:a+3968])
	return

def toggle_flags(used,checked):
	a = section_address(2)

	while True:
		flag_bits = bits = int.from_bytes(sav[a+flags_offset:a+flags_offset+300], byteorder='little')
		flag_index = []
		flag_items = []

		print('Toggle Flags\n')

		for i in range(300 * 0x8):
			o = '☐'
			if bits & 1: o = '■'
			bits >>= 1
			flag = "UNDEFINED"
			if i in flags.keys(): flag = flags[i]
			if not used and flag == '_UNUSED': continue
			if checked == 0 and o == '■': continue
			if checked == 1 and o == '☐': continue
			if flag == "UNDEFINED" and o == '☐': continue
			flag_index.append(i+1)
			flag_items.append("{2:04d} {0} {1}".format(o,flag,i+1))

		flag_items_byname = flag_items.copy()
		flag_items_byname.sort(key = lambda x: x[7:])
		flag_items.sort()

		maxlen = len(max(flag_items, key=len))
		for i,j in zip(flag_items, flag_items_byname):
			print("%s\t%s" % (i.ljust(maxlen, " "), j))

		print()

		while True:
			try:
				e = int(input("Toggle Flag (1-" + str(300 * 0x8) + ") ['0' to Exit]: "))
				if e > 300 * 0x8 or e < 0:
					print("\nOut of range. Try again...\n")
					continue
				if e == 0:
					print()
					return
				if e not in flag_index:
					print("\nInvalid flag. Pick from flags above.\n")
					continue
				break
			except ValueError:
				print("\nNot a number. Try again...\n")
			except Exception as err:
				print(f"Unexpected {err=}, {type(err)=}")
				raise

		flag_bits ^= (1 << (e - 1))
		for i, j in enumerate(flag_bits.to_bytes(300, 'little')): sav[a+flags_offset+i] = j

	print()

	return

def playtime():
	print('Edit Play Time: {0:d}:{1:02d}:{2:02d}:{3:02d}'.format(
		read_number(section_address(0) + 0x0E,2,0x0),
		sav[section_address(0) + 0x10],
		sav[section_address(0) + 0x11],
		sav[section_address(0) + 0x12]
	))

	while True:
		try:
			t = input('New Play Time (hhh:mm:ss:ff): ')
			if len(t) == 0:
				print('\nNo change.\n')
				return
			try:
				h, m, s, f = [abs(int(i)) for i in t.split(":")]
			except ValueError:
				print('\nFormat must be hhh:mm:ss:ff and hhh, mm, ss, ff must be integers.\n')
				continue
			if h > 255:
				print('\nHours (hhh) ' + str(h) + ' > 255.\n')
				continue
			if m > 59:
				print('\nMinutes (mm) ' + str(m) + ' > 59.\n')
				continue
			if s > 59:
				print('\nSeconds (ss) ' + str(s) + ' > 59.\n')
				continue
			if f > 59:
				print('\nFrames (ff) ' + str(f) + ' > 59.\n')
				continue
			break
		except Exception as err:
			print(f"Unexpected {err=}, {type(err)=}")
			raise

	for i, j in enumerate(h.to_bytes(2, 'little')): sav[section_address(0) + 0x0E + i] = j
	sav[section_address(0) + 0x10] = m
	sav[section_address(0) + 0x11] = s
	sav[section_address(0) + 0x12] = f

	print()

	return

def dump_lanette_pc():
	def read_sections():
		pcbox = bytearray()
		for i in range(5,14,1):
			a = section_address(i)
			pcbox += bytearray(sav[a:a+3968])
		return pcbox

	def write_sections(pcbox):
		for i in range(5,14,1):
			a = section_address(i)
			for j in range(3968): sav[a+j] = pcbox[(i-5)*3968 + j]
		return

	pcbox = read_sections()
	current_box = pcbox[0]
	mons = []

	data_g = [0, 0, 0, 0, 0, 0, 1, 1, 2, 3, 2, 3, 1, 1, 2, 3, 2, 3, 1, 1, 2, 3, 2, 3]

	for box in range(14):
		empty = 0
		for index in range(30):
			mon = 4 + box * 80 * 30 + index * 80
			personality = int.from_bytes(pcbox[mon:mon+4], byteorder='little')
			if personality == 0: continue
			otid = int.from_bytes(pcbox[mon+4:mon+8], byteorder='little')
			key = personality ^ otid
			e_data = bytearray(pcbox[mon+0x20:mon+0x20+48])
			data = bytearray()
			for i in range(0,48,4):
				pt = key ^ int.from_bytes(e_data[i:i+4], byteorder='little')
				data += pt.to_bytes(4, 'little')
			g = data_g[personality % 24] * 12
			sid = int.from_bytes(data[g:g+2], byteorder='little')
			item = int.from_bytes(data[g+2:g+4], byteorder='little')
			mons.append([box,index+1,sid,item,nid_name[sid_index[sid]],poketoascii(pcbox,mon+0x8,10)])

	# for future edits
	#write_sections(pcbox)

	return current_box, mons

def lanette_pc_box():
	current_box, mons = dump_lanette_pc()

	print("Lanette's PC [by box]:\n")

	maxmonlen = len(max(sid_index.values(), key=len))
	maxitemlen = len(max(items_index.values(), key=len))
	box = -1
	for mon in mons:
		if box != mon[0]:
			if box != -1: print()
			box = mon[0]
			current_label = ''
			if box == current_box: current_label = '(Current)'
			print('Box: {0} {1}\n'.format(box+1,current_label))
		index = mon[1]
		sid = mon[2]
		item = mon[3]
		nid = mon[4]
		name = mon[5]
		if name.lower() == sid_index[sid].lower(): name = ''
		format_string = '{0:02d}. {1:03d} {4:03d} {2:' + str(maxmonlen) + 's} {5:' + str(maxmonlen) + 's} {3:' + str(maxitemlen) + 's}'
		item_name = items_index[item]
		if item_name == 'NONE': item_name = ''
		print(format_string.format(index+1,sid,sid_index[sid],item_name,nid,name))

	print()
	return

def lanette_pc_name():
	current_box, mons = dump_lanette_pc()
	lines = []

	print("Lanette's PC [by name]:\n")

	maxmonlen = len(max(sid_index.values(), key=len))
	maxitemlen = len(max(items_index.values(), key=len))
	for mon in mons:
		box = mon[0]
		index = mon[1]
		sid = mon[2]
		item = mon[3]
		nid = mon[4]
		name = mon[5]
		if name.lower() == sid_index[sid].lower(): name = ''
		c = ' '
		if box == current_box: c = 'C'
		item_name = items_index[item]
		if item_name == 'NONE': item_name = ''
		format_string = '{0:02d} {1} {2:02d}. {3:03d} {6:03d} {4:' + str(maxmonlen) + 's} {7:' + str(maxmonlen) + 's} {5:' + str(maxitemlen) + 's}'
		lines.append(format_string.format(box+1,c,index+1,sid,sid_index[sid],item_name,nid,name))

	lines.sort(key = lambda x: x[17:])

	for i in lines: print(i)
	print()
	return

def dump_party():
	party_size = read_number(section_address(1) + team_size_offset,4,0)
	data_g = [0, 0, 0, 0, 0, 0, 1, 1, 2, 3, 2, 3, 1, 1, 2, 3, 2, 3, 1, 1, 2, 3, 2, 3]
	mons = []

	for mon in range(party_size):
		address = section_address(1) + team_size_offset + 4 + mon * 100
		personality = int.from_bytes(sav[address:address+4], byteorder='little')
		if personality == 0: continue
		name_address = address + 0x08
		otid = int.from_bytes(sav[address+4:address+8], byteorder='little')
		key = personality ^ otid
		e_data = bytearray(sav[address+0x20:address+0x20+48])
		data = bytearray()
		for i in range(0,48,4):
			pt = key ^ int.from_bytes(e_data[i:i+4], byteorder='little')
			data += pt.to_bytes(4, 'little')
		g = data_g[personality % 24] * 12
		sid = int.from_bytes(data[g:g+2], byteorder='little')
		item = int.from_bytes(data[g+2:g+4], byteorder='little')
		mons.append([mon+1,sid,item,nid_name[sid_index[sid]],name_address])

	return mons

def mirage_island():
	poke_address = section_address(1) + team_size_offset + 4
	island_address = section_address(2) + mirage_island_offset

	sav[island_address + 0] = sav[poke_address + 0]
	sav[island_address + 1] = sav[poke_address + 1]

	return

def latios_hack():
	address = section_address(0)
	seen_a = int.from_bytes(sav[address+pokedex_seen_offset_a:address+pokedex_seen_offset_a+49], byteorder='little')
	seen_a ^= (1 << (380 - 1))
	seen_a ^= (1 << (381 - 1))
	for i, j in enumerate(seen_a.to_bytes(49, 'little')): sav[address+pokedex_seen_offset_a+i] = j

	address = section_address(1)
	seen_b = int.from_bytes(sav[address+pokedex_seen_offset_b:address+pokedex_seen_offset_b+49], byteorder='little')
	seen_b ^= (1 << (380 - 1))
	seen_b ^= (1 << (381 - 1))
	for i, j in enumerate(seen_b.to_bytes(49, 'little')): sav[address+pokedex_seen_offset_b+i] = j

	address = section_address(4)
	seen_c = int.from_bytes(sav[address+pokedex_seen_offset_c:address+pokedex_seen_offset_c+49], byteorder='little')
	seen_c ^= (1 << (380 - 1))
	seen_c ^= (1 << (381 - 1))
	for i, j in enumerate(seen_c.to_bytes(49, 'little')): sav[address+pokedex_seen_offset_c+i] = j

	return

def pokeblocks():
	address = section_address(1)
	maxlen = len(max(pokeblock_colors.values(), key=len))

	while True:
		format_string = 'Idx {1:' + str(maxlen) + 's} {2:>6s} {3:>6s} {4:>6s} {5:>6s} {6:>6s} {7:>6s} {8:>6s}'
		print(format_string.format(0,'Color','Spicy','Dry','Sweet','Bitter','Sour','Feel','Level'))
		print()
		for i in range(40):
			b = address + pokeblocks_offset + i*8
			#if sav[b] == 0: break
			format_string = '{0:2d}. {1:' + str(maxlen) + 's} {2:6d} {3:6d} {4:6d} {5:6d} {6:6d} {7:6d} {8:6d}'
			print(format_string.format(i+1,pokeblock_colors[sav[b]],sav[b+1],sav[b+2],sav[b+3],sav[b+4],sav[b+5],sav[b+6],max(sav[b+1],sav[b+2],sav[b+3],sav[b+4],sav[b+5])))

		print()

		while True:
			try:
				e = int(input("Edit block (1-40) ['0' to Exit]: "))
				if e > 40 or e < 0:
					print("\nOut of range. Try again...\n")
					continue
				if e == 0:
					print()
					return
				break
			except ValueError:
				print("\nNot a number. Try again...\n")
			except Exception as err:
				print(f"Unexpected {err=}, {type(err)=}")
				raise

		print()
		print('Input block as comma delimited values:\n')
		print('color[0-14], spicy[0-255], dry[0-255], sweet[0-255], bitter[0-255], sour[0-255], feel[0-255]')
		print()
		print('Colors:\n')
		for i in range(15):
			print('{0}={1} '.format(i,pokeblock_colors[i]),end='')
			if i % 5 == 4: print()
		print()
		print('Set color or entire input to 0 to delete block\n')
		print('[Return] to abort\n')

		b = address + pokeblocks_offset + (int(e)-1)*8

		while True:
			try:
				f = input("Block " + str(e) + ": ")
				if len(f) == 0: break
				if f == '0':
					color = 0
					break
				try:
					color, spicy, dry, sweet, bitter, sour, feel = [abs(int(i)) for i in f.replace(' ','').split(",")]
				except ValueError:
					print('\nFormat must be color,spicy,dry,sweet,bitter,sour,feel and all fields integers.\n')
					continue
				if color > 14:
					print('\ncolor must be 0-14\n')
					continue
				if spicy > 255 or dry > 255 or sweet > 255 or bitter > 255 or sour > 255 or feel > 255:
					print('\nspicy, dry, sweet, bitter, sour, feel must be 0-255\n')
					continue
				break
			except Exception as err:
				print(f"Unexpected {err=}, {type(err)=}")
				raise

		print()

		if color == 0: spicy = dry = sweet = bitter = sour = feel = 0

		sav[b+0] = color
		sav[b+1] = spicy
		sav[b+2] = dry
		sav[b+3] = sweet
		sav[b+4] = bitter
		sav[b+5] = sour
		sav[b+6] = feel
		#sav[b+7] = 0x3

		# compress
		i = 0
		while i < 39:
			b = address + pokeblocks_offset + i*8
			if sav[b] == 0:
				ss = 0
				for j in range(i+1,40):
					c = address + pokeblocks_offset + j*8
					ss += sav[c]
					if ss > 0: break
				if ss == 0: break
				sav[b:b+(39-i)*8] = sav[b+8:b+(39-i)*8+8]
				sav[b+8*(39-i):b+8*(39-i)+8] = bytearray([0,0,0,0,0,0,0,0])
				continue
			i += 1

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

605b89b67018abcea91e693a4dd25be3  Pokemon - Emerald Version (USA, Europe).gba
698a239d05afc59a818483ee01bab4b7  Pokemon - Emerald 386 (USA, Europe).gba
c9a195879eae869dff1a87ebe3735342  Pokemon - Emerald Final 7.41 (USA, Europe).gba
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
#		(
#			'Sort TMs & HMs',
#			sort_items,
#			['TM_HM']
#		),
		(
			'Berries',
			items,
			['BERRIES']
		),
#		(
#			'Sort Berries',
#			sort_items,
#			['BERRIES']
#		),
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
#			[['ITEMS','POKE_BALLS','TM_HM','BERRIES','KEY_ITEMS','PC_ITEMS']]
			[['ITEMS','POKE_BALLS','KEY_ITEMS','PC_ITEMS']]
		),
		(
			'Pokéblocks',
			pokeblocks,
			[]
		),
		(
			'Coins: ' + str(read_number(section_address(1) + coins_offset,2,get_security_key() & 0xFFFF)),
			edit_number,
			['Coins',section_address(1) + coins_offset,2,get_security_key() & 0xFFFF,9999]
		),
		(
			'Money: ' + str(read_number(section_address(1) + money_offset,4,get_security_key())),
			edit_number,
			['Money',section_address(1) + money_offset,4,get_security_key()]
		),
		(
			'Soot Sack Steps: ' + str(read_number(section_address(2) + soot_sack_steps_offset,2,0x0)),
			edit_number,
			['Soot Sack Steps',section_address(2) + soot_sack_steps_offset,2,0x0]
		),
		(
			'Dewford Town Rand: ' + str(read_number(section_address(3) + dewford_rand_offset,2,0x0)),
			edit_number,
			['Dewford Town Rand',section_address(3) + dewford_rand_offset,2,0x0]
		),
		(
			'Mirage Island Hack: ' + str(read_number(section_address(2) + mirage_island_offset,2,0x0)),
			mirage_island,
			[]
		),
		(
			'Edit ID: ' + str(read_number(section_address(0) + 0xA,2,0x0)),
			edit_number,
			['ID',section_address(0) + 0xA,2,0x0]
		),
		(
			'Edit Secret ID: ' + str(read_number(section_address(0) + 0xA + 2,2,0x0)),
			edit_number,
			['Secret ID',section_address(0) + 0xA + 2,2,0x0]
		),
		(
			'Edit Player Name: ' + poketoascii(sav,section_address(0),7),
			text_edit,
			[section_address(0),7,'Player Name']
		),
		(
			'Edit Player Gender (0 = boy, 1 = girl): ' + str(read_number(section_address(0) + 0x8,1,0x0)),
			edit_number,
			['Player Gender (0 = boy, 1 = girl)',section_address(0) + 0x8,1,0x0,1]
		),
		(
			'Edit Party Names',
			edit_party_names,
			[]
		),
		(
			'Edit Play Time: {0:d}:{1:02d}:{2:02d}:{3:02d}'.format(
				read_number(section_address(0) + 0x0E,2,0x0),
				sav[section_address(0) + 0x10],
				sav[section_address(0) + 0x11],
				sav[section_address(0) + 0x12]
			),
			playtime,
			[]
		),
		(
			'Toggle Flags',
			toggle_flags,
			[True,-1]
		),
		(
			'Toggle Used Flags (filter out _UNUSED)',
			toggle_flags,
			[False,-1]
		),
		(
			'Toggle Checked Flag (filter out _UNUSED & unchecked)',
			toggle_flags,
			[False,1]
		),
		(
			'Toggle Unchecked Flags (filter out _UNUSED & checked)',
			toggle_flags,
			[False,0]
		),
		(
			'Pokédex [Full] (read-only)',
			pokedex,
			[False, False]
		),
		(
			'Pokédex Seen (read-only)',
			pokedex,
			[True, False]
		),
		(
			'Pokédex Obtainable (read-only)',
			pokedex,
			[False, True]
		),
		(
			'Pokédex Latias/Latios Seen Hack',
			latios_hack,
			[]
		),
		(
			"Lanette's PC [by box] (read-only)",
			lanette_pc_box,
			[]
		),
		(
			"Lanette's PC [by name] (read-only)",
			lanette_pc_name,
			[]
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


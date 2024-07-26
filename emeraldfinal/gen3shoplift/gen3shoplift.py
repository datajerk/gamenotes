#!/usr/bin/env python3

import sys
import os
import re
import binascii


### globals

outputfilename = 'newbag.sav'
version = "0.2.0"

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


### big dicts

items_index = {0: 'NONE', 1: 'MASTER_BALL', 2: 'ULTRA_BALL', 3: 'GREAT_BALL', 4: 'POKE_BALL', 5: 'SAFARI_BALL', 6: 'NET_BALL', 7: 'DIVE_BALL', 8: 'NEST_BALL', 9: 'REPEAT_BALL', 10: 'TIMER_BALL', 11: 'LUXURY_BALL', 12: 'PREMIER_BALL', 13: 'POTION', 14: 'ANTIDOTE', 15: 'BURN_HEAL', 16: 'ICE_HEAL', 17: 'AWAKENING', 18: 'PARALYZE_HEAL', 19: 'FULL_RESTORE', 20: 'MAX_POTION', 21: 'HYPER_POTION', 22: 'SUPER_POTION', 23: 'FULL_HEAL', 24: 'REVIVE', 25: 'MAX_REVIVE', 26: 'FRESH_WATER', 27: 'SODA_POP', 28: 'LEMONADE', 29: 'MOOMOO_MILK', 30: 'ENERGY_POWDER', 31: 'ENERGY_ROOT', 32: 'HEAL_POWDER', 33: 'REVIVAL_HERB', 34: 'ETHER', 35: 'MAX_ETHER', 36: 'ELIXIR', 37: 'MAX_ELIXIR', 38: 'LAVA_COOKIE', 39: 'BLUE_FLUTE', 40: 'YELLOW_FLUTE', 41: 'RED_FLUTE', 42: 'BLACK_FLUTE', 43: 'WHITE_FLUTE', 44: 'BERRY_JUICE', 45: 'SACRED_ASH', 46: 'SHOAL_SALT', 47: 'SHOAL_SHELL', 48: 'RED_SHARD', 49: 'BLUE_SHARD', 50: 'YELLOW_SHARD', 51: 'GREEN_SHARD', 52: '034', 53: '035', 54: '036', 55: '037', 56: '038', 57: '039', 58: '03A', 59: '03B', 60: '03C', 61: '03D', 62: '03E', 63: 'HP_UP', 64: 'PROTEIN', 65: 'IRON', 66: 'CARBOS', 67: 'CALCIUM', 68: 'RARE_CANDY', 69: 'PP_UP', 70: 'ZINC', 71: 'PP_MAX', 72: '048', 73: 'GUARD_SPEC', 74: 'DIRE_HIT', 75: 'X_ATTACK', 76: 'X_DEFEND', 77: 'X_SPEED', 78: 'X_ACCURACY', 79: 'X_SPECIAL', 80: 'POKE_DOLL', 81: 'FLUFFY_TAIL', 82: '052', 83: 'SUPER_REPEL', 84: 'MAX_REPEL', 85: 'ESCAPE_ROPE', 86: 'REPEL', 87: '057', 88: '058', 89: '059', 90: '05A', 91: '05B', 92: '05C', 93: 'SUN_STONE', 94: 'MOON_STONE', 95: 'FIRE_STONE', 96: 'THUNDER_STONE', 97: 'WATER_STONE', 98: 'LEAF_STONE', 99: '063', 100: '064', 101: '065', 102: '066', 103: 'TINY_MUSHROOM', 104: 'BIG_MUSHROOM', 105: '069', 106: 'PEARL', 107: 'BIG_PEARL', 108: 'STARDUST', 109: 'STAR_PIECE', 110: 'NUGGET', 111: 'HEART_SCALE', 112: '070', 113: '071', 114: '072', 115: '073', 116: '074', 117: '075', 118: '076', 119: '077', 120: '078', 121: 'ORANGE_MAIL', 122: 'HARBOR_MAIL', 123: 'GLITTER_MAIL', 124: 'MECH_MAIL', 125: 'WOOD_MAIL', 126: 'WAVE_MAIL', 127: 'BEAD_MAIL', 128: 'SHADOW_MAIL', 129: 'TROPIC_MAIL', 130: 'DREAM_MAIL', 131: 'FAB_MAIL', 132: 'RETRO_MAIL', 133: 'CHERI_BERRY', 134: 'CHESTO_BERRY', 135: 'PECHA_BERRY', 136: 'RAWST_BERRY', 137: 'ASPEAR_BERRY', 138: 'LEPPA_BERRY', 139: 'ORAN_BERRY', 140: 'PERSIM_BERRY', 141: 'LUM_BERRY', 142: 'SITRUS_BERRY', 143: 'FIGY_BERRY', 144: 'WIKI_BERRY', 145: 'MAGO_BERRY', 146: 'AGUAV_BERRY', 147: 'IAPAPA_BERRY', 148: 'RAZZ_BERRY', 149: 'BLUK_BERRY', 150: 'NANAB_BERRY', 151: 'WEPEAR_BERRY', 152: 'PINAP_BERRY', 153: 'POMEG_BERRY', 154: 'KELPSY_BERRY', 155: 'QUALOT_BERRY', 156: 'HONDEW_BERRY', 157: 'GREPA_BERRY', 158: 'TAMATO_BERRY', 159: 'CORNN_BERRY', 160: 'MAGOST_BERRY', 161: 'RABUTA_BERRY', 162: 'NOMEL_BERRY', 163: 'SPELON_BERRY', 164: 'PAMTRE_BERRY', 165: 'WATMEL_BERRY', 166: 'DURIN_BERRY', 167: 'BELUE_BERRY', 168: 'LIECHI_BERRY', 169: 'GANLON_BERRY', 170: 'SALAC_BERRY', 171: 'PETAYA_BERRY', 172: 'APICOT_BERRY', 173: 'LANSAT_BERRY', 174: 'STARF_BERRY', 175: 'ENIGMA_BERRY', 176: 'UNUSED_BERRY_1', 177: 'UNUSED_BERRY_2', 178: 'UNUSED_BERRY_3', 179: 'BRIGHT_POWDER', 180: 'WHITE_HERB', 181: 'MACHO_BRACE', 182: 'EXP_SHARE', 183: 'QUICK_CLAW', 184: 'SOOTHE_BELL', 185: 'MENTAL_HERB', 186: 'CHOICE_BAND', 187: 'KINGS_ROCK', 188: 'SILVER_POWDER', 189: 'AMULET_COIN', 190: 'CLEANSE_TAG', 191: 'SOUL_DEW', 192: 'DEEP_SEA_TOOTH', 193: 'DEEP_SEA_SCALE', 194: 'SMOKE_BALL', 195: 'EVERSTONE', 196: 'FOCUS_BAND', 197: 'LUCKY_EGG', 198: 'SCOPE_LENS', 199: 'METAL_COAT', 200: 'LEFTOVERS', 201: 'DRAGON_SCALE', 202: 'LIGHT_BALL', 203: 'SOFT_SAND', 204: 'HARD_STONE', 205: 'MIRACLE_SEED', 206: 'BLACK_GLASSES', 207: 'BLACK_BELT', 208: 'MAGNET', 209: 'MYSTIC_WATER', 210: 'SHARP_BEAK', 211: 'POISON_BARB', 212: 'NEVER_MELT_ICE', 213: 'SPELL_TAG', 214: 'TWISTED_SPOON', 215: 'CHARCOAL', 216: 'DRAGON_FANG', 217: 'SILK_SCARF', 218: 'UP_GRADE', 219: 'SHELL_BELL', 220: 'SEA_INCENSE', 221: 'LAX_INCENSE', 222: 'LUCKY_PUNCH', 223: 'METAL_POWDER', 224: 'THICK_CLUB', 225: 'STICK', 226: '0E2', 227: '0E3', 228: '0E4', 229: '0E5', 230: '0E6', 231: '0E7', 232: '0E8', 233: '0E9', 234: '0EA', 235: '0EB', 236: '0EC', 237: '0ED', 238: '0EE', 239: '0EF', 240: '0F0', 241: '0F1', 242: '0F2', 243: '0F3', 244: '0F4', 245: '0F5', 246: '0F6', 247: '0F7', 248: '0F8', 249: '0F9', 250: '0FA', 251: '0FB', 252: '0FC', 253: '0FD', 254: 'RED_SCARF', 255: 'BLUE_SCARF', 256: 'PINK_SCARF', 257: 'GREEN_SCARF', 258: 'YELLOW_SCARF', 259: 'MACH_BIKE', 260: 'COIN_CASE', 261: 'ITEMFINDER', 262: 'OLD_ROD', 263: 'GOOD_ROD', 264: 'SUPER_ROD', 265: 'SS_TICKET', 266: 'CONTEST_PASS', 267: '10B', 268: 'WAILMER_PAIL', 269: 'DEVON_GOODS', 270: 'SOOT_SACK', 271: 'BASEMENT_KEY', 272: 'ACRO_BIKE', 273: 'POKEBLOCK_CASE', 274: 'LETTER', 275: 'EON_TICKET', 276: 'RED_ORB', 277: 'BLUE_ORB', 278: 'SCANNER', 279: 'GO_GOGGLES', 280: 'METEORITE', 281: 'ROOM_1_KEY', 282: 'ROOM_2_KEY', 283: 'ROOM_4_KEY', 284: 'ROOM_6_KEY', 285: 'STORAGE_KEY', 286: 'ROOT_FOSSIL', 287: 'CLAW_FOSSIL', 288: 'DEVON_SCOPE', 289: 'TM01', 290: 'TM02', 291: 'TM03', 292: 'TM04', 293: 'TM05', 294: 'TM06', 295: 'TM07', 296: 'TM08', 297: 'TM09', 298: 'TM10', 299: 'TM11', 300: 'TM12', 301: 'TM13', 302: 'TM14', 303: 'TM15', 304: 'TM16', 305: 'TM17', 306: 'TM18', 307: 'TM19', 308: 'TM20', 309: 'TM21', 310: 'TM22', 311: 'TM23', 312: 'TM24', 313: 'TM25', 314: 'TM26', 315: 'TM27', 316: 'TM28', 317: 'TM29', 318: 'TM30', 319: 'TM31', 320: 'TM32', 321: 'TM33', 322: 'TM34', 323: 'TM35', 324: 'TM36', 325: 'TM37', 326: 'TM38', 327: 'TM39', 328: 'TM40', 329: 'TM41', 330: 'TM42', 331: 'TM43', 332: 'TM44', 333: 'TM45', 334: 'TM46', 335: 'TM47', 336: 'TM48', 337: 'TM49', 338: 'TM50', 339: 'HM01', 340: 'HM02', 341: 'HM03', 342: 'HM04', 343: 'HM05', 344: 'HM06', 345: 'HM07', 346: 'HM08', 347: '15B', 348: '15C', 349: 'OAKS_PARCEL', 350: 'POKE_FLUTE', 351: 'SECRET_KEY', 352: 'BIKE_VOUCHER', 353: 'GOLD_TEETH', 354: 'OLD_AMBER', 355: 'CARD_KEY', 356: 'LIFT_KEY', 357: 'HELIX_FOSSIL', 358: 'DOME_FOSSIL', 359: 'SILPH_SCOPE', 360: 'BICYCLE', 361: 'TOWN_MAP', 362: 'VS_SEEKER', 363: 'FAME_CHECKER', 364: 'TM_CASE', 365: 'BERRY_POUCH', 366: 'TEACHY_TV', 367: 'TRI_PASS', 368: 'RAINBOW_PASS', 369: 'TEA', 370: 'MYSTIC_TICKET', 371: 'AURORA_TICKET', 372: 'POWDER_JAR', 373: 'RUBY', 374: 'SAPPHIRE', 375: 'MAGMA_EMBLEM', 376: 'OLD_SEA_MAP'}
items_id = {'NONE': 0, 'MASTER_BALL': 1, 'ULTRA_BALL': 2, 'GREAT_BALL': 3, 'POKE_BALL': 4, 'SAFARI_BALL': 5, 'NET_BALL': 6, 'DIVE_BALL': 7, 'NEST_BALL': 8, 'REPEAT_BALL': 9, 'TIMER_BALL': 10, 'LUXURY_BALL': 11, 'PREMIER_BALL': 12, 'POTION': 13, 'ANTIDOTE': 14, 'BURN_HEAL': 15, 'ICE_HEAL': 16, 'AWAKENING': 17, 'PARALYZE_HEAL': 18, 'FULL_RESTORE': 19, 'MAX_POTION': 20, 'HYPER_POTION': 21, 'SUPER_POTION': 22, 'FULL_HEAL': 23, 'REVIVE': 24, 'MAX_REVIVE': 25, 'FRESH_WATER': 26, 'SODA_POP': 27, 'LEMONADE': 28, 'MOOMOO_MILK': 29, 'ENERGY_POWDER': 30, 'ENERGY_ROOT': 31, 'HEAL_POWDER': 32, 'REVIVAL_HERB': 33, 'ETHER': 34, 'MAX_ETHER': 35, 'ELIXIR': 36, 'MAX_ELIXIR': 37, 'LAVA_COOKIE': 38, 'BLUE_FLUTE': 39, 'YELLOW_FLUTE': 40, 'RED_FLUTE': 41, 'BLACK_FLUTE': 42, 'WHITE_FLUTE': 43, 'BERRY_JUICE': 44, 'SACRED_ASH': 45, 'SHOAL_SALT': 46, 'SHOAL_SHELL': 47, 'RED_SHARD': 48, 'BLUE_SHARD': 49, 'YELLOW_SHARD': 50, 'GREEN_SHARD': 51, '034': 52, '035': 53, '036': 54, '037': 55, '038': 56, '039': 57, '03A': 58, '03B': 59, '03C': 60, '03D': 61, '03E': 62, 'HP_UP': 63, 'PROTEIN': 64, 'IRON': 65, 'CARBOS': 66, 'CALCIUM': 67, 'RARE_CANDY': 68, 'PP_UP': 69, 'ZINC': 70, 'PP_MAX': 71, '048': 72, 'GUARD_SPEC': 73, 'DIRE_HIT': 74, 'X_ATTACK': 75, 'X_DEFEND': 76, 'X_SPEED': 77, 'X_ACCURACY': 78, 'X_SPECIAL': 79, 'POKE_DOLL': 80, 'FLUFFY_TAIL': 81, '052': 82, 'SUPER_REPEL': 83, 'MAX_REPEL': 84, 'ESCAPE_ROPE': 85, 'REPEL': 86, '057': 87, '058': 88, '059': 89, '05A': 90, '05B': 91, '05C': 92, 'SUN_STONE': 93, 'MOON_STONE': 94, 'FIRE_STONE': 95, 'THUNDER_STONE': 96, 'WATER_STONE': 97, 'LEAF_STONE': 98, '063': 99, '064': 100, '065': 101, '066': 102, 'TINY_MUSHROOM': 103, 'BIG_MUSHROOM': 104, '069': 105, 'PEARL': 106, 'BIG_PEARL': 107, 'STARDUST': 108, 'STAR_PIECE': 109, 'NUGGET': 110, 'HEART_SCALE': 111, '070': 112, '071': 113, '072': 114, '073': 115, '074': 116, '075': 117, '076': 118, '077': 119, '078': 120, 'ORANGE_MAIL': 121, 'HARBOR_MAIL': 122, 'GLITTER_MAIL': 123, 'MECH_MAIL': 124, 'WOOD_MAIL': 125, 'WAVE_MAIL': 126, 'BEAD_MAIL': 127, 'SHADOW_MAIL': 128, 'TROPIC_MAIL': 129, 'DREAM_MAIL': 130, 'FAB_MAIL': 131, 'RETRO_MAIL': 132, 'CHERI_BERRY': 133, 'CHESTO_BERRY': 134, 'PECHA_BERRY': 135, 'RAWST_BERRY': 136, 'ASPEAR_BERRY': 137, 'LEPPA_BERRY': 138, 'ORAN_BERRY': 139, 'PERSIM_BERRY': 140, 'LUM_BERRY': 141, 'SITRUS_BERRY': 142, 'FIGY_BERRY': 143, 'WIKI_BERRY': 144, 'MAGO_BERRY': 145, 'AGUAV_BERRY': 146, 'IAPAPA_BERRY': 147, 'RAZZ_BERRY': 148, 'BLUK_BERRY': 149, 'NANAB_BERRY': 150, 'WEPEAR_BERRY': 151, 'PINAP_BERRY': 152, 'POMEG_BERRY': 153, 'KELPSY_BERRY': 154, 'QUALOT_BERRY': 155, 'HONDEW_BERRY': 156, 'GREPA_BERRY': 157, 'TAMATO_BERRY': 158, 'CORNN_BERRY': 159, 'MAGOST_BERRY': 160, 'RABUTA_BERRY': 161, 'NOMEL_BERRY': 162, 'SPELON_BERRY': 163, 'PAMTRE_BERRY': 164, 'WATMEL_BERRY': 165, 'DURIN_BERRY': 166, 'BELUE_BERRY': 167, 'LIECHI_BERRY': 168, 'GANLON_BERRY': 169, 'SALAC_BERRY': 170, 'PETAYA_BERRY': 171, 'APICOT_BERRY': 172, 'LANSAT_BERRY': 173, 'STARF_BERRY': 174, 'ENIGMA_BERRY': 175, 'UNUSED_BERRY_1': 176, 'UNUSED_BERRY_2': 177, 'UNUSED_BERRY_3': 178, 'BRIGHT_POWDER': 179, 'WHITE_HERB': 180, 'MACHO_BRACE': 181, 'EXP_SHARE': 182, 'QUICK_CLAW': 183, 'SOOTHE_BELL': 184, 'MENTAL_HERB': 185, 'CHOICE_BAND': 186, 'KINGS_ROCK': 187, 'SILVER_POWDER': 188, 'AMULET_COIN': 189, 'CLEANSE_TAG': 190, 'SOUL_DEW': 191, 'DEEP_SEA_TOOTH': 192, 'DEEP_SEA_SCALE': 193, 'SMOKE_BALL': 194, 'EVERSTONE': 195, 'FOCUS_BAND': 196, 'LUCKY_EGG': 197, 'SCOPE_LENS': 198, 'METAL_COAT': 199, 'LEFTOVERS': 200, 'DRAGON_SCALE': 201, 'LIGHT_BALL': 202, 'SOFT_SAND': 203, 'HARD_STONE': 204, 'MIRACLE_SEED': 205, 'BLACK_GLASSES': 206, 'BLACK_BELT': 207, 'MAGNET': 208, 'MYSTIC_WATER': 209, 'SHARP_BEAK': 210, 'POISON_BARB': 211, 'NEVER_MELT_ICE': 212, 'SPELL_TAG': 213, 'TWISTED_SPOON': 214, 'CHARCOAL': 215, 'DRAGON_FANG': 216, 'SILK_SCARF': 217, 'UP_GRADE': 218, 'SHELL_BELL': 219, 'SEA_INCENSE': 220, 'LAX_INCENSE': 221, 'LUCKY_PUNCH': 222, 'METAL_POWDER': 223, 'THICK_CLUB': 224, 'STICK': 225, '0E2': 226, '0E3': 227, '0E4': 228, '0E5': 229, '0E6': 230, '0E7': 231, '0E8': 232, '0E9': 233, '0EA': 234, '0EB': 235, '0EC': 236, '0ED': 237, '0EE': 238, '0EF': 239, '0F0': 240, '0F1': 241, '0F2': 242, '0F3': 243, '0F4': 244, '0F5': 245, '0F6': 246, '0F7': 247, '0F8': 248, '0F9': 249, '0FA': 250, '0FB': 251, '0FC': 252, '0FD': 253, 'RED_SCARF': 254, 'BLUE_SCARF': 255, 'PINK_SCARF': 256, 'GREEN_SCARF': 257, 'YELLOW_SCARF': 258, 'MACH_BIKE': 259, 'COIN_CASE': 260, 'ITEMFINDER': 261, 'OLD_ROD': 262, 'GOOD_ROD': 263, 'SUPER_ROD': 264, 'SS_TICKET': 265, 'CONTEST_PASS': 266, '10B': 267, 'WAILMER_PAIL': 268, 'DEVON_GOODS': 269, 'SOOT_SACK': 270, 'BASEMENT_KEY': 271, 'ACRO_BIKE': 272, 'POKEBLOCK_CASE': 273, 'LETTER': 274, 'EON_TICKET': 275, 'RED_ORB': 276, 'BLUE_ORB': 277, 'SCANNER': 278, 'GO_GOGGLES': 279, 'METEORITE': 280, 'ROOM_1_KEY': 281, 'ROOM_2_KEY': 282, 'ROOM_4_KEY': 283, 'ROOM_6_KEY': 284, 'STORAGE_KEY': 285, 'ROOT_FOSSIL': 286, 'CLAW_FOSSIL': 287, 'DEVON_SCOPE': 288, 'TM01': 289, 'TM02': 290, 'TM03': 291, 'TM04': 292, 'TM05': 293, 'TM06': 294, 'TM07': 295, 'TM08': 296, 'TM09': 297, 'TM10': 298, 'TM11': 299, 'TM12': 300, 'TM13': 301, 'TM14': 302, 'TM15': 303, 'TM16': 304, 'TM17': 305, 'TM18': 306, 'TM19': 307, 'TM20': 308, 'TM21': 309, 'TM22': 310, 'TM23': 311, 'TM24': 312, 'TM25': 313, 'TM26': 314, 'TM27': 315, 'TM28': 316, 'TM29': 317, 'TM30': 318, 'TM31': 319, 'TM32': 320, 'TM33': 321, 'TM34': 322, 'TM35': 323, 'TM36': 324, 'TM37': 325, 'TM38': 326, 'TM39': 327, 'TM40': 328, 'TM41': 329, 'TM42': 330, 'TM43': 331, 'TM44': 332, 'TM45': 333, 'TM46': 334, 'TM47': 335, 'TM48': 336, 'TM49': 337, 'TM50': 338, 'HM01': 339, 'HM02': 340, 'HM03': 341, 'HM04': 342, 'HM05': 343, 'HM06': 344, 'HM07': 345, 'HM08': 346, '15B': 347, '15C': 348, 'OAKS_PARCEL': 349, 'POKE_FLUTE': 350, 'SECRET_KEY': 351, 'BIKE_VOUCHER': 352, 'GOLD_TEETH': 353, 'OLD_AMBER': 354, 'CARD_KEY': 355, 'LIFT_KEY': 356, 'HELIX_FOSSIL': 357, 'DOME_FOSSIL': 358, 'SILPH_SCOPE': 359, 'BICYCLE': 360, 'TOWN_MAP': 361, 'VS_SEEKER': 362, 'FAME_CHECKER': 363, 'TM_CASE': 364, 'BERRY_POUCH': 365, 'TEACHY_TV': 366, 'TRI_PASS': 367, 'RAINBOW_PASS': 368, 'TEA': 369, 'MYSTIC_TICKET': 370, 'AURORA_TICKET': 371, 'POWDER_JAR': 372, 'RUBY': 373, 'SAPPHIRE': 374, 'MAGMA_EMBLEM': 375, 'OLD_SEA_MAP': 376}
items_pocket = {0: 'ITEMS', 1: 'POKE_BALLS', 2: 'POKE_BALLS', 3: 'POKE_BALLS', 4: 'POKE_BALLS', 5: 'POKE_BALLS', 6: 'POKE_BALLS', 7: 'POKE_BALLS', 8: 'POKE_BALLS', 9: 'POKE_BALLS', 10: 'POKE_BALLS', 11: 'POKE_BALLS', 12: 'POKE_BALLS', 13: 'ITEMS', 14: 'ITEMS', 15: 'ITEMS', 16: 'ITEMS', 17: 'ITEMS', 18: 'ITEMS', 19: 'ITEMS', 20: 'ITEMS', 21: 'ITEMS', 22: 'ITEMS', 23: 'ITEMS', 24: 'ITEMS', 25: 'ITEMS', 26: 'ITEMS', 27: 'ITEMS', 28: 'ITEMS', 29: 'ITEMS', 30: 'ITEMS', 31: 'ITEMS', 32: 'ITEMS', 33: 'ITEMS', 34: 'ITEMS', 35: 'ITEMS', 36: 'ITEMS', 37: 'ITEMS', 38: 'ITEMS', 39: 'ITEMS', 40: 'ITEMS', 41: 'ITEMS', 42: 'ITEMS', 43: 'ITEMS', 44: 'ITEMS', 45: 'ITEMS', 46: 'ITEMS', 47: 'ITEMS', 48: 'ITEMS', 49: 'ITEMS', 50: 'ITEMS', 51: 'ITEMS', 63: 'ITEMS', 64: 'ITEMS', 65: 'ITEMS', 66: 'ITEMS', 67: 'ITEMS', 68: 'ITEMS', 69: 'ITEMS', 70: 'ITEMS', 71: 'ITEMS', 73: 'ITEMS', 74: 'ITEMS', 75: 'ITEMS', 76: 'ITEMS', 77: 'ITEMS', 78: 'ITEMS', 79: 'ITEMS', 80: 'ITEMS', 81: 'ITEMS', 83: 'ITEMS', 84: 'ITEMS', 85: 'ITEMS', 86: 'ITEMS', 93: 'ITEMS', 94: 'ITEMS', 95: 'ITEMS', 96: 'ITEMS', 97: 'ITEMS', 98: 'ITEMS', 103: 'ITEMS', 104: 'ITEMS', 106: 'ITEMS', 107: 'ITEMS', 108: 'ITEMS', 109: 'ITEMS', 110: 'ITEMS', 111: 'ITEMS', 121: 'ITEMS', 122: 'ITEMS', 123: 'ITEMS', 124: 'ITEMS', 125: 'ITEMS', 126: 'ITEMS', 127: 'ITEMS', 128: 'ITEMS', 129: 'ITEMS', 130: 'ITEMS', 131: 'ITEMS', 132: 'ITEMS', 133: 'BERRIES', 134: 'BERRIES', 135: 'BERRIES', 136: 'BERRIES', 137: 'BERRIES', 138: 'BERRIES', 139: 'BERRIES', 140: 'BERRIES', 141: 'BERRIES', 142: 'BERRIES', 143: 'BERRIES', 144: 'BERRIES', 145: 'BERRIES', 146: 'BERRIES', 147: 'BERRIES', 148: 'BERRIES', 149: 'BERRIES', 150: 'BERRIES', 151: 'BERRIES', 152: 'BERRIES', 153: 'BERRIES', 154: 'BERRIES', 155: 'BERRIES', 156: 'BERRIES', 157: 'BERRIES', 158: 'BERRIES', 159: 'BERRIES', 160: 'BERRIES', 161: 'BERRIES', 162: 'BERRIES', 163: 'BERRIES', 164: 'BERRIES', 165: 'BERRIES', 166: 'BERRIES', 167: 'BERRIES', 168: 'BERRIES', 169: 'BERRIES', 170: 'BERRIES', 171: 'BERRIES', 172: 'BERRIES', 173: 'BERRIES', 174: 'BERRIES', 175: 'BERRIES', 179: 'ITEMS', 180: 'ITEMS', 181: 'ITEMS', 182: 'ITEMS', 183: 'ITEMS', 184: 'ITEMS', 185: 'ITEMS', 186: 'ITEMS', 187: 'ITEMS', 188: 'ITEMS', 189: 'ITEMS', 190: 'ITEMS', 191: 'ITEMS', 192: 'ITEMS', 193: 'ITEMS', 194: 'ITEMS', 195: 'ITEMS', 196: 'ITEMS', 197: 'ITEMS', 198: 'ITEMS', 199: 'ITEMS', 200: 'ITEMS', 201: 'ITEMS', 202: 'ITEMS', 203: 'ITEMS', 204: 'ITEMS', 205: 'ITEMS', 206: 'ITEMS', 207: 'ITEMS', 208: 'ITEMS', 209: 'ITEMS', 210: 'ITEMS', 211: 'ITEMS', 212: 'ITEMS', 213: 'ITEMS', 214: 'ITEMS', 215: 'ITEMS', 216: 'ITEMS', 217: 'ITEMS', 218: 'ITEMS', 219: 'ITEMS', 220: 'ITEMS', 221: 'ITEMS', 222: 'ITEMS', 223: 'ITEMS', 224: 'ITEMS', 225: 'ITEMS', 254: 'ITEMS', 255: 'ITEMS', 256: 'ITEMS', 257: 'ITEMS', 258: 'ITEMS', 259: 'KEY_ITEMS', 260: 'KEY_ITEMS', 261: 'KEY_ITEMS', 262: 'KEY_ITEMS', 263: 'KEY_ITEMS', 264: 'KEY_ITEMS', 265: 'KEY_ITEMS', 266: 'KEY_ITEMS', 268: 'KEY_ITEMS', 269: 'KEY_ITEMS', 270: 'KEY_ITEMS', 271: 'KEY_ITEMS', 272: 'KEY_ITEMS', 273: 'KEY_ITEMS', 274: 'KEY_ITEMS', 275: 'KEY_ITEMS', 276: 'KEY_ITEMS', 277: 'KEY_ITEMS', 278: 'KEY_ITEMS', 279: 'KEY_ITEMS', 280: 'KEY_ITEMS', 281: 'KEY_ITEMS', 282: 'KEY_ITEMS', 283: 'KEY_ITEMS', 284: 'KEY_ITEMS', 285: 'KEY_ITEMS', 286: 'KEY_ITEMS', 287: 'KEY_ITEMS', 288: 'KEY_ITEMS', 289: 'TM_HM', 290: 'TM_HM', 291: 'TM_HM', 292: 'TM_HM', 293: 'TM_HM', 294: 'TM_HM', 295: 'TM_HM', 296: 'TM_HM', 297: 'TM_HM', 298: 'TM_HM', 299: 'TM_HM', 300: 'TM_HM', 301: 'TM_HM', 302: 'TM_HM', 303: 'TM_HM', 304: 'TM_HM', 305: 'TM_HM', 306: 'TM_HM', 307: 'TM_HM', 308: 'TM_HM', 309: 'TM_HM', 310: 'TM_HM', 311: 'TM_HM', 312: 'TM_HM', 313: 'TM_HM', 314: 'TM_HM', 315: 'TM_HM', 316: 'TM_HM', 317: 'TM_HM', 318: 'TM_HM', 319: 'TM_HM', 320: 'TM_HM', 321: 'TM_HM', 322: 'TM_HM', 323: 'TM_HM', 324: 'TM_HM', 325: 'TM_HM', 326: 'TM_HM', 327: 'TM_HM', 328: 'TM_HM', 329: 'TM_HM', 330: 'TM_HM', 331: 'TM_HM', 332: 'TM_HM', 333: 'TM_HM', 334: 'TM_HM', 335: 'TM_HM', 336: 'TM_HM', 337: 'TM_HM', 338: 'TM_HM', 339: 'TM_HM', 340: 'TM_HM', 341: 'TM_HM', 342: 'TM_HM', 343: 'TM_HM', 344: 'TM_HM', 345: 'TM_HM', 346: 'TM_HM', 349: 'KEY_ITEMS', 350: 'KEY_ITEMS', 351: 'KEY_ITEMS', 352: 'KEY_ITEMS', 353: 'KEY_ITEMS', 354: 'KEY_ITEMS', 355: 'KEY_ITEMS', 356: 'KEY_ITEMS', 357: 'KEY_ITEMS', 358: 'KEY_ITEMS', 359: 'KEY_ITEMS', 360: 'KEY_ITEMS', 361: 'KEY_ITEMS', 362: 'KEY_ITEMS', 363: 'KEY_ITEMS', 364: 'KEY_ITEMS', 365: 'KEY_ITEMS', 366: 'KEY_ITEMS', 367: 'KEY_ITEMS', 368: 'KEY_ITEMS', 369: 'KEY_ITEMS', 370: 'KEY_ITEMS', 371: 'KEY_ITEMS', 372: 'KEY_ITEMS', 373: 'KEY_ITEMS', 374: 'KEY_ITEMS', 375: 'KEY_ITEMS', 376: 'KEY_ITEMS'}
items_name = {0: '????????', 1: 'MASTER BALL', 2: 'ULTRA BALL', 3: 'GREAT BALL', 4: 'POKé BALL', 5: 'SAFARI BALL', 6: 'NET BALL', 7: 'DIVE BALL', 8: 'NEST BALL', 9: 'REPEAT BALL', 10: 'TIMER BALL', 11: 'LUXURY BALL', 12: 'PREMIER BALL', 13: 'POTION', 14: 'ANTIDOTE', 15: 'BURN HEAL', 16: 'ICE HEAL', 17: 'AWAKENING', 18: 'PARLYZ HEAL', 19: 'FULL RESTORE', 20: 'MAX POTION', 21: 'HYPER POTION', 22: 'SUPER POTION', 23: 'FULL HEAL', 24: 'REVIVE', 25: 'MAX REVIVE', 26: 'FRESH WATER', 27: 'SODA POP', 28: 'LEMONADE', 29: 'MOOMOO MILK', 30: 'ENERGYPOWDER', 31: 'ENERGY ROOT', 32: 'HEAL POWDER', 33: 'REVIVAL HERB', 34: 'ETHER', 35: 'MAX ETHER', 36: 'ELIXIR', 37: 'MAX ELIXIR', 38: 'LAVA COOKIE', 39: 'BLUE FLUTE', 40: 'YELLOW FLUTE', 41: 'RED FLUTE', 42: 'BLACK FLUTE', 43: 'WHITE FLUTE', 44: 'BERRY JUICE', 45: 'SACRED ASH', 46: 'SHOAL SALT', 47: 'SHOAL SHELL', 48: 'RED SHARD', 49: 'BLUE SHARD', 50: 'YELLOW SHARD', 51: 'GREEN SHARD', 63: 'HP UP', 64: 'PROTEIN', 65: 'IRON', 66: 'CARBOS', 67: 'CALCIUM', 68: 'RARE CANDY', 69: 'PP UP', 70: 'ZINC', 71: 'PP MAX', 73: 'GUARD SPEC.', 74: 'DIRE HIT', 75: 'X ATTACK', 76: 'X DEFEND', 77: 'X SPEED', 78: 'X ACCURACY', 79: 'X SPECIAL', 80: 'POKé DOLL', 81: 'FLUFFY TAIL', 83: 'SUPER REPEL', 84: 'MAX REPEL', 85: 'ESCAPE ROPE', 86: 'REPEL', 93: 'SUN STONE', 94: 'MOON STONE', 95: 'FIRE STONE', 96: 'THUNDERSTONE', 97: 'WATER STONE', 98: 'LEAF STONE', 103: 'TINYMUSHROOM', 104: 'BIG MUSHROOM', 106: 'PEARL', 107: 'BIG PEARL', 108: 'STARDUST', 109: 'STAR PIECE', 110: 'NUGGET', 111: 'HEART SCALE', 121: 'ORANGE MAIL', 122: 'HARBOR MAIL', 123: 'GLITTER MAIL', 124: 'MECH MAIL', 125: 'WOOD MAIL', 126: 'WAVE MAIL', 127: 'BEAD MAIL', 128: 'SHADOW MAIL', 129: 'TROPIC MAIL', 130: 'DREAM MAIL', 131: 'FAB MAIL', 132: 'RETRO MAIL', 133: 'CHERI BERRY', 134: 'CHESTO BERRY', 135: 'PECHA BERRY', 136: 'RAWST BERRY', 137: 'ASPEAR BERRY', 138: 'LEPPA BERRY', 139: 'ORAN BERRY', 140: 'PERSIM BERRY', 141: 'LUM BERRY', 142: 'SITRUS BERRY', 143: 'FIGY BERRY', 144: 'WIKI BERRY', 145: 'MAGO BERRY', 146: 'AGUAV BERRY', 147: 'IAPAPA BERRY', 148: 'RAZZ BERRY', 149: 'BLUK BERRY', 150: 'NANAB BERRY', 151: 'WEPEAR BERRY', 152: 'PINAP BERRY', 153: 'POMEG BERRY', 154: 'KELPSY BERRY', 155: 'QUALOT BERRY', 156: 'HONDEW BERRY', 157: 'GREPA BERRY', 158: 'TAMATO BERRY', 159: 'CORNN BERRY', 160: 'MAGOST BERRY', 161: 'RABUTA BERRY', 162: 'NOMEL BERRY', 163: 'SPELON BERRY', 164: 'PAMTRE BERRY', 165: 'WATMEL BERRY', 166: 'DURIN BERRY', 167: 'BELUE BERRY', 168: 'LIECHI BERRY', 169: 'GANLON BERRY', 170: 'SALAC BERRY', 171: 'PETAYA BERRY', 172: 'APICOT BERRY', 173: 'LANSAT BERRY', 174: 'STARF BERRY', 175: 'ENIGMA BERRY', 179: 'BRIGHTPOWDER', 180: 'WHITE HERB', 181: 'MACHO BRACE', 182: 'EXP. SHARE', 183: 'QUICK CLAW', 184: 'SOOTHE BELL', 185: 'MENTAL HERB', 186: 'CHOICE BAND', 187: "KING'S ROCK", 188: 'SILVERPOWDER', 189: 'AMULET COIN', 190: 'CLEANSE TAG', 191: 'SOUL DEW', 192: 'DEEPSEATOOTH', 193: 'DEEPSEASCALE', 194: 'SMOKE BALL', 195: 'EVERSTONE', 196: 'FOCUS BAND', 197: 'LUCKY EGG', 198: 'SCOPE LENS', 199: 'METAL COAT', 200: 'LEFTOVERS', 201: 'DRAGON SCALE', 202: 'LIGHT BALL', 203: 'SOFT SAND', 204: 'HARD STONE', 205: 'MIRACLE SEED', 206: 'BLACKGLASSES', 207: 'BLACK BELT', 208: 'MAGNET', 209: 'MYSTIC WATER', 210: 'SHARP BEAK', 211: 'POISON BARB', 212: 'NEVERMELTICE', 213: 'SPELL TAG', 214: 'TWISTEDSPOON', 215: 'CHARCOAL', 216: 'DRAGON FANG', 217: 'SILK SCARF', 218: 'UP-GRADE', 219: 'SHELL BELL', 220: 'SEA INCENSE', 221: 'LAX INCENSE', 222: 'LUCKY PUNCH', 223: 'METAL POWDER', 224: 'THICK CLUB', 225: 'STICK', 254: 'RED SCARF', 255: 'BLUE SCARF', 256: 'PINK SCARF', 257: 'GREEN SCARF', 258: 'YELLOW SCARF', 259: 'MACH BIKE', 260: 'COIN CASE', 261: 'ITEMFINDER', 262: 'OLD ROD', 263: 'GOOD ROD', 264: 'SUPER ROD', 265: 'S.S. TICKET', 266: 'CONTEST PASS', 268: 'WAILMER PAIL', 269: 'DEVON GOODS', 270: 'SOOT SACK', 271: 'BASEMENT KEY', 272: 'ACRO BIKE', 273: '{POKEBLOCK} CASE', 274: 'LETTER', 275: 'EON TICKET', 276: 'RED ORB', 277: 'BLUE ORB', 278: 'SCANNER', 279: 'GO-GOGGLES', 280: 'METEORITE', 281: 'RM. 1 KEY', 282: 'RM. 2 KEY', 283: 'RM. 4 KEY', 284: 'RM. 6 KEY', 285: 'STORAGE KEY', 286: 'ROOT FOSSIL', 287: 'CLAW FOSSIL', 288: 'DEVON SCOPE', 289: 'TM01', 290: 'TM02', 291: 'TM03', 292: 'TM04', 293: 'TM05', 294: 'TM06', 295: 'TM07', 296: 'TM08', 297: 'TM09', 298: 'TM10', 299: 'TM11', 300: 'TM12', 301: 'TM13', 302: 'TM14', 303: 'TM15', 304: 'TM16', 305: 'TM17', 306: 'TM18', 307: 'TM19', 308: 'TM20', 309: 'TM21', 310: 'TM22', 311: 'TM23', 312: 'TM24', 313: 'TM25', 314: 'TM26', 315: 'TM27', 316: 'TM28', 317: 'TM29', 318: 'TM30', 319: 'TM31', 320: 'TM32', 321: 'TM33', 322: 'TM34', 323: 'TM35', 324: 'TM36', 325: 'TM37', 326: 'TM38', 327: 'TM39', 328: 'TM40', 329: 'TM41', 330: 'TM42', 331: 'TM43', 332: 'TM44', 333: 'TM45', 334: 'TM46', 335: 'TM47', 336: 'TM48', 337: 'TM49', 338: 'TM50', 339: 'HM01', 340: 'HM02', 341: 'HM03', 342: 'HM04', 343: 'HM05', 344: 'HM06', 345: 'HM07', 346: 'HM08', 349: "OAK'S PARCEL", 350: 'POKé FLUTE', 351: 'SECRET KEY', 352: 'BIKE VOUCHER', 353: 'GOLD TEETH', 354: 'OLD AMBER', 355: 'CARD KEY', 356: 'LIFT KEY', 357: 'HELIX FOSSIL', 358: 'DOME FOSSIL', 359: 'SILPH SCOPE', 360: 'BICYCLE', 361: 'TOWN MAP', 362: 'VS SEEKER', 363: 'FAME CHECKER', 364: 'TM CASE', 365: 'BERRY POUCH', 366: 'TEACHY TV', 367: 'TRI-PASS', 368: 'RAINBOW PASS', 369: 'TEA', 370: 'MYSTICTICKET', 371: 'AURORATICKET', 372: 'POWDER JAR', 373: 'RUBY', 374: 'SAPPHIRE', 375: 'MAGMA EMBLEM', 376: 'OLD SEA MAP'}


### functions

def init_dicts_arrays():
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
		for item in items_name:
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

print("\nPokémon Gen III (Emerald only for now) Offline Store v" + version)
print("\n(Tested ROM (Pokemon - Emerald Final 7.41 (USA, Europe).gba) md5sum c9a195879eae869dff1a87ebe3735342)")
print("\nUSE AT YOUR OWN PERIL!!!\n")
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
			'Poké Balls',
			items,
			['POKE_BALLS']
		),
		(
			'THs & HMs',
			items,
			['TM_HM']
		),
		(
			'Berries',
			items,
			['BERRIES']
		),
		(
			'Key Items',
			items,
			['KEY_ITEMS']
		),
		(
			'PC Items',
			items,
			['PC_ITEMS']
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


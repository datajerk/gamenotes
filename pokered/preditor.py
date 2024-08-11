#!/usr/bin/env python3

import sys
import os
import re
import binascii
import collections

# globals
outputfilename = 'newpack.sav'
version = "0.12.2"
item_names = {}
eng_letter = {}
longest_item = 0
pokeball = '◓'

MAX_ITEMS = 20
MAX_BOX_ITEMS = 50

items = {
	1: 'Master Ball',
	2: 'Ultra Ball',
	3: 'Great Ball',
	4: 'Poké Ball',
	5: 'Town Map',
	6: 'Bicycle',
	7: '?????',
	8: 'Safari Ball',
	9: 'Pokédex',
	10: 'Moon Stone',
	11: 'Antidote',
	12: 'Burn Heal',
	13: 'Ice Heal',
	14: 'Awakening',
	15: 'Parlyz Heal',
	16: 'Full Restore',
	17: 'Max Potion',
	18: 'Hyper Potion',
	19: 'Super Potion',
	20: 'Potion',
	21: 'BoulderBadge',
	22: 'CascadeBadge',
	23: 'ThunderBadge',
	24: 'RainbowBadge',
	25: 'SoulBadge',
	26: 'MarshBadge',
	27: 'VolcanoBadge',
	28: 'EarthBadge',
	29: 'Escape Rope',
	30: 'Repel',
	31: 'Old Amber',
	32: 'Fire Stone',
	33: 'Thunderstone',
	34: 'Water Stone',
	35: 'HP Up',
	36: 'Protein',
	37: 'Iron',
	38: 'Carbos',
	39: 'Calcium',
	40: 'Rare Candy',
	41: 'Dome Fossil',
	42: 'Helix Fossil',
	43: 'Secret Key',
	44: '?????',
	45: 'Bike Voucher',
	46: 'X Accuracy',
	47: 'Leaf Stone',
	48: 'Card Key',
	49: 'Nugget',
	50: 'PP Up*',
	51: 'Poké Doll',
	52: 'Full Heal',
	53: 'Revive',
	54: 'Max Revive',
	55: 'Guard Spec.',
	56: 'Super Repel',
	57: 'Max Repel',
	58: 'Dire Hit',
	59: 'Coin',
	60: 'Fresh Water',
	61: 'Soda Pop',
	62: 'Lemonade',
	63: 'S.S. Ticket',
	64: 'Gold Teeth',
	65: 'X Attack',
	66: 'X Defend',
	67: 'X Speed',
	68: 'X Special',
	69: 'Coin Case',
	70: 'Oak\'s Parcel',
	71: 'Itemfinder',
	72: 'Silph Scope',
	73: 'Poké Flute',
	74: 'Lift Key',
	75: 'Exp. All',
	76: 'Old Rod',
	77: 'Good Rod',
	78: 'Super Rod',
	79: 'PP Up',
	80: 'Ether',
	81: 'Max Ether',
	82: 'Elixer',
	83: 'Max Elixer',
	196: 'HM01 Cut',
	197: 'HM02 Fly',
	198: 'HM03 Surf',
	199: 'HM04 Strength',
	200: 'HM05 Flash',
	201: 'TM01 Mega Punch',
	202: 'TM02 Razor Wind',
	203: 'TM03 Swords Dance',
	204: 'TM04 Whirlwind',
	205: 'TM05 Mega Kick',
	206: 'TM06 Toxic',
	207: 'TM07 Horn Drill',
	208: 'TM08 Body Slam',
	209: 'TM09 Take Down',
	210: 'TM10 Double-Edge',
	211: 'TM11 BubbleBeam',
	212: 'TM12 Water Gun',
	213: 'TM13 Ice Beam',
	214: 'TM14 Blizzard',
	215: 'TM15 Hyper Beam',
	216: 'TM16 Pay Day',
	217: 'TM17 Submission',
	218: 'TM18 Counter',
	219: 'TM19 Seismic Toss',
	220: 'TM20 Rage',
	221: 'TM21 Mega Drain',
	222: 'TM22 SolarBeam',
	223: 'TM23 Dragon Rage',
	224: 'TM24 Thunderbolt',
	225: 'TM25 Thunder',
	226: 'TM26 Earthquake',
	227: 'TM27 Fissure',
	228: 'TM28 Dig',
	229: 'TM29 Psychic',
	230: 'TM30 Teleport',
	231: 'TM31 Mimic',
	232: 'TM32 Double Team',
	233: 'TM33 Reflect',
	234: 'TM34 Bide',
	235: 'TM35 Metronome',
	236: 'TM36 Selfdestruct',
	237: 'TM37 Egg Bomb',
	238: 'TM38 Fire Blast',
	239: 'TM39 Swift',
	240: 'TM40 Skull Bash',
	241: 'TM41 Softboiled',
	242: 'TM42 Dream Eater',
	243: 'TM43 Sky Attack',
	244: 'TM44 Rest',
	245: 'TM45 Thunder Wave',
	246: 'TM46 Psywave',
	247: 'TM47 Explosion',
	248: 'TM48 Rock Slide',
	249: 'TM49 Tri Attack',
	250: 'TM50 Substitute',
}

eng_index = {
	0x7F: ' ',
	0x80: 'A',
	0x81: 'B',
	0x82: 'C',
	0x83: 'D',
	0x84: 'E',
	0x85: 'F',
	0x86: 'G',
	0x87: 'H',
	0x88: 'I',
	0x89: 'J',
	0x8A: 'K',
	0x8B: 'L',
	0x8C: 'M',
	0x8D: 'N',
	0x8E: 'O',
	0x8F: 'P',
	0x90: 'Q',
	0x91: 'R',
	0x92: 'S',
	0x93: 'T',
	0x94: 'U',
	0x95: 'V',
	0x96: 'W',
	0x97: 'X',
	0x98: 'Y',
	0x99: 'Z',
	0x9A: '(',
	0x9B: ')',
	0x9C: ':',
	0x9D: ';',
	0x9E: '[',
	0x9F: ']',
	0xA0: 'a',
	0xA1: 'b',
	0xA2: 'c',
	0xA3: 'd',
	0xA4: 'e',
	0xA5: 'f',
	0xA6: 'g',
	0xA7: 'h',
	0xA8: 'i',
	0xA9: 'j',
	0xAA: 'k',
	0xAB: 'l',
	0xAC: 'm',
	0xAD: 'n',
	0xAE: 'o',
	0xAF: 'p',
	0xB0: 'q',
	0xB1: 'r',
	0xB2: 's',
	0xB3: 't',
	0xB4: 'u',
	0xB5: 'v',
	0xB6: 'w',
	0xB7: 'x',
	0xB8: 'y',
	0xB9: 'z',
	0xBA: 'é',
	0xE0: "'",
	0xE1: '%', # PK
	0xE2: '$', # MN
	0xE3: '-',
	0xE6: '?',
	0xE7: '!',
	0xEF: '^', # male symbol
	0xF1: '*', # x (times symbol)
	0xF2: '.',
	0xF3: '/',
	0xF4: ',',
	0xF5: '+', # female symbol
	0xF6: '0',
	0xF7: '1',
	0xF8: '2',
	0xF9: '3',
	0xFA: '4',
	0xFB: '5',
	0xFC: '6',
	0xFD: '7',
	0xFE: '8',
	0xFF: '9',
}

sid_index = {
	0:(-1,"'M (glitch)"),
	1:(112,"Rhydon"),
	2:(115,"Kangaskhan"),
	3:(32,"Nidoran♂"),
	4:(35,"Clefairy"),
	5:(21,"Spearow"),
	6:(100,"Voltorb"),
	7:(34,"Nidoking"),
	8:(80,"Slowbro"),
	9:(2,"Ivysaur"),
	10:(103,"Exeggutor"),
	11:(108,"Lickitung"),
	12:(102,"Exeggcute"),
	13:(88,"Grimer"),
	14:(94,"Gengar"),
	15:(29,"Nidoran♀"),
	16:(31,"Nidoqueen"),
	17:(104,"Cubone"),
	18:(111,"Rhyhorn"),
	19:(131,"Lapras"),
	20:(59,"Arcanine"),
	21:(151,"Mew"),
	22:(130,"Gyarados"),
	23:(90,"Shellder"),
	24:(72,"Tentacool"),
	25:(92,"Gastly"),
	26:(123,"Scyther"),
	27:(120,"Staryu"),
	28:(9,"Blastoise"),
	29:(127,"Pinsir"),
	30:(114,"Tangela"),
	31:(-1,"Missing No. (Gyaoon)"),
	32:(-1,"Missing No. (Nidoran♂-like Pokémon)"),
	33:(58,"Growlithe"),
	34:(95,"Onix"),
	35:(22,"Fearow"),
	36:(16,"Pidgey"),
	37:(79,"Slowpoke"),
	38:(64,"Kadabra"),
	39:(75,"Graveler"),
	40:(113,"Chansey"),
	41:(67,"Machoke"),
	42:(122,"Mr. Mime"),
	43:(106,"Hitmonlee"),
	44:(107,"Hitmonchan"),
	45:(24,"Arbok"),
	46:(47,"Parasect"),
	47:(54,"Psyduck"),
	48:(96,"Drowzee"),
	49:(76,"Golem"),
	50:(-1,"Missing No. (Balloonda)"),
	51:(126,"Magmar"),
	52:(-1,"Missing No. (Buu)"),
	53:(125,"Electabuzz"),
	54:(82,"Magneton"),
	55:(109,"Koffing"),
	56:(-1,"Missing No. (Deer)"),
	57:(56,"Mankey"),
	58:(86,"Seel"),
	59:(50,"Diglett"),
	60:(128,"Tauros"),
	61:(-1,"Missing No. (Elephant Pokémon)"),
	62:(-1,"Missing No. (Crocky)"),
	63:(-1,"Missing No. (Squid Pokémon 1)"),
	64:(83,"Farfetch'd"),
	65:(48,"Venonat"),
	66:(149,"Dragonite"),
	67:(-1,"Missing No. (Cactus)"),
	68:(-1,"Missing No. (Jaggu)"),
	69:(-1,"Missing No. (Zubat pre-evo)"),
	70:(84,"Doduo"),
	71:(60,"Poliwag"),
	72:(124,"Jynx"),
	73:(146,"Moltres"),
	74:(144,"Articuno"),
	75:(145,"Zapdos"),
	76:(132,"Ditto"),
	77:(52,"Meowth"),
	78:(98,"Krabby"),
	79:(-1,"Missing No. (Fish Pokémon 1)"),
	80:(-1,"Missing No. (Fish Pokémon 2)"),
	81:(-1,"Missing No. (Vulpix pre-evo)"),
	82:(37,"Vulpix"),
	83:(38,"Ninetales"),
	84:(25,"Pikachu"),
	85:(26,"Raichu"),
	86:(-1,"Missing No. (Frog-like Pokémon 1)"),
	87:(-1,"Missing No. (Frog-like Pokémon 2)"),
	88:(147,"Dratini"),
	89:(148,"Dragonair"),
	90:(140,"Kabuto"),
	91:(141,"Kabutops"),
	92:(116,"Horsea"),
	93:(117,"Seadra"),
	94:(-1,"Missing No. (Lizard Pokémon 2)"),
	95:(-1,"Missing No. (Lizard Pokémon 3)"),
	96:(27,"Sandshrew"),
	97:(28,"Sandslash"),
	98:(138,"Omanyte"),
	99:(139,"Omastar"),
	100:(39,"Jigglypuff"),
	101:(40,"Wigglytuff"),
	102:(133,"Eevee"),
	103:(136,"Flareon"),
	104:(135,"Jolteon"),
	105:(134,"Vaporeon"),
	106:(66,"Machop"),
	107:(41,"Zubat"),
	108:(23,"Ekans"),
	109:(46,"Paras"),
	110:(61,"Poliwhirl"),
	111:(62,"Poliwrath"),
	112:(13,"Weedle"),
	113:(14,"Kakuna"),
	114:(15,"Beedrill"),
	115:(-1,"Missing No. [Unknown]"),
	116:(85,"Dodrio"),
	117:(57,"Primeape"),
	118:(51,"Dugtrio"),
	119:(49,"Venomoth"),
	120:(87,"Dewgong"),
	121:(-1,"Missing No. [Unknown]"),
	122:(-1,"Missing No. (Squid Pokémon 2)"),
	123:(10,"Caterpie"),
	124:(11,"Metapod"),
	125:(12,"Butterfree"),
	126:(68,"Machamp"),
	127:(-1,"Missing No. (Golduck mid-evo)"),
	128:(55,"Golduck"),
	129:(97,"Hypno"),
	130:(42,"Golbat"),
	131:(150,"Mewtwo"),
	132:(143,"Snorlax"),
	133:(129,"Magikarp"),
	134:(-1,"Missing No. (Meowth pre-evo)"),
	135:(-1,"Missing No. [Unknown]"),
	136:(89,"Muk"),
	137:(-1,"Missing No. (Gyaoon pre-evo)"),
	138:(99,"Kingler"),
	139:(91,"Cloyster"),
	140:(-1,"Missing No. (Magneton-like Pokémon)"),
	141:(101,"Electrode"),
	142:(36,"Clefable"),
	143:(110,"Weezing"),
	144:(53,"Persian"),
	145:(105,"Marowak"),
	146:(-1,"Missing No. (Marowak evo)"),
	147:(93,"Haunter"),
	148:(63,"Abra"),
	149:(65,"Alakazam"),
	150:(17,"Pidgeotto"),
	151:(18,"Pidgeot"),
	152:(121,"Starmie"),
	153:(1,"Bulbasaur"),
	154:(3,"Venusaur"),
	155:(73,"Tentacruel"),
	156:(-1,"Missing No. (Goldeen pre-evo)"),
	157:(118,"Goldeen"),
	158:(119,"Seaking"),
	159:(-1,"Missing No. (Kotora)"),
	160:(-1,"Missing No. (Raitora)"),
	161:(-1,"Missing No. (Raitora evo)"),
	162:(-1,"Missing No. (Ponyta pre-evo)"),
	163:(77,"Ponyta"),
	164:(78,"Rapidash"),
	165:(19,"Rattata"),
	166:(20,"Raticate"),
	167:(33,"Nidorino"),
	168:(30,"Nidorina"),
	169:(74,"Geodude"),
	170:(137,"Porygon"),
	171:(142,"Aerodactyl"),
	172:(-1,"Missing No. (Blastoise-like Pokémon)"),
	173:(81,"Magnemite"),
	174:(-1,"Missing No. (Lizard Pokémon 1)"),
	175:(-1,"Missing No. (Gorochu)"),
	176:(4,"Charmander"),
	177:(7,"Squirtle"),
	178:(5,"Charmeleon"),
	179:(8,"Wartortle"),
	180:(6,"Charizard"),
	181:(-1,"Missing No. (Original Wartortle evo)"),
	182:(-1,"Missing No. (Kabutops Fossil)"),
	183:(-1,"Missing No. (Aerodactyl Fossil)"),
	184:(-1,"Missing No. (Pokémon Tower Ghost)"),
	185:(43,"Oddish"),
	186:(44,"Gloom"),
	187:(45,"Vileplume"),
	188:(69,"Bellsprout"),
	189:(70,"Weepinbell"),
	190:(71,"Victreebel"),
}

nid_index = {
	1:(153,"Bulbasaur"),
	2:(9,"Ivysaur"),
	3:(154,"Venusaur"),
	4:(176,"Charmander"),
	5:(178,"Charmeleon"),
	6:(180,"Charizard"),
	7:(177,"Squirtle"),
	8:(179,"Wartortle"),
	9:(28,"Blastoise"),
	10:(123,"Caterpie"),
	11:(124,"Metapod"),
	12:(125,"Butterfree"),
	13:(112,"Weedle"),
	14:(113,"Kakuna"),
	15:(114,"Beedrill"),
	16:(36,"Pidgey"),
	17:(150,"Pidgeotto"),
	18:(151,"Pidgeot"),
	19:(165,"Rattata"),
	20:(166,"Raticate"),
	21:(5,"Spearow"),
	22:(35,"Fearow"),
	23:(108,"Ekans"),
	24:(45,"Arbok"),
	25:(84,"Pikachu"),
	26:(85,"Raichu"),
	27:(96,"Sandshrew"),
	28:(97,"Sandslash"),
	29:(15,"Nidoran♀"),
	30:(168,"Nidorina"),
	31:(16,"Nidoqueen"),
	32:(3,"Nidoran♂"),
	33:(167,"Nidorino"),
	34:(7,"Nidoking"),
	35:(4,"Clefairy"),
	36:(142,"Clefable"),
	37:(82,"Vulpix"),
	38:(83,"Ninetales"),
	39:(100,"Jigglypuff"),
	40:(101,"Wigglytuff"),
	41:(107,"Zubat"),
	42:(130,"Golbat"),
	43:(185,"Oddish"),
	44:(186,"Gloom"),
	45:(187,"Vileplume"),
	46:(109,"Paras"),
	47:(46,"Parasect"),
	48:(65,"Venonat"),
	49:(119,"Venomoth"),
	50:(59,"Diglett"),
	51:(118,"Dugtrio"),
	52:(77,"Meowth"),
	53:(144,"Persian"),
	54:(47,"Psyduck"),
	55:(128,"Golduck"),
	56:(57,"Mankey"),
	57:(117,"Primeape"),
	58:(33,"Growlithe"),
	59:(20,"Arcanine"),
	60:(71,"Poliwag"),
	61:(110,"Poliwhirl"),
	62:(111,"Poliwrath"),
	63:(148,"Abra"),
	64:(38,"Kadabra"),
	65:(149,"Alakazam"),
	66:(106,"Machop"),
	67:(41,"Machoke"),
	68:(126,"Machamp"),
	69:(188,"Bellsprout"),
	70:(189,"Weepinbell"),
	71:(190,"Victreebel"),
	72:(24,"Tentacool"),
	73:(155,"Tentacruel"),
	74:(169,"Geodude"),
	75:(39,"Graveler"),
	76:(49,"Golem"),
	77:(163,"Ponyta"),
	78:(164,"Rapidash"),
	79:(37,"Slowpoke"),
	80:(8,"Slowbro"),
	81:(173,"Magnemite"),
	82:(54,"Magneton"),
	83:(64,"Farfetch'd"),
	84:(70,"Doduo"),
	85:(116,"Dodrio"),
	86:(58,"Seel"),
	87:(120,"Dewgong"),
	88:(13,"Grimer"),
	89:(136,"Muk"),
	90:(23,"Shellder"),
	91:(139,"Cloyster"),
	92:(25,"Gastly"),
	93:(147,"Haunter"),
	94:(14,"Gengar"),
	95:(34,"Onix"),
	96:(48,"Drowzee"),
	97:(129,"Hypno"),
	98:(78,"Krabby"),
	99:(138,"Kingler"),
	100:(6,"Voltorb"),
	101:(141,"Electrode"),
	102:(12,"Exeggcute"),
	103:(10,"Exeggutor"),
	104:(17,"Cubone"),
	105:(145,"Marowak"),
	106:(43,"Hitmonlee"),
	107:(44,"Hitmonchan"),
	108:(11,"Lickitung"),
	109:(55,"Koffing"),
	110:(143,"Weezing"),
	111:(18,"Rhyhorn"),
	112:(1,"Rhydon"),
	113:(40,"Chansey"),
	114:(30,"Tangela"),
	115:(2,"Kangaskhan"),
	116:(92,"Horsea"),
	117:(93,"Seadra"),
	118:(157,"Goldeen"),
	119:(158,"Seaking"),
	120:(27,"Staryu"),
	121:(152,"Starmie"),
	122:(42,"Mr. Mime"),
	123:(26,"Scyther"),
	124:(72,"Jynx"),
	125:(53,"Electabuzz"),
	126:(51,"Magmar"),
	127:(29,"Pinsir"),
	128:(60,"Tauros"),
	129:(133,"Magikarp"),
	130:(22,"Gyarados"),
	131:(19,"Lapras"),
	132:(76,"Ditto"),
	133:(102,"Eevee"),
	134:(105,"Vaporeon"),
	135:(104,"Jolteon"),
	136:(103,"Flareon"),
	137:(170,"Porygon"),
	138:(98,"Omanyte"),
	139:(99,"Omastar"),
	140:(90,"Kabuto"),
	141:(91,"Kabutops"),
	142:(171,"Aerodactyl"),
	143:(132,"Snorlax"),
	144:(74,"Articuno"),
	145:(75,"Zapdos"),
	146:(73,"Moltres"),
	147:(88,"Dratini"),
	148:(89,"Dragonair"),
	149:(66,"Dragonite"),
	150:(131,"Mewtwo"),
	151:(21,"Mew"),
}

events = {0: 'FOLLOWED_OAK_INTO_LAB', 3: 'HALL_OF_FAME_DEX_RATING', 6: 'PALLET_AFTER_GETTING_POKEBALLS', 24: 'GOT_TOWN_MAP', 25: 'ENTERED_BLUES_HOUSE', 26: 'DAISY_WALKING', 32: 'FOLLOWED_OAK_INTO_LAB_2', 33: 'OAK_ASKED_TO_CHOOSE_MON', 34: 'GOT_STARTER', 35: 'BATTLED_RIVAL_IN_OAKS_LAB', 36: 'GOT_POKEBALLS_FROM_OAK', 37: 'GOT_POKEDEX', 38: 'PALLET_AFTER_GETTING_POKEBALLS_2', 39: 'OAK_APPEARED_IN_PALLET', 40: 'VIRIDIAN_GYM_OPEN', 41: 'GOT_TM42', 56: 'OAK_GOT_PARCEL', 57: 'GOT_OAKS_PARCEL', 80: 'GOT_TM27', 81: 'BEAT_VIRIDIAN_GYM_GIOVANNI', 82: 'BEAT_VIRIDIAN_GYM_TRAINER_0', 83: 'BEAT_VIRIDIAN_GYM_TRAINER_1', 84: 'BEAT_VIRIDIAN_GYM_TRAINER_2', 85: 'BEAT_VIRIDIAN_GYM_TRAINER_3', 86: 'BEAT_VIRIDIAN_GYM_TRAINER_4', 87: 'BEAT_VIRIDIAN_GYM_TRAINER_5', 88: 'BEAT_VIRIDIAN_GYM_TRAINER_6', 89: 'BEAT_VIRIDIAN_GYM_TRAINER_7', 104: 'BOUGHT_MUSEUM_TICKET', 105: 'GOT_OLD_AMBER', 114: 'BEAT_PEWTER_GYM_TRAINER_0', 118: 'GOT_TM34', 119: 'BEAT_BROCK', 152: 'BEAT_CERULEAN_RIVAL', 167: 'BEAT_CERULEAN_ROCKET_THIEF', 186: 'BEAT_CERULEAN_GYM_TRAINER_0', 187: 'BEAT_CERULEAN_GYM_TRAINER_1', 190: 'GOT_TM11', 191: 'BEAT_MISTY', 192: 'GOT_BICYCLE', 238: 'POKEMON_TOWER_RIVAL_ON_LEFT', 239: 'BEAT_POKEMON_TOWER_RIVAL', 241: 'BEAT_POKEMONTOWER_3_TRAINER_0', 242: 'BEAT_POKEMONTOWER_3_TRAINER_1', 243: 'BEAT_POKEMONTOWER_3_TRAINER_2', 249: 'BEAT_POKEMONTOWER_4_TRAINER_0', 250: 'BEAT_POKEMONTOWER_4_TRAINER_1', 251: 'BEAT_POKEMONTOWER_4_TRAINER_2', 258: 'BEAT_POKEMONTOWER_5_TRAINER_0', 259: 'BEAT_POKEMONTOWER_5_TRAINER_1', 260: 'BEAT_POKEMONTOWER_5_TRAINER_2', 261: 'BEAT_POKEMONTOWER_5_TRAINER_3', 263: 'IN_PURIFIED_ZONE', 265: 'BEAT_POKEMONTOWER_6_TRAINER_0', 266: 'BEAT_POKEMONTOWER_6_TRAINER_1', 267: 'BEAT_POKEMONTOWER_6_TRAINER_2', 271: 'BEAT_GHOST_MAROWAK', 273: 'BEAT_POKEMONTOWER_7_TRAINER_0', 274: 'BEAT_POKEMONTOWER_7_TRAINER_1', 275: 'BEAT_POKEMONTOWER_7_TRAINER_2', 279: 'RESCUED_MR_FUJI_2', 296: 'GOT_POKE_FLUTE', 337: 'GOT_BIKE_VOUCHER', 342: 'SEEL_FAN_BOAST', 343: 'PIKACHU_FAN_BOAST', 352: '2ND_LOCK_OPENED', 353: '1ST_LOCK_OPENED', 354: 'BEAT_VERMILION_GYM_TRAINER_0', 355: 'BEAT_VERMILION_GYM_TRAINER_1', 356: 'BEAT_VERMILION_GYM_TRAINER_2', 358: 'GOT_TM24', 359: 'BEAT_LT_SURGE', 384: 'GOT_TM41', 396: 'GOT_TM13', 397: 'GOT_TM48', 398: 'GOT_TM49', 399: 'GOT_TM18', 424: 'GOT_TM21', 425: 'BEAT_ERIKA', 426: 'BEAT_CELADON_GYM_TRAINER_0', 427: 'BEAT_CELADON_GYM_TRAINER_1', 428: 'BEAT_CELADON_GYM_TRAINER_2', 429: 'BEAT_CELADON_GYM_TRAINER_3', 430: 'BEAT_CELADON_GYM_TRAINER_4', 431: 'BEAT_CELADON_GYM_TRAINER_5', 432: 'BEAT_CELADON_GYM_TRAINER_6', 440: '1B8 ; ???', 441: 'FOUND_ROCKET_HIDEOUT', 442: 'GOT_10_COINS', 443: 'GOT_20_COINS', 444: 'GOT_20_COINS_2', 447: '1BF ; ???', 480: 'GOT_COIN_CASE', 568: 'GOT_HM04', 569: 'GAVE_GOLD_TEETH', 590: 'SAFARI_GAME_OVER', 591: 'IN_SAFARI_ZONE', 600: 'GOT_TM06', 601: 'BEAT_KOGA', 602: 'BEAT_FUCHSIA_GYM_TRAINER_0', 603: 'BEAT_FUCHSIA_GYM_TRAINER_1', 604: 'BEAT_FUCHSIA_GYM_TRAINER_2', 605: 'BEAT_FUCHSIA_GYM_TRAINER_3', 606: 'BEAT_FUCHSIA_GYM_TRAINER_4', 607: 'BEAT_FUCHSIA_GYM_TRAINER_5', 632: 'MANSION_SWITCH_ON', 649: 'BEAT_MANSION_1_TRAINER_0', 664: 'GOT_TM38', 665: 'BEAT_BLAINE', 666: 'BEAT_CINNABAR_GYM_TRAINER_0', 667: 'BEAT_CINNABAR_GYM_TRAINER_1', 668: 'BEAT_CINNABAR_GYM_TRAINER_2', 669: 'BEAT_CINNABAR_GYM_TRAINER_3', 670: 'BEAT_CINNABAR_GYM_TRAINER_4', 671: 'BEAT_CINNABAR_GYM_TRAINER_5', 672: 'BEAT_CINNABAR_GYM_TRAINER_6', 679: '2A7 ; ???', 680: 'CINNABAR_GYM_GATE0_UNLOCKED', 681: 'CINNABAR_GYM_GATE1_UNLOCKED', 682: 'CINNABAR_GYM_GATE2_UNLOCKED', 683: 'CINNABAR_GYM_GATE3_UNLOCKED', 684: 'CINNABAR_GYM_GATE4_UNLOCKED', 685: 'CINNABAR_GYM_GATE5_UNLOCKED', 686: 'CINNABAR_GYM_GATE6_UNLOCKED', 727: 'GOT_TM35', 736: 'GAVE_FOSSIL_TO_LAB', 737: 'LAB_STILL_REVIVING_FOSSIL', 738: 'LAB_HANDING_OVER_FOSSIL_MON', 832: 'GOT_TM31', 848: 'DEFEATED_FIGHTING_DOJO', 849: 'BEAT_KARATE_MASTER', 850: 'BEAT_FIGHTING_DOJO_TRAINER_0', 851: 'BEAT_FIGHTING_DOJO_TRAINER_1', 852: 'BEAT_FIGHTING_DOJO_TRAINER_2', 853: 'BEAT_FIGHTING_DOJO_TRAINER_3', 854: 'GOT_HITMONLEE', 855: 'GOT_HITMONCHAN', 864: 'GOT_TM46', 865: 'BEAT_SABRINA', 866: 'BEAT_SAFFRON_GYM_TRAINER_0', 867: 'BEAT_SAFFRON_GYM_TRAINER_1', 868: 'BEAT_SAFFRON_GYM_TRAINER_2', 869: 'BEAT_SAFFRON_GYM_TRAINER_3', 870: 'BEAT_SAFFRON_GYM_TRAINER_4', 871: 'BEAT_SAFFRON_GYM_TRAINER_5', 872: 'BEAT_SAFFRON_GYM_TRAINER_6', 919: 'SILPH_CO_RECEPTIONIST_AT_DESK', 944: 'GOT_TM29', 960: 'GOT_POTION_SAMPLE', 984: 'GOT_HM05', 994: 'BEAT_ROUTE_3_TRAINER_0', 995: 'BEAT_ROUTE_3_TRAINER_1', 996: 'BEAT_ROUTE_3_TRAINER_2', 997: 'BEAT_ROUTE_3_TRAINER_3', 998: 'BEAT_ROUTE_3_TRAINER_4', 999: 'BEAT_ROUTE_3_TRAINER_5', 1000: 'BEAT_ROUTE_3_TRAINER_6', 1001: 'BEAT_ROUTE_3_TRAINER_7', 1010: 'BEAT_ROUTE_4_TRAINER_0', 1023: 'BOUGHT_MAGIKARP', 1041: 'BEAT_ROUTE_6_TRAINER_0', 1042: 'BEAT_ROUTE_6_TRAINER_1', 1043: 'BEAT_ROUTE_6_TRAINER_2', 1044: 'BEAT_ROUTE_6_TRAINER_3', 1045: 'BEAT_ROUTE_6_TRAINER_4', 1046: 'BEAT_ROUTE_6_TRAINER_5', 1073: 'BEAT_ROUTE_8_TRAINER_0', 1074: 'BEAT_ROUTE_8_TRAINER_1', 1075: 'BEAT_ROUTE_8_TRAINER_2', 1076: 'BEAT_ROUTE_8_TRAINER_3', 1077: 'BEAT_ROUTE_8_TRAINER_4', 1078: 'BEAT_ROUTE_8_TRAINER_5', 1079: 'BEAT_ROUTE_8_TRAINER_6', 1080: 'BEAT_ROUTE_8_TRAINER_7', 1081: 'BEAT_ROUTE_8_TRAINER_8', 1089: 'BEAT_ROUTE_9_TRAINER_0', 1090: 'BEAT_ROUTE_9_TRAINER_1', 1091: 'BEAT_ROUTE_9_TRAINER_2', 1092: 'BEAT_ROUTE_9_TRAINER_3', 1093: 'BEAT_ROUTE_9_TRAINER_4', 1094: 'BEAT_ROUTE_9_TRAINER_5', 1095: 'BEAT_ROUTE_9_TRAINER_6', 1096: 'BEAT_ROUTE_9_TRAINER_7', 1097: 'BEAT_ROUTE_9_TRAINER_8', 1105: 'BEAT_ROUTE_10_TRAINER_0', 1106: 'BEAT_ROUTE_10_TRAINER_1', 1107: 'BEAT_ROUTE_10_TRAINER_2', 1108: 'BEAT_ROUTE_10_TRAINER_3', 1109: 'BEAT_ROUTE_10_TRAINER_4', 1110: 'BEAT_ROUTE_10_TRAINER_5', 1113: 'BEAT_ROCK_TUNNEL_1_TRAINER_0', 1114: 'BEAT_ROCK_TUNNEL_1_TRAINER_1', 1115: 'BEAT_ROCK_TUNNEL_1_TRAINER_2', 1116: 'BEAT_ROCK_TUNNEL_1_TRAINER_3', 1117: 'BEAT_ROCK_TUNNEL_1_TRAINER_4', 1118: 'BEAT_ROCK_TUNNEL_1_TRAINER_5', 1119: 'BEAT_ROCK_TUNNEL_1_TRAINER_6', 1121: 'BEAT_POWER_PLANT_VOLTORB_0', 1122: 'BEAT_POWER_PLANT_VOLTORB_1', 1123: 'BEAT_POWER_PLANT_VOLTORB_2', 1124: 'BEAT_POWER_PLANT_VOLTORB_3', 1125: 'BEAT_POWER_PLANT_VOLTORB_4', 1126: 'BEAT_POWER_PLANT_VOLTORB_5', 1127: 'BEAT_POWER_PLANT_VOLTORB_6', 1128: 'BEAT_POWER_PLANT_VOLTORB_7', 1129: 'BEAT_ZAPDOS', 1137: 'BEAT_ROUTE_11_TRAINER_0', 1138: 'BEAT_ROUTE_11_TRAINER_1', 1139: 'BEAT_ROUTE_11_TRAINER_2', 1140: 'BEAT_ROUTE_11_TRAINER_3', 1141: 'BEAT_ROUTE_11_TRAINER_4', 1142: 'BEAT_ROUTE_11_TRAINER_5', 1143: 'BEAT_ROUTE_11_TRAINER_6', 1144: 'BEAT_ROUTE_11_TRAINER_7', 1145: 'BEAT_ROUTE_11_TRAINER_8', 1146: 'BEAT_ROUTE_11_TRAINER_9', 1151: 'GOT_ITEMFINDER', 1152: 'GOT_TM39', 1154: 'BEAT_ROUTE_12_TRAINER_0', 1155: 'BEAT_ROUTE_12_TRAINER_1', 1156: 'BEAT_ROUTE_12_TRAINER_2', 1157: 'BEAT_ROUTE_12_TRAINER_3', 1158: 'BEAT_ROUTE_12_TRAINER_4', 1159: 'BEAT_ROUTE_12_TRAINER_5', 1160: 'BEAT_ROUTE_12_TRAINER_6', 1166: 'FIGHT_ROUTE12_SNORLAX', 1167: 'BEAT_ROUTE12_SNORLAX', 1169: 'BEAT_ROUTE_13_TRAINER_0', 1170: 'BEAT_ROUTE_13_TRAINER_1', 1171: 'BEAT_ROUTE_13_TRAINER_2', 1172: 'BEAT_ROUTE_13_TRAINER_3', 1173: 'BEAT_ROUTE_13_TRAINER_4', 1174: 'BEAT_ROUTE_13_TRAINER_5', 1175: 'BEAT_ROUTE_13_TRAINER_6', 1176: 'BEAT_ROUTE_13_TRAINER_7', 1177: 'BEAT_ROUTE_13_TRAINER_8', 1178: 'BEAT_ROUTE_13_TRAINER_9', 1185: 'BEAT_ROUTE_14_TRAINER_0', 1186: 'BEAT_ROUTE_14_TRAINER_1', 1187: 'BEAT_ROUTE_14_TRAINER_2', 1188: 'BEAT_ROUTE_14_TRAINER_3', 1189: 'BEAT_ROUTE_14_TRAINER_4', 1190: 'BEAT_ROUTE_14_TRAINER_5', 1191: 'BEAT_ROUTE_14_TRAINER_6', 1192: 'BEAT_ROUTE_14_TRAINER_7', 1193: 'BEAT_ROUTE_14_TRAINER_8', 1194: 'BEAT_ROUTE_14_TRAINER_9', 1200: 'GOT_EXP_ALL', 1201: 'BEAT_ROUTE_15_TRAINER_0', 1202: 'BEAT_ROUTE_15_TRAINER_1', 1203: 'BEAT_ROUTE_15_TRAINER_2', 1204: 'BEAT_ROUTE_15_TRAINER_3', 1205: 'BEAT_ROUTE_15_TRAINER_4', 1206: 'BEAT_ROUTE_15_TRAINER_5', 1207: 'BEAT_ROUTE_15_TRAINER_6', 1208: 'BEAT_ROUTE_15_TRAINER_7', 1209: 'BEAT_ROUTE_15_TRAINER_8', 1210: 'BEAT_ROUTE_15_TRAINER_9', 1217: 'BEAT_ROUTE_16_TRAINER_0', 1218: 'BEAT_ROUTE_16_TRAINER_1', 1219: 'BEAT_ROUTE_16_TRAINER_2', 1220: 'BEAT_ROUTE_16_TRAINER_3', 1221: 'BEAT_ROUTE_16_TRAINER_4', 1222: 'BEAT_ROUTE_16_TRAINER_5', 1224: 'FIGHT_ROUTE16_SNORLAX', 1225: 'BEAT_ROUTE16_SNORLAX', 1230: 'GOT_HM02', 1231: 'RESCUED_MR_FUJI', 1233: 'BEAT_ROUTE_17_TRAINER_0', 1234: 'BEAT_ROUTE_17_TRAINER_1', 1235: 'BEAT_ROUTE_17_TRAINER_2', 1236: 'BEAT_ROUTE_17_TRAINER_3', 1237: 'BEAT_ROUTE_17_TRAINER_4', 1238: 'BEAT_ROUTE_17_TRAINER_5', 1239: 'BEAT_ROUTE_17_TRAINER_6', 1240: 'BEAT_ROUTE_17_TRAINER_7', 1241: 'BEAT_ROUTE_17_TRAINER_8', 1242: 'BEAT_ROUTE_17_TRAINER_9', 1249: 'BEAT_ROUTE_18_TRAINER_0', 1250: 'BEAT_ROUTE_18_TRAINER_1', 1251: 'BEAT_ROUTE_18_TRAINER_2', 1265: 'BEAT_ROUTE_19_TRAINER_0', 1266: 'BEAT_ROUTE_19_TRAINER_1', 1267: 'BEAT_ROUTE_19_TRAINER_2', 1268: 'BEAT_ROUTE_19_TRAINER_3', 1269: 'BEAT_ROUTE_19_TRAINER_4', 1270: 'BEAT_ROUTE_19_TRAINER_5', 1271: 'BEAT_ROUTE_19_TRAINER_6', 1272: 'BEAT_ROUTE_19_TRAINER_7', 1273: 'BEAT_ROUTE_19_TRAINER_8', 1274: 'BEAT_ROUTE_19_TRAINER_9', 1280: 'IN_SEAFOAM_ISLANDS', 1281: 'BEAT_ROUTE_20_TRAINER_0', 1282: 'BEAT_ROUTE_20_TRAINER_1', 1283: 'BEAT_ROUTE_20_TRAINER_2', 1284: 'BEAT_ROUTE_20_TRAINER_3', 1285: 'BEAT_ROUTE_20_TRAINER_4', 1286: 'BEAT_ROUTE_20_TRAINER_5', 1287: 'BEAT_ROUTE_20_TRAINER_6', 1288: 'BEAT_ROUTE_20_TRAINER_7', 1289: 'BEAT_ROUTE_20_TRAINER_8', 1290: 'BEAT_ROUTE_20_TRAINER_9', 1294: 'SEAFOAM1_BOULDER1_DOWN_HOLE', 1295: 'SEAFOAM1_BOULDER2_DOWN_HOLE', 1297: 'BEAT_ROUTE_21_TRAINER_0', 1298: 'BEAT_ROUTE_21_TRAINER_1', 1299: 'BEAT_ROUTE_21_TRAINER_2', 1300: 'BEAT_ROUTE_21_TRAINER_3', 1301: 'BEAT_ROUTE_21_TRAINER_4', 1302: 'BEAT_ROUTE_21_TRAINER_5', 1303: 'BEAT_ROUTE_21_TRAINER_6', 1304: 'BEAT_ROUTE_21_TRAINER_7', 1305: 'BEAT_ROUTE_21_TRAINER_8', 1312: '1ST_ROUTE22_RIVAL_BATTLE', 1313: '2ND_ROUTE22_RIVAL_BATTLE', 1317: 'BEAT_ROUTE22_RIVAL_1ST_BATTLE', 1318: 'BEAT_ROUTE22_RIVAL_2ND_BATTLE', 1319: 'ROUTE22_RIVAL_WANTS_BATTLE', 1328: 'PASSED_CASCADEBADGE_CHECK', 1329: 'PASSED_THUNDERBADGE_CHECK', 1330: 'PASSED_RAINBOWBADGE_CHECK', 1331: 'PASSED_SOULBADGE_CHECK', 1332: 'PASSED_MARSHBADGE_CHECK', 1333: 'PASSED_VOLCANOBADGE_CHECK', 1334: 'PASSED_EARTHBADGE_CHECK', 1336: 'VICTORY_ROAD_2_BOULDER_ON_SWITCH1', 1337: 'BEAT_VICTORY_ROAD_2_TRAINER_0', 1338: 'BEAT_VICTORY_ROAD_2_TRAINER_1', 1339: 'BEAT_VICTORY_ROAD_2_TRAINER_2', 1340: 'BEAT_VICTORY_ROAD_2_TRAINER_3', 1341: 'BEAT_VICTORY_ROAD_2_TRAINER_4', 1342: 'BEAT_MOLTRES', 1343: 'VICTORY_ROAD_2_BOULDER_ON_SWITCH2', 1344: 'GOT_NUGGET', 1345: 'BEAT_ROUTE24_ROCKET', 1346: 'BEAT_ROUTE_24_TRAINER_0', 1347: 'BEAT_ROUTE_24_TRAINER_1', 1348: 'BEAT_ROUTE_24_TRAINER_2', 1349: 'BEAT_ROUTE_24_TRAINER_3', 1350: 'BEAT_ROUTE_24_TRAINER_4', 1351: 'BEAT_ROUTE_24_TRAINER_5', 1353: 'NUGGET_REWARD_AVAILABLE', 1360: 'MET_BILL', 1361: 'BEAT_ROUTE_25_TRAINER_0', 1362: 'BEAT_ROUTE_25_TRAINER_1', 1363: 'BEAT_ROUTE_25_TRAINER_2', 1364: 'BEAT_ROUTE_25_TRAINER_3', 1365: 'BEAT_ROUTE_25_TRAINER_4', 1366: 'BEAT_ROUTE_25_TRAINER_5', 1367: 'BEAT_ROUTE_25_TRAINER_6', 1368: 'BEAT_ROUTE_25_TRAINER_7', 1369: 'BEAT_ROUTE_25_TRAINER_8', 1371: 'USED_CELL_SEPARATOR_ON_BILL', 1372: 'GOT_SS_TICKET', 1373: 'MET_BILL_2', 1374: 'BILL_SAID_USE_CELL_SEPARATOR', 1375: 'LEFT_BILLS_HOUSE_AFTER_HELPING', 1378: 'BEAT_VIRIDIAN_FOREST_TRAINER_0', 1379: 'BEAT_VIRIDIAN_FOREST_TRAINER_1', 1380: 'BEAT_VIRIDIAN_FOREST_TRAINER_2', 1393: 'BEAT_MT_MOON_1_TRAINER_0', 1394: 'BEAT_MT_MOON_1_TRAINER_1', 1395: 'BEAT_MT_MOON_1_TRAINER_2', 1396: 'BEAT_MT_MOON_1_TRAINER_3', 1397: 'BEAT_MT_MOON_1_TRAINER_4', 1398: 'BEAT_MT_MOON_1_TRAINER_5', 1399: 'BEAT_MT_MOON_1_TRAINER_6', 1401: 'BEAT_MT_MOON_EXIT_SUPER_NERD', 1402: 'BEAT_MT_MOON_3_TRAINER_0', 1403: 'BEAT_MT_MOON_3_TRAINER_1', 1404: 'BEAT_MT_MOON_3_TRAINER_2', 1405: 'BEAT_MT_MOON_3_TRAINER_3', 1406: 'GOT_DOME_FOSSIL', 1407: 'GOT_HELIX_FOSSIL', 1476: 'BEAT_SS_ANNE_5_TRAINER_0', 1477: 'BEAT_SS_ANNE_5_TRAINER_1', 1504: 'GOT_HM01', 1505: 'RUBBED_CAPTAINS_BACK', 1506: 'SS_ANNE_LEFT', 1507: 'WALKED_PAST_GUARD_AFTER_SS_ANNE_LEFT', 1508: 'STARTED_WALKING_OUT_OF_DOCK', 1509: 'WALKED_OUT_OF_DOCK', 1521: 'BEAT_SS_ANNE_8_TRAINER_0', 1522: 'BEAT_SS_ANNE_8_TRAINER_1', 1523: 'BEAT_SS_ANNE_8_TRAINER_2', 1524: 'BEAT_SS_ANNE_8_TRAINER_3', 1537: 'BEAT_SS_ANNE_9_TRAINER_0', 1538: 'BEAT_SS_ANNE_9_TRAINER_1', 1539: 'BEAT_SS_ANNE_9_TRAINER_2', 1540: 'BEAT_SS_ANNE_9_TRAINER_3', 1553: 'BEAT_SS_ANNE_10_TRAINER_0', 1554: 'BEAT_SS_ANNE_10_TRAINER_1', 1555: 'BEAT_SS_ANNE_10_TRAINER_2', 1556: 'BEAT_SS_ANNE_10_TRAINER_3', 1557: 'BEAT_SS_ANNE_10_TRAINER_4', 1558: 'BEAT_SS_ANNE_10_TRAINER_5', 1632: 'VICTORY_ROAD_3_BOULDER_ON_SWITCH1', 1633: 'BEAT_VICTORY_ROAD_3_TRAINER_0', 1634: 'BEAT_VICTORY_ROAD_3_TRAINER_1', 1635: 'BEAT_VICTORY_ROAD_3_TRAINER_2', 1636: 'BEAT_VICTORY_ROAD_3_TRAINER_3', 1638: 'VICTORY_ROAD_3_BOULDER_ON_SWITCH2', 1649: 'BEAT_ROCKET_HIDEOUT_1_TRAINER_0', 1650: 'BEAT_ROCKET_HIDEOUT_1_TRAINER_1', 1651: 'BEAT_ROCKET_HIDEOUT_1_TRAINER_2', 1652: 'BEAT_ROCKET_HIDEOUT_1_TRAINER_3', 1653: 'BEAT_ROCKET_HIDEOUT_1_TRAINER_4', 1655: '677 ; ???', 1663: '67F ; ???', 1665: 'BEAT_ROCKET_HIDEOUT_2_TRAINER_0', 1681: 'BEAT_ROCKET_HIDEOUT_3_TRAINER_0', 1682: 'BEAT_ROCKET_HIDEOUT_3_TRAINER_1', 1698: 'BEAT_ROCKET_HIDEOUT_4_TRAINER_0', 1699: 'BEAT_ROCKET_HIDEOUT_4_TRAINER_1', 1700: 'BEAT_ROCKET_HIDEOUT_4_TRAINER_2', 1701: 'ROCKET_HIDEOUT_4_DOOR_UNLOCKED', 1702: 'ROCKET_DROPPED_LIFT_KEY', 1703: 'BEAT_ROCKET_HIDEOUT_GIOVANNI', 1778: 'BEAT_SILPH_CO_2F_TRAINER_0', 1779: 'BEAT_SILPH_CO_2F_TRAINER_1', 1780: 'BEAT_SILPH_CO_2F_TRAINER_2', 1781: 'BEAT_SILPH_CO_2F_TRAINER_3', 1789: 'SILPH_CO_2_UNLOCKED_DOOR1', 1790: 'SILPH_CO_2_UNLOCKED_DOOR2', 1791: 'GOT_TM36', 1794: 'BEAT_SILPH_CO_3F_TRAINER_0', 1795: 'BEAT_SILPH_CO_3F_TRAINER_1', 1800: 'SILPH_CO_3_UNLOCKED_DOOR1', 1801: 'SILPH_CO_3_UNLOCKED_DOOR2', 1810: 'BEAT_SILPH_CO_4F_TRAINER_0', 1811: 'BEAT_SILPH_CO_4F_TRAINER_1', 1812: 'BEAT_SILPH_CO_4F_TRAINER_2', 1816: 'SILPH_CO_4_UNLOCKED_DOOR1', 1817: 'SILPH_CO_4_UNLOCKED_DOOR2', 1826: 'BEAT_SILPH_CO_5F_TRAINER_0', 1827: 'BEAT_SILPH_CO_5F_TRAINER_1', 1828: 'BEAT_SILPH_CO_5F_TRAINER_2', 1829: 'BEAT_SILPH_CO_5F_TRAINER_3', 1832: 'SILPH_CO_5_UNLOCKED_DOOR1', 1833: 'SILPH_CO_5_UNLOCKED_DOOR2', 1834: 'SILPH_CO_5_UNLOCKED_DOOR3', 1846: 'BEAT_SILPH_CO_6F_TRAINER_0', 1847: 'BEAT_SILPH_CO_6F_TRAINER_1', 1848: 'BEAT_SILPH_CO_6F_TRAINER_2', 1855: 'SILPH_CO_6_UNLOCKED_DOOR', 1856: 'BEAT_SILPH_CO_RIVAL', 1861: 'BEAT_SILPH_CO_7F_TRAINER_0', 1862: 'BEAT_SILPH_CO_7F_TRAINER_1', 1863: 'BEAT_SILPH_CO_7F_TRAINER_2', 1864: 'BEAT_SILPH_CO_7F_TRAINER_3', 1868: 'SILPH_CO_7_UNLOCKED_DOOR1', 1869: 'SILPH_CO_7_UNLOCKED_DOOR2', 1870: 'SILPH_CO_7_UNLOCKED_DOOR3', 1874: 'BEAT_SILPH_CO_8F_TRAINER_0', 1875: 'BEAT_SILPH_CO_8F_TRAINER_1', 1876: 'BEAT_SILPH_CO_8F_TRAINER_2', 1880: 'SILPH_CO_8_UNLOCKED_DOOR', 1890: 'BEAT_SILPH_CO_9F_TRAINER_0', 1891: 'BEAT_SILPH_CO_9F_TRAINER_1', 1892: 'BEAT_SILPH_CO_9F_TRAINER_2', 1896: 'SILPH_CO_9_UNLOCKED_DOOR1', 1897: 'SILPH_CO_9_UNLOCKED_DOOR2', 1898: 'SILPH_CO_9_UNLOCKED_DOOR3', 1899: 'SILPH_CO_9_UNLOCKED_DOOR4', 1905: 'BEAT_SILPH_CO_10F_TRAINER_0', 1906: 'BEAT_SILPH_CO_10F_TRAINER_1', 1912: 'SILPH_CO_10_UNLOCKED_DOOR', 1924: 'BEAT_SILPH_CO_11F_TRAINER_0', 1925: 'BEAT_SILPH_CO_11F_TRAINER_1', 1928: 'SILPH_CO_11_UNLOCKED_DOOR', 1933: 'GOT_MASTER_BALL', 1935: 'BEAT_SILPH_CO_GIOVANNI', 2049: 'BEAT_MANSION_2_TRAINER_0', 2065: 'BEAT_MANSION_3_TRAINER_0', 2066: 'BEAT_MANSION_3_TRAINER_1', 2081: 'BEAT_MANSION_4_TRAINER_0', 2082: 'BEAT_MANSION_4_TRAINER_1', 2176: 'GOT_HM03', 2241: 'BEAT_MEWTWO', 2273: 'BEAT_LORELEIS_ROOM_TRAINER_0', 2278: 'AUTOWALKED_INTO_LORELEIS_ROOM', 2281: 'BEAT_BRUNOS_ROOM_TRAINER_0', 2286: 'AUTOWALKED_INTO_BRUNOS_ROOM', 2289: 'BEAT_AGATHAS_ROOM_TRAINER_0', 2294: 'AUTOWALKED_INTO_AGATHAS_ROOM', 2297: 'BEAT_LANCES_ROOM_TRAINER_0', 2302: 'BEAT_LANCE', 2303: 'LANCES_ROOM_LOCK_DOOR', 2305: 'BEAT_CHAMPION_RIVAL', 2321: 'BEAT_VICTORY_ROAD_1_TRAINER_0', 2322: 'BEAT_VICTORY_ROAD_1_TRAINER_1', 2327: 'VICTORY_ROAD_1_BOULDER_ON_SWITCH', 2481: 'BEAT_ROCK_TUNNEL_2_TRAINER_0', 2482: 'BEAT_ROCK_TUNNEL_2_TRAINER_1', 2483: 'BEAT_ROCK_TUNNEL_2_TRAINER_2', 2484: 'BEAT_ROCK_TUNNEL_2_TRAINER_3', 2485: 'BEAT_ROCK_TUNNEL_2_TRAINER_4', 2486: 'BEAT_ROCK_TUNNEL_2_TRAINER_5', 2487: 'BEAT_ROCK_TUNNEL_2_TRAINER_6', 2488: 'BEAT_ROCK_TUNNEL_2_TRAINER_7', 2496: 'SEAFOAM2_BOULDER1_DOWN_HOLE', 2497: 'SEAFOAM2_BOULDER2_DOWN_HOLE', 2504: 'SEAFOAM3_BOULDER1_DOWN_HOLE', 2505: 'SEAFOAM3_BOULDER2_DOWN_HOLE', 2512: 'SEAFOAM4_BOULDER1_DOWN_HOLE', 2513: 'SEAFOAM4_BOULDER2_DOWN_HOLE', 2522: 'BEAT_ARTICUNO'}

# functions

def init_dicts_arrays():
	global longest_item

	for key in dict(items):
		if len(items[key]) > longest_item: longest_item = len(items[key])
		item_names[items[key]] = key

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

def array_menu(array, max_items, item_type_filter):
	sub_sel = -1
	while (sub_sel != 0):
		count = [0]
		item_count = {}
		for key in dict(items): item_count[key] = 0
		sub_menu = ['Return']

		for i in range(sav[array]):
			item_index = sav[array + i*2 + 1]
			item_count[item_index] = sav[array + i*2 + 2]

		for item_index in dict(items):
			format_string = '{:' + str(longest_item + 1) + '} {:2}'
			sub_menu.append(format_string.format(items[item_index] + ':', item_count[item_index]))
			count.append(item_count[item_index])

		sub_sel = menu(main_menu[sel] + ' Menu (Select ' + main_menu[sel] + ' to Edit, ' + str(sav[array]) + ' of ' + str(max_items) + ' array elements assigned)',sub_menu,1,max_items - sav[array],count)

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
		print()

		item = sub_menu[sub_sel].split(':')[0]
		target_index = item_names[item]

		for i in range(sav[array]):
			item_index = sav[array + i*2 + 1]
			if target_index == item_index: break

		# append
		if target_index != item_index:
			if q == 0: continue
			i += 1
			sav[array + i*2 + 1] = target_index
			sav[array + i*2 + 3] = 0xff
			sav[array] += 1

		# update
		if q > 0:
			sav[array + i*2 + 2] = q
			continue

		# delete
		for i in range(i, sav[array]):
			sav[array + i*2 + 1] = sav[array + i*2 + 3]
			sav[array + i*2 + 2] = sav[array + i*2 + 4]
		sav[array] -= 1

	return

def array_sort(array, max_items, item_type_filter):
	names = {}

	print('\nCurrent Order:\n')
	for i in range(sav[array]):
		index = sav[array + i*2 + 1]
		count = sav[array + i*2 + 2]
		name = items[index]
		names[name] = (index,count)
		print('{0:03d} {1:02d} {2}'.format(index,count,name))
	print()

	for i, key in enumerate(dict(sorted(names.items()))):
		sav[array + i*2 + 1] = names[key][0]
		sav[array + i*2 + 2] = names[key][1]

	print('New Order:\n')
	for i in range(sav[array]):
		index = sav[array + i*2 + 1]
		count = sav[array + i*2 + 2]
		name = items[index]
		names[name] = (index,count)
		print('{0:03d} {1:02d} {2}'.format(index,count,name))
	print('\n')

	return

def text_edit(address, length, label):
	letters = list(eng_index.values())
	letters = [l for l in letters if l != '@']
	allowed = ''.join(letters)
	letters = [l.replace('[', '\\[') for l in letters]
	letters = [l.replace(']', '\\]') for l in letters]
	letters = [l.replace('-', '\\-') for l in letters]

	print('Allowed letters: \n\n' + allowed)
	print('\nUse: + for ♀ (female), ^ for ♂ (male), % for PK, $ for MN, * for x (times symbol)')
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
	sav[address+i+1] = 0x50
	
	print()

	return

def num_edit(address, length, label, endian):
	if endian == 'big':
		mx = 0x100 ** length - 1
		value = 0
		for i in range(address,address+length): value = ((value << 8) | sav[i])
	if endian == 'lit':
		mx = 0x100 ** length - 1
		value = 0
		for i in range(address+length-1,address-1,-1): value = ((value << 8) | sav[i])
	if endian == 'bcd':
		mx = int("99" * length)
		value = int(binascii.hexlify(sav[address:address+length]).decode())

	print('\nCurrent ' + label + ': ',end='')
	print(str(value))
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

	if endian == 'bcd':
		new = int('0x' + str(new),16)
		endian = 'big'
	if endian == 'big':
		for i in range(address+length-1,address-1,-1):
			sav[i] = new & 0xFF
			new = (new >> 8)
	if endian == 'lit':
		for i in range(address,address+length):
			sav[i] = new & 0xFF
			new = (new >> 8)

	print('\n')

	return

def dump_boxes():
	def dump_box(address):
		count = sav[address]

		for i, j in enumerate(range(count)):
			sid = sav[address + 1 + j]
			if sid == 0xFF: break
			level = sav[address + 0x16 + j * 0x21 + 0x03]
			name = poketoascii(address + 0x386 + j * 0xB,10)
			if sid_index[sid][1].casefold() == name.casefold(): name = ''
			print("{0:02d}. {2:03d} L{4:03d} {3:12s}{5}".format(i+1,sid,sid_index[sid][0],sid_index[sid][1],level,name))
		print()

	print()

	for box in range(0,12):
		base = 0x4000
		address = base + box * 0x462
		if box > 5:
			base = 0x6000
			address = base + (box - 6) * 0x462

		if box == (sav[0x284C] & 0x7F): address = 0x30C0

		count = sav[address]
		if count == 0 and box != (sav[0x284C] & 0x7F): continue

		print("Pokémon Box " + str(box + 1),end='')
		if box == (sav[0x284C] & 0x7F): print(" [Current]",end='')
		print()
		print()

		dump_box(address)

	print()

	return

def mew():
	for box in range(0,12):
		base = 0x4000
		address = base + box * 0x462
		if box > 5:
			base = 0x6000
			address = base + (box - 6) * 0x462
		#if box == (sav[0x284C] & 0x7F): continue
		if box == (sav[0x284C] & 0x7F): address = 0x30C0
		count = sav[address]
		if count < 20: break

	if box == 11 and count == 20:
		print('All Boxes Full!')
		return

	sav[address] = count + 1
	# data pulled from public sav file
	sid = 21
	#data = [21, 0, 25, 5, 0, 24, 24, 45, 1, 0, 0, 0, 0, 199, 0, 0, 135, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 161, 197, 35, 0, 0, 0]
	data = [21, 0, 31, 7, 0, 24, 24, 45, 1, 0, 0, 0, 0, 199, 0, 0, 236, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 161, 197, 35, 0, 0, 0]
	# protagonist ID
	data[0xC] = sav[0x2605]
	data[0xD] = sav[0x2606]
	# trainer = [152, 142, 146, 135, 136, 145, 128, 80, 80, 80, 80]
	# rename to protagonist name
	trainer = [0x50] * 0xB
	for i in range(0xB):
		if sav[0x2598+i] == 0x50: break
		trainer[i] = sav[0x2598+i]
	name = [140, 132, 150, 80, 80, 80, 80, 80, 80, 80, 80]

	sav[address + 1 + count] = 21
	sav[address + 1 + count + 1] = 0xFF
	for i, j in enumerate(data):
		sav[address + 0x16 + count * 0x21 + i] = j
	for i, j in enumerate(trainer):
		sav[address + 0x2AA + count * 0xB + i] = j
	for i, j in enumerate(name):
		sav[address + 0x386 + count * 0xB + i] = j

	own  = int.from_bytes(sav[0x25A3:0x25A3+0x13], byteorder='little')
	own |= (1 << (151 - 1))
	for i, j in enumerate(own.to_bytes(0x13, 'little')): sav[0x25A3+i] = j
	seen = int.from_bytes(sav[0x25B6:0x25B6+0x13], byteorder='little')
	seen |= (1 << (151 - 1))
	for i, j in enumerate(seen.to_bytes(0x13, 'little')): sav[0x25B6+i] = j

	print('Mew added to Pokédex and Box {}, Row {}\n'.format(box+1,count+1))

	return

def box_by_name():
	by_name = []

	print()

	for box in range(0,12):
		base = 0x4000
		address = base + box * 0x462
		if box > 5:
			base = 0x6000
			address = base + (box - 6) * 0x462

		if box == (sav[0x284C] & 0x7F): address = 0x30C0

		count = sav[address]
		if count == 0: continue

		current = " "
		if box == (sav[0x284C] & 0x7F): current = "C"

		for i, j in enumerate(range(count)):
			sid = sav[address + 1 + j]
			if sid == 0xFF: break
			level = sav[address + 0x16 + j * 0x21 + 0x03]
			name = poketoascii(address + 0x386 + j * 0xB, 10)
			if sid_index[sid][1].casefold() == name.casefold(): name = ''
			by_name.append("{5:02d} {6} {0:02d}. {2:03d} L{4:03d} {3:12s}{7}".format(i+1,sid,sid_index[sid][0],sid_index[sid][1],level,box+1,current,name))

	by_name.sort(key = lambda x: x[17:])
	for i in by_name:
		print(i)

	print()
	print()

	return

def box_party_nids():
	#a = [0] * 152
	a = ['☐'] * 152

	for box in range(0,12):
		base = 0x4000
		address = base + box * 0x462
		if box > 5:
			base = 0x6000
			address = base + (box - 6) * 0x462

		if box == (sav[0x284C] & 0x7F): address = 0x30C0

		count = sav[address]
		if count == 0: continue

		current = " "
		if box == (sav[0x284C] & 0x7F): current = "C"

		for i, j in enumerate(range(count)):
			sid = sav[address + 1 + j]
			if sid == 0xFF: break
			#a[sid_index[sid][0]] = 1
			a[sid_index[sid][0]] = '■'

	address = 0x2F2C
	count = sav[address]

	for i in range(count):
		sid = sav[address + 1 + i]
		if sid == 0xFF: break
		#a[sid_index[sid][0]] = 1
		a[sid_index[sid][0]] = '●'

	return a

def pokedex():
	own  = int.from_bytes(sav[0x25A3:0x25A3+0x13], byteorder='little')
	seen = int.from_bytes(sav[0x25B6:0x25B6+0x13], byteorder='little')
	by_name = {}
	nid_list = []
	name_list = []
	nids = box_party_nids()

	print()
	print("Seen: {0:d} Owned: {1:d}\n".format(seen.bit_count(),own.bit_count()))

	for nid in dict(nid_index):
		o = s = " "
		if own & 1: o = pokeball
		if seen & 1: s = "S"
		#n = '☐'
		#if nids[nid] == 1: n = '■'
		n = nids[nid]
		own >>= 1
		seen >>= 1
		str="{0:03d}. {1} {4} {2} {3}".format(nid,s,o,nid_index[nid][1],n)
		by_name[nid_index[nid][1]] = str
		nid_list.append(str)

	name_list = list(collections.OrderedDict(sorted(by_name.items())).values())

	maxlen = len(max(nid_list, key=len))
	for i,j in zip(nid_list, name_list):
		print("%s\t%s" % (i.ljust(maxlen, " "), j))

	print()
	print()

	return

def party():
	address = 0x2F2C
	count = sav[address]

	while True:
		party_list = ['Return']

		for i in range(count):
			sid = sav[address + 1 + i]
			if sid == 0xFF: break
			level = sav[address + 0x8 + i * 0x2C + 0x21]
			name = poketoascii(address + 0x152 + i * 0xB,10)
			party_list.append("{2:03d} L{4:03d} {3:11s} {5}".format(i+1,sid,sid_index[sid][0],sid_index[sid][1],level,name))

		sel = menu('Select Pokémon to Rename:',party_list,0,1,[])
		if sel == 0: return
		text_edit(address + 0x152 + (sel-1) * 0xB, 0xA, 'Name')

	return

def hof():
	address = 0x0598
	count = sav[0x284E]

	for i in range(count):
		print("Hall of Fame " + str(i+1))
		print()
		for j in range(6):
			sid   = sav[address + 0x10 * i + j * 0x10]
			level = sav[address + 0x10 * i + j * 0x10 + 0x01]
			n     =     address + 0x10 * i + j * 0x10 + 0x02
			name = poketoascii(n,10)
			print("{2:03d} L{4:03d} {3:11s} {5}".format(j+1,sid,sid_index[sid][0],sid_index[sid][1],level,name))
		print()

	return

def edit_wild(address,wild_type):
	mx = 100
	probs = [25, 15, 15, 10, 10, 10, 5, 5, 4, 1]
	longest = len(max(list(zip(*list(nid_index.values())))[1], key = len))
	rates = {}
	levels = {}
	nid = {}
	own  = int.from_bytes(sav[0x25A3:0x25A3+0x13], byteorder='little')

	print('Current ' + wild_type + ' Table:\n')
	for p, i in enumerate(range(address, address + 0xB + 0x9,2)):
		if sid_index[sav[i+1]][1] in rates.keys():
			rates[sid_index[sav[i+1]][1]] += probs[p]
		else:
			rates[sid_index[sav[i+1]][1]] = probs[p]
		if sid_index[sav[i+1]][1] in levels.keys():
			levels[sid_index[sav[i+1]][1]] += ", "
			levels[sid_index[sav[i+1]][1]] += str(sav[i])
		else:
			levels[sid_index[sav[i+1]][1]] = str(sav[i])
		nid[sid_index[sav[i+1]][1]] = sid_index[sav[i+1]][0]
		format_string = "L{0:03d} {1:" + str(longest) + "s}  {2:2d}%"
		print(format_string.format(sav[i],sid_index[sav[i+1]][1],probs[p]))
	print()

	longest_levels = len(max(list(levels.values()), key=len))
	print('Current ' + wild_type + ' Rate:\n')
	for i in dict(sorted(rates.items(), key=lambda item: item[1],reverse=True)):
		format_string  = "{3} {4:03d}. {0:" + str(longest) + "s}  "
		format_string += "{1:" + str(longest_levels) + "s}   "
		format_string += "{2:2d}%"
		ball = ' '
		if own & (1 << (nid[i] - 1)): ball = pokeball
		print(format_string.format(i, levels[i], rates[i], ball, nid[i]))
	print()

	nid_list = ['Return']
	for nid in dict(nid_index):
		nid_list.append(nid_index[nid][1])

	sel = menu('Select next ' + wild_type + ' Pokémon:',nid_list,1,1,[])
	if sel == 0: return

	while True:
		try:
			level = int(input('Level (1-' + str(mx) + '): '))
			if level > mx or level < 1:
				print("\nOut of range. Try again...\n")
				continue
			break
		except ValueError:
			print("\nNot a number. Try again...\n")
		except Exception as err:
			print(f"Unexpected {err=}, {type(err)=}")
			raise

	for i in range(address, address + 0xB + 0x9,2):
		sav[i] = level
		sav[i+1] = nid_index[sel][0]

	print()

	return

def poketoascii(address,length):
	s = ''
	for i in range(length):
		if sav[address+i] == 0x50: break
		s += eng_index[sav[address+i]]
	s = s.replace('+','♀')
	s = s.replace('^','♂')

	return s

def playtime():
	print("Current Play Time: {0:d}:{1:02d}:{2:02d}:{3:02d}\n".format(sav[0x2CED],sav[0x2CEF],sav[0x2CF0],sav[0x2CF1]))

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

	sav[0x2CED] = h
	sav[0x2CEF] = m
	sav[0x2CF0] = s
	sav[0x2CF1] = f

	print()

	return

def toggle_events():
	while True:
		event_bits = bits = int.from_bytes(sav[0x29F3:0x29F3+0x140], byteorder='little')

		print('Toggle Events\n')

		for i in range(0x140 * 0x8):
			event = "UNDEFINED"
			if i in events.keys(): event = events[i]
			o = '☐'
			if bits & 1: o = '■'
			bits >>= 1
			if event == "UNDEFINED" and o == '☐': continue
			print("{2:04d} {0} {1}".format(o,event,i+1))

		print()

		while True:
			try:
				e = int(input("Toggle Event (1-" + str(0x140 * 0x8) + ") ['0' to Exit]: "))
				if e > 0x140 * 0x8 or e < 0:
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

		event_bits ^= (1 << (e - 1))
		for i, j in enumerate(event_bits.to_bytes(0x140, 'little')): sav[0x29F3+i] = j

	print()

	return

def writeout():
	chksum = 0
	for i in range(0x2598,0x3522+1): chksum += sav[i]

	chksum &= 0xFF
	chksum1 = 0x3523

	sav[chksum1] = (chksum ^ 0xFF)

	try:
		f = open(outputfilename,'wb')
		f.write(sav)
		f.close()
	except Exception as err:
		print(f"Unexpected {err=}, {type(err)=}")
		raise

	print(outputfilename + "' written out, enjoy!\n")

	return


### main

init_dicts_arrays()

# open and read save file

if len(sys.argv) != 2:
	print("\nUsage: " + sys.argv[0] + " [.sav file name]\n")
	sys.exit(1)

try:
	sav = bytearray(open(sys.argv[1],'rb').read())
except Exception as err:
	print(f"Unexpected {err=}, {type(err)=}")
	raise

print("\nPokémon Red/Blue/Yellow Savefile Editor v" + version)
print("\nUSE AT YOUR OWN PERIL!!!\n")

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
			array_menu,
			[0x25C9, MAX_ITEMS, 'ITEM']
		),
		(
			'Sort Items', 
			array_sort,
			[0x25C9, MAX_ITEMS, 'ITEM']
		),
		(
			'Box Items', 
			array_menu,
			[0x27E6, MAX_BOX_ITEMS, 'ITEM']
		),
		(
			'Sort Box Items', 
			array_sort,
			[0x27E6, MAX_BOX_ITEMS, 'ITEM']
		),
		(
			'Edit ID: ' + str((sav[0x2605] << 8) | sav[0x2606]),
			num_edit,
			[0x2605, 2, 'ID', 'big']
		),
		(
			'Edit Player Name: ' + poketoascii(0x2598,7),
			text_edit,
			[0x2598, 7, 'Player Name']
		),
		(
			'Edit Rival Name: ' + poketoascii(0x25F6,7),
			text_edit,
			[0x25F6, 7, 'Rival Name']
		),
		(
			'Edit Money: ' + binascii.hexlify(sav[0x25F3:0x25F3+3]).decode(),
			num_edit,
			[0x25F3, 3, 'Money', 'bcd']
		),
		(
			'Edit Coins: ' + binascii.hexlify(sav[0x2850:0x2850+2]).decode(),
			num_edit,
			[0x2850, 2, 'Coins', 'bcd']
		),
		(
			'Edit Pikachu Friendship (Yellow): ' + str(sav[0x271C]),
			num_edit,
			[0x271C, 1, 'Friendship', 'lit']
		),
		(
			'Edit Wild Pokémon Table',
			edit_wild,
			[0x2B34, 'Wild']
		),
		(
			'Edit Surf Pokémon Table',
			edit_wild,
			[0x2B51, 'Surf']
		),
		(
			'Edit Party Names',
			party,
			[]
		),
		(
			'Edit Play Time: {0:d}:{1:02d}:{2:02d}:{3:02d}'.format(sav[0x2CED],sav[0x2CEF],sav[0x2CF0],sav[0x2CF1]),
			playtime,
			[]
		),
		(
			'Toggle Events',
			toggle_events,
			[]
		),
		(
			"Bill's PC [by box] (read only)",
			dump_boxes,
			[]
		),
		(
			"Bill's PC [by name] (read only)",
			box_by_name,
			[]
		),
		(
			'Pokédex (read only)',
			pokedex,
			[]
		),
		(
			'Hall of Fame (read only)',
			hof,
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


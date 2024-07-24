#!/usr/bin/env python3

import sys
import os
import re
import binascii
import collections

# globals
outputfilename = 'newbag.sav'
version = "0.10.1"
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

		sub_sel = menu(main_menu[sel] + ' Menu (Select ' + main_menu[sel] + ' to increase to 99), ' + str(sav[array]) + ' of ' + str(max_items) + ' array elements assigned',sub_menu,1,max_items - sav[array],count)

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
	a = [0] * 152

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
			a[sid_index[sid][0]] = 1

	address = 0x2F2C
	count = sav[address]

	for i in range(count):
		sid = sav[address + 1 + i]
		if sid == 0xFF: break
		a[sid_index[sid][0]] = 1

	return a

def pokedex():
	own  = int.from_bytes(sav[0x25A3:0x25A3+0x13], byteorder='little')
	seen = int.from_bytes(sav[0x25B6:0x25B6+0x13], byteorder='little')
	by_name = {}
	nid_list = []
	name_list = []
	nids = box_party_nids()

	print()
	print("Seen: {0:d} Own: {1:d}\n".format(seen.bit_count(),own.bit_count()))

	for nid in dict(nid_index):
		o = s = " "
		if own & 1: o = pokeball
		if seen & 1: s = "S"
		n = '☐'
		if nids[nid] == 1: n = '■'
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
print("Play time: {0:02d}:{1:02d}:{2:02d}\n".format(sav[0x2CED],sav[0x2CEF],sav[0x2CF0]))

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
			'Edit Protagonist Name: ' + poketoascii(0x2598,7),
			text_edit,
			[0x2598, 7, 'Protagonist Name']
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


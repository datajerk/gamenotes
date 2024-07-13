#!/usr/bin/env python3

import sys
import os


# globals
outputfilename = 'newbag.sav'
version = "0.0.1"
item_count = {}
longest_item = 0

MAX_ITEMS = 20

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
	196: 'HM01',
	197: 'HM02',
	198: 'HM03',
	199: 'HM04',
	200: 'HM05',
	201: 'TM01',
	202: 'TM02',
	203: 'TM03',
	204: 'TM04',
	205: 'TM05',
	206: 'TM06',
	207: 'TM07',
	208: 'TM08',
	209: 'TM09',
	210: 'TM10',
	211: 'TM11',
	212: 'TM12',
	213: 'TM13',
	214: 'TM14',
	215: 'TM15',
	216: 'TM16',
	217: 'TM17',
	218: 'TM18',
	219: 'TM19',
	220: 'TM20',
	221: 'TM21',
	222: 'TM22',
	223: 'TM23',
	224: 'TM24',
	225: 'TM25',
	226: 'TM26',
	227: 'TM27',
	228: 'TM28',
	229: 'TM29',
	230: 'TM30',
	231: 'TM31',
	232: 'TM32',
	233: 'TM33',
	234: 'TM34',
	235: 'TM35',
	236: 'TM36',
	237: 'TM37',
	238: 'TM38',
	239: 'TM39',
	240: 'TM40',
	241: 'TM41',
	242: 'TM42',
	243: 'TM43',
	244: 'TM44',
	245: 'TM45',
	246: 'TM46',
	247: 'TM47',
	248: 'TM48',
	249: 'TM49',
	250: 'TM50',
	251: 'TM51',
	252: 'TM52',
	253: 'TM53',
	254: 'TM54',
	255: 'TM55',
}

item_names = {
	'Master Ball': 1,
	'Ultra Ball': 2,
	'Great Ball': 3,
	'Poké Ball': 4,
	'Town Map': 5,
	'Bicycle': 6,
	'?????': 7,
	'Safari Ball': 8,
	'Pokédex': 9,
	'Moon Stone': 10,
	'Antidote': 11,
	'Burn Heal': 12,
	'Ice Heal': 13,
	'Awakening': 14,
	'Parlyz Heal': 15,
	'Full Restore': 16,
	'Max Potion': 17,
	'Hyper Potion': 18,
	'Super Potion': 19,
	'Potion': 20,
	'BoulderBadge': 21,
	'CascadeBadge': 22,
	'ThunderBadge': 23,
	'RainbowBadge': 24,
	'SoulBadge': 25,
	'MarshBadge': 26,
	'VolcanoBadge': 27,
	'EarthBadge': 28,
	'Escape Rope': 29,
	'Repel': 30,
	'Old Amber': 31,
	'Fire Stone': 32,
	'Thunderstone': 33,
	'Water Stone': 34,
	'HP Up': 35,
	'Protein': 36,
	'Iron': 37,
	'Carbos': 38,
	'Calcium': 39,
	'Rare Candy': 40,
	'Dome Fossil': 41,
	'Helix Fossil': 42,
	'Secret Key': 43,
	'?????': 44,
	'Bike Voucher': 45,
	'X Accuracy': 46,
	'Leaf Stone': 47,
	'Card Key': 48,
	'Nugget': 49,
	'PP Up*': 50,
	'Poké Doll': 51,
	'Full Heal': 52,
	'Revive': 53,
	'Max Revive': 54,
	'Guard Spec.': 55,
	'Super Repel': 56,
	'Max Repel': 57,
	'Dire Hit': 58,
	'Coin': 59,
	'Fresh Water': 60,
	'Soda Pop': 61,
	'Lemonade': 62,
	'S.S. Ticket': 63,
	'Gold Teeth': 64,
	'X Attack': 65,
	'X Defend': 66,
	'X Speed': 67,
	'X Special': 68,
	'Coin Case': 69,
	'Oak\'s Parcel': 70,
	'Itemfinder': 71,
	'Silph Scope': 72,
	'Poké Flute': 73,
	'Lift Key': 74,
	'Exp. All': 75,
	'Old Rod': 76,
	'Good Rod': 77,
	'Super Rod': 78,
	'PP Up': 79,
	'Ether': 80,
	'Max Ether': 81,
	'Elixer': 82,
	'Max Elixer': 83,
	'HM01': 196,
	'HM02': 197,
	'HM03': 198,
	'HM04': 199,
	'HM05': 200,
	'TM01': 201,
	'TM02': 202,
	'TM03': 203,
	'TM04': 204,
	'TM05': 205,
	'TM06': 206,
	'TM07': 207,
	'TM08': 208,
	'TM09': 209,
	'TM10': 210,
	'TM11': 211,
	'TM12': 212,
	'TM13': 213,
	'TM14': 214,
	'TM15': 215,
	'TM16': 216,
	'TM17': 217,
	'TM18': 218,
	'TM19': 219,
	'TM20': 220,
	'TM21': 221,
	'TM22': 222,
	'TM23': 223,
	'TM24': 224,
	'TM25': 225,
	'TM26': 226,
	'TM27': 227,
	'TM28': 228,
	'TM29': 229,
	'TM30': 230,
	'TM31': 231,
	'TM32': 232,
	'TM33': 233,
	'TM34': 234,
	'TM35': 235,
	'TM36': 236,
	'TM37': 237,
	'TM38': 238,
	'TM39': 239,
	'TM40': 240,
	'TM41': 241,
	'TM42': 242,
	'TM43': 243,
	'TM44': 244,
	'TM45': 245,
	'TM46': 246,
	'TM47': 247,
	'TM48': 248,
	'TM49': 249,
	'TM50': 250,
	'TM51': 251,
	'TM52': 252,
	'TM53': 253,
	'TM54': 254,
	'TM55': 255,
}


# functions

def init_dicts_arrays():
	global longest_item

	for key in dict(items):
		item_count[key] = 0
		if len(items[key]) > longest_item: longest_item = len(items[key])
	return


def menu(title, menu_items, orientation, left):
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
			if left == 0 and sel != 0:
				print("\nBag full of this type of item, 'return' is your only option. Try again...\n")
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
		sub_menu = ['Return']
		for i in range(sav[array]):
			item_index = sav[array + i*2 + 1]
			item_count[item_index] = sav[array + i*2 + 2]

		for item_index in dict(items):
			format_string = '{:' + str(longest_item + 1) + '} {:2}'
			sub_menu.append(format_string.format(items[item_index] + ':', item_count[item_index]))

		sub_sel = menu(main_menu[sel] + ' Menu (Select ' + main_menu[sel] + ' to increase to 99), ' + str(sav[array]) + ' of ' + str(max_items) + ' array elements assigned',sub_menu,1,max_items - sav[array])

		if sub_sel == 0: break

		item = sub_menu[sub_sel].split(':')[0]
		target_index = item_names[item]

		for i in range(sav[array]):
			item_index = sav[array + i*2 + 1]
			if target_index == item_index: break

		if target_index != item_index:
			i += 1
			sav[array + i*2 + 1] = target_index
			sav[array + i*2 + 3] = 0xff
			sav[array] += 1

		sav[array + i*2 + 2] = 99

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

print("\nPokémon Red Offline Store v" + version)
print("\nUSE AT YOUR OWN PERIL!!!\n")
print("Let's go shopping!\n\n")

sel = -1
while sel != 0:
	main_menu = [
		'Exit [and [over]write "' + outputfilename + '"]',
		'Item', 
		'[Over]write "' + outputfilename + '" and continue shopping',
		'Abort! (all changes since last write lost)'
	]

	sel = menu('Main Menu',main_menu,0,1)

	if sel == 1: array_menu(0x25C9, MAX_ITEMS, 'ITEM')
	if sel == 2: writeout()
	if sel == 3: sys.exit(0)

writeout()
sys.exit(0)


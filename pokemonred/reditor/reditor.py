#!/usr/bin/env python3

import sys
import os
import re


# globals
outputfilename = 'newbag.sav'
version = "0.0.5"
item_names = {}
eng_letter = {}
longest_item = 0

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
	count = [0]
	item_count = {}
	for key in dict(items): item_count[key] = 0
	while (sub_sel != 0):
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
				q = int(input('Quantity (1-99): '))
				if q > 99 or q < 1:
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

		if target_index != item_index:
			i += 1
			sav[array + i*2 + 1] = target_index
			sav[array + i*2 + 3] = 0xff
			sav[array] += 1

		sav[array + i*2 + 2] = q

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
	letters = [l.replace('[', '\[') for l in letters]
	letters = [l.replace(']', '\]') for l in letters]
	letters = [l.replace('-', '\-') for l in letters]

	print('\nAllowed letters: \n\n' + allowed)
	print('\nUse: + for gender femail, ^ for gender mail, % for PK, $ for MN, * for "times" symbol ("x")')
	print("\nMax length: " + str(length))
	print('\nCurrent ' + label + ': ',end='')

	text = ''
	for i in range(7):
		if sav[address+i] == 0x50: break
		text += eng_index[sav[address+i]]

	print(text)
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
			if not re.match("^[" + "".join(letters) + "]{1,7}$", new):
				print("\nInvalid character(s)\n")
				continue
			break
		except Exception as err:
			print(f"Unexpected {err=}, {type(err)=}")
			raise

	for i in range(len(new)): sav[address+i] = eng_letter[new[i]]
	sav[address+i+1] = 0x50
	
	print('\n')

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
	rival = ''
	for i in range(7):
		if sav[0x25F6+i] == 0x50: break
		rival += eng_index[sav[0x25F6+i]]

	protagonist = ''
	for i in range(7):
		if sav[0x2598+i] == 0x50: break
		protagonist += eng_index[sav[0x2598+i]]

	main_menu = [
		'Exit [and [over]write "' + outputfilename + '"]',
		'Items', 
		'Sort Items', 
		'Box Items', 
		'Sort Box Items', 
		'Edit Rival Name: ' + rival,
		'Edit Protagonist Name: ' + protagonist,
		'[Over]write "' + outputfilename + '" and continue shopping',
		'Abort! (all changes since last write lost)'
	]

	sel = menu('Main Menu',main_menu,0,1,[])

	if sel == 1: array_menu(0x25C9, MAX_ITEMS, 'ITEM')
	if sel == 2: array_sort(0x25C9, MAX_ITEMS, 'ITEM')
	if sel == 3: array_menu(0x27E6, MAX_BOX_ITEMS, 'ITEM')
	if sel == 4: array_sort(0x27E6, MAX_BOX_ITEMS, 'ITEM')
	if sel == 5: text_edit(0x25F6, 7, 'Rival')
	if sel == 6: text_edit(0x2598, 7, 'Protagonist')
	if sel == 7: writeout()
	if sel == 8: sys.exit(0)

writeout()
sys.exit(0)


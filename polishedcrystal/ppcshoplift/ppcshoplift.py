#!/usr/bin/env python3

import sys
import os


# globals
items = {}
item_names = {}
longest_item_by_type = {}
tmhm = []
key_items = []
outputfilename = 'newbag.sav'
version = "0.0.4"

# constants/item_data_constants.asm
# too lazy to parse with code, hard coding for now
MAX_ITEMS     = 75
MAX_MEDICINE  = 37
MAX_BALLS     = 25
MAX_BERRIES   = 31

# ram/wramx.asm for how memory is laid out
COINS=0x237c   # 2 bytes big-endian
MONEY=0x2375   # 3 bytes big-endian
MMONEY=MONEY+3 # 3 bytes big-endian


# functions

def init_dicts_arrays():
	try:
		lines = open('asm/attributes.asm','r').readlines()
	except Exception as err:
		print(f"Unexpected {err=}, {type(err)=}")
		raise

	for i in range(len(lines)):
		if lines[i].strip() == 'ItemAttributes:': break

	item_index = 0
	for i in range(i+2,len(lines),2):
		if lines[i].find('assert_table_length') != -1: break
		item = lines[i].strip()[2:]
		item_type = lines[i+1].strip().split(', ')[3];

		if not item_type in longest_item_by_type:
			longest_item_by_type[item_type] = len(item)

		if len(item) > longest_item_by_type[item_type]: longest_item_by_type[item_type] = len(item)

		item_index += 1
		items[item] = (item_index,item_type, 0)
		item_names[item_index] = item

	try:
		lines = open('asm/tmhm_constants.asm','r').readlines()
	except Exception as err:
		print(f"Unexpected {err=}, {type(err)=}")
		raise

	for i in range(len(lines)):
		if lines[i].find('add_tm ') != -1: break

	c = 0
	for i in range(i,len(lines)):
		if lines[i].find('add_hm ') != -1: break
		if lines[i].find('add_tm ') == -1: continue
		c += 1
		tmhm.append('{:02} {}'.format(c,lines[i].strip().split()[1]))

	c = 0
	for i in range(i,len(lines)):
		if lines[i].find('add_mt ') != -1: break
		if lines[i].find('add_hm ') == -1: continue
		c += 1
		tmhm.append('H{} {}'.format(c,lines[i].strip().split()[1]))

#	for i in range(i,len(lines)):
#		if lines[i].find('add_mt ') == -1: break
#		tmhm.append(lines[i].strip().split()[1])

	try:
		lines = open('asm/item_constants.asm','r').readlines()
	except Exception as err:
		print(f"Unexpected {err=}, {type(err)=}")
		raise

	for i in range(len(lines)):
		if lines[i].find('BICYCLE') != -1: break

	for i in range(i,len(lines)):
		if lines[i].find('NUM_KEY_ITEMS') != -1: break
		key_items.append(lines[i].strip().split()[1])

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
			count = sav[array + i*2 + 2]
			item = item_names[item_index]
			items[item] = (item_index, items[item][1], count)

		for item in dict(sorted(items.items())):
			item_index, item_type, count = items[item]
			if item_type == item_type_filter:
				format_string = '{:' + str(longest_item_by_type[item_type] + 1) + '} {:2}'
				sub_menu.append(format_string.format(item + ':', count))

		sub_sel = menu(main_menu[sel] + ' Menu (Select ' + main_menu[sel] + ' to increase to 99), ' + str(sav[array]) + ' of ' + str(max_items) + ' array elements assigned',sub_menu,1,max_items - sav[array])

		if sub_sel == 0: break

		item = sub_menu[sub_sel].split(':')[0]
		target_index = items[item][0]

		for i in range(sav[array]):
			item_index = sav[array + i*2 + 1]
			if target_index == item_index: break

		if target_index != item_index:
			i += 1
			sav[array + i*2 + 1] = items[item][0]
			sav[array + i*2 + 3] = 0xff
			sav[array] += 1

		sav[array + i*2 + 2] = 99

	return

def bit_array_menu(array, length, bit_array_type, array_labels):
	sub_sel = -1
	while (sub_sel != 0):
		bits = int.from_bytes(sav[array:array+length], byteorder='little')
		max_label_len = len(max(array_labels, key=len))
		sub_menu = ['Return']

		for i in range(len(array_labels)):
			format_string = '{:' + str(max_label_len + 1) + '} {}'
			sub_menu.append(format_string.format(array_labels[i] + ':', bits & 1))
			bits >>= 1

		sub_sel = menu(main_menu[sel] + ' Menu (Select ' + main_menu[sel] + ' to toggle bit)',sub_menu,1,1)
		bits = int.from_bytes(sav[array:array+length], byteorder='little')
		if sub_sel > 0:
			bits ^= (1 << (sub_sel - 1))
			for i, j in enumerate(bits.to_bytes(length, 'little')): sav[array+i] = j

	return

def apricorn_menu():
	apricorn_colors = ['Red', 'Blu', 'Ylw', 'Grn', 'Wht', 'Blk', 'Pnk']
	array=0x253E
	length=len(apricorn_colors)

	sub_sel = -1
	while (sub_sel != 0):
		sub_menu = ['Return']
		for i in range(length): sub_menu.append(apricorn_colors[i] + ": " + str(sav[array + i]))
		sub_sel = menu(main_menu[sel] + ' Menu (Select ' + main_menu[sel] + ' to increase to 99)',sub_menu,0,1)
		if sub_sel: sav[array + sub_sel - 1] = 99

	return

def writeout():
	# copy main to backup and compute chksum
			
	chksum = 0
	for i in range(0x2008,0x2B83):
		sav[i - (0x2008 - 0x1208)] = sav[i]
		chksum += sav[i]

	chksum &= 0xFFFF
	chksum1 = 0x2D0D
	chksum2 = 0x1F0D

	sav[chksum1+0] = sav[chksum2+0] = (chksum & 0xFF)
	sav[chksum1+1] = sav[chksum2+1] = (chksum >> 8)

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

print("\nPokémon Polished Crystal 3.0.0-beta Offline Store v" + version)
print("(Tested ROM (polishedcrystal-3.0.0-beta-22d6f8e1.gbc) md5sum 64276e3acc3fda02e0dcc235c9c2748a)\n")
print("USE AT YOUR OWN PERIL!!!\n")
print("Let's go shopping!\n")
print("Money:     " + str((sav[MONEY] << 16) | (sav[MONEY+1] << 8) | sav[MONEY+2]))
print("Mom Money: " + str((sav[MMONEY] << 16) | (sav[MMONEY+1] << 8) | sav[MMONEY+2]))
print("\n")

#sav[MONEY]   = 9999999 >> 16
#sav[MONEY+1] = (9999999 >> 8) & 0xFF
#sav[MONEY+2] = 9999999 & 0xFF

sel = -1
while sel != 0:
	main_menu = [
		'Exit [and [over]write "' + outputfilename + '"]',
		'Item', 'Med', 'Ball', 'TH/HM', 'Berry', 'Key Item', 'Apricorn',
		'Max Coins (current count: ' + str((sav[COINS] << 8) | sav[COINS+1]) + ')',
		'[Over]write "' + outputfilename + '" and continue shopping',
		'Abort! (all changes since last write lost)'
	]

	sel = menu('Main Menu',main_menu,0,1)

	if sel == 1: array_menu(0x2394, MAX_ITEMS, 'ITEM')
	if sel == 2: array_menu(0x242C, MAX_MEDICINE, 'MEDICINE')
	if sel == 3: array_menu(0x2478, MAX_BALLS, 'BALL')
	if sel == 4: bit_array_menu(0x2385, 11, main_menu[sel], tmhm)
	if sel == 5: array_menu(0x24AC, MAX_BERRIES, 'BERRIES')
	if sel == 6: bit_array_menu(0x2390,  4, main_menu[sel], key_items)
	if sel == 7: apricorn_menu()
	if sel == 8:
		sav[COINS+0] = (50000 >> 8)
		sav[COINS+1] = (50000 & 0xFF)
	if sel == 9: writeout()
	if sel == 10: sys.exit(0)

writeout()
sys.exit(0)


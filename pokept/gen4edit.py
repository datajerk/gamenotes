#!/usr/bin/env python3

import sys
import os
import re
import math
import itertools

#from ctypes import *
from dicts import *
from structs import *
from constants import *
from PIL import Image
import re


### functions

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
			print("\nNot an integer. Try again...\n")
		except Exception as err:
			print(f"Unexpected {err=}, {type(err)=}")
			raise
	print()
	return sel

def writeout(outputfilename,savedata,g,s):
	if g.contents.footer.chksum != 0xFFFF:
		g.contents.footer.chksum = crc_ccitt_16(bytes(g.contents.data) + bytes(g.contents.padding))

	if s.contents.footer.chksum != 0xFFFF:
		s.contents.footer.chksum = crc_ccitt_16(bytes(s.contents.data) + bytes(s.contents.padding))

	try:
		f = open(outputfilename,'wb')
		f.write(bytes(savedata))
		f.close()
	except Exception as err:
		print(f"Unexpected {err=}, {type(err)=}")
		raise

	print(outputfilename + "' written out, enjoy!\n")
	return

def crc_ccitt_16(data):
	crc = 0xFFFF 
	for byte in data:
		crc ^= (byte << 8) 
		for _ in range(8):
			if crc & 0x8000:  
				crc = (crc << 1) ^ 0x1021 
			else:
				crc <<= 1 
 
			crc &= 0xFFFF

	return crc

def dump_struct(struct):
	print(struct.__name__ + ' structure:\n')
	for field_name,field_type in struct._fields_:
		print('{0:<30}{1:>10}{2:>10}{3:>10}'.format(
			field_name,
			hex(getattr(getattr(struct,field_name),'offset')),
			hex(getattr(getattr(struct,field_name),'size')),
			int(getattr(getattr(struct,field_name),'size')),
		))

	print('sizeof: ' + str(sizeof(struct)) + ' bytes')
	print('sizeof: ' + hex(sizeof(struct)) + ' bytes')
	print()
	return

def edit_number(label, p, field, mx=None):
	value = getattr(p, field)
	print('Current ' + label + ':',value,end='\n')

	while True:
		try:
			new = int(input('New ' + label + ' range(0-' + str(mx) + '): '))
			if new > mx or new < 0:
				print("\nOut of range. Try again...\n")
				continue
			break
		except ValueError:
			print("\nNot an integer. Try again...\n")
		except Exception as err:
			print(f"Unexpected {err=}, {type(err)=}")
			raise

	setattr(p, field, new)
	return

def toggle_number(p, field):
	setattr(p, field, getattr(p, field) ^ 1)
	return

def items(p, pocket, slots):
	sub_sel = -1
	while (sub_sel != 0):
		items_count = {i: 0 for i in [k for k, v in items_pocket.items() if v == pocket]}
		items_count.update({i.id:i.q for i in p if i.id > 0})
		used_slots = len({i.id:i.q for i in p if i.id > 0})
		items_name2id = {items_name[i]: i for i, q in items_count.items()}
		items_name_q = {items_name[i]: q for i, q in items_count.items()}
		longest_name_len = len(max(list(items_name_q.keys()), key=len))
		format_string = '{0:' + str(longest_name_len) + 's}  {1:3d}'
		sub_menu = ['Return'] + [format_string.format(n,q) for n, q in dict(sorted(items_name_q.items())).items()]
		count = [0] + [q for n, q in dict(sorted(items_name_q.items())).items()]
		menu2id=dict(
			enumerate(
				list(
					dict(
						sorted(
							{n:i for n, i in items_name2id.items() if i > 0}.items()
						)
					).values()
				)
				,1)
			)

		o = 0 if len(sub_menu) < 20 else 1 
		sub_sel = menu(main_menu[sel] +
		 	' Menu (Select ' +
			main_menu[sel] +
			' to Edit, ' +
			str(used_slots) +
			' of ' + str(slots) +
			' array elements assigned)',
			sub_menu,o,slots - used_slots,count)

		if sub_sel == 0: break

		while True:
			try:
				q = int(input('Quantity (0-999): '))
				if q > 999 or q < 0:
					print("\nOut of range. Try again...\n")
					continue
				break
			except ValueError:
				print("\nNot an integer. Try again...\n")
			except Exception as err:
				print(f"Unexpected {err=}, {type(err)=}")
				raise

		items_count[menu2id[sub_sel]]=q

		a = 0
		for n, i in dict(sorted(items_name2id.items())).items():
			if items_count[i] > 0:
				p[a].id = i
				p[a].q = items_count[i]
				a+=1

		for i in range(a,slots,1): p[i].id = p[i].q = 0

		print()

	return

def sort_items(p, pocket, slots):
	items_count = {i: 0 for i in [k for k, v in items_pocket.items() if v == pocket]}
	items_count.update({i.id:i.q for i in p if i.id > 0})
	items_name2id = {items_name[i]: i for i, q in items_count.items()}

	a = 0
	for n, i in dict(sorted(items_name2id.items())).items():
		if items_count[i] > 0:
			p[a].id = i
			p[a].q = items_count[i]
			a+=1

	for i in range(a,slots,1): p[i].id = p[i].q = 0

	return

def sort_all_items(t):

	for i in t: sort_items(*i)

	return

def read_string(p, mx=100):
	s = ''
	for i in range(mx):
		if p[i].char == 0xFFFF: break
		s += chars[p[i].char]

	return s

def dump_string(p, mx=0):
	for i in range(mx):
		if p[i].char == 0xFFFF: break
		print(p[i].char,end=' ')

	print()

	for i in range(mx):
		if p[i].char == 0xFFFF: break
		print(hex(p[i].char),end=' ')

	print()
	return

#future support for special chars
def edit_string(label, p, mx=0):
	value = read_string(p, mx)
	print('Current ' + label + ':',value,end='\n')

	while True:
		try:
			new = input('New ' + label + ': ')
			if len(new) == 0:
				print("\nNo Change\n\n")
				return
			if len(new) > mx - 1:
				print("\nToo long, max length: " + str(mx - 1) + "\n")
				continue
			#future support for special chars
			#if not re.match("^[" + "".join(letters) + "]{1," + str(length) + "}$", new):
			#	print("\nInvalid character(s)\n")
			#	continue
			break
		except Exception as err:
			print(f"Unexpected {err=}, {type(err)=}")
			raise

	for i in range(len(new)): p[i].char = chars_i[new[i]]
	if len(new) < mx: p[len(new)].char = 0xFFFF
	return

def crypto(p,n,seed):
	last_seed = seed

	for i in range(n):
		next_seed = (((0x41C64E6D * last_seed) & 0xFFFFFFFF) + 0x6073) & 0xFFFFFFFF
		p[i] ^= (next_seed >> 16)
		last_seed = next_seed

	return

def pokemon_data_decrypt(p,n,box=0):
	pk = []

	for mon in range(n):
		crypto(p[mon].data.bitstream,64,p[mon].header.chksum)
		if not box: crypto(p[mon].battle_stats,50,p[mon].header.personality)
		assert(p[mon].header.chksum == sum(p[mon].data.bitstream) & 0xFFFF)

		k = ((p[mon].header.personality & 0x3e000) >> 0xd) % 24
		factoradic = []
		for i in range(4, 0, -1):
			factorial = math.factorial(i - 1)
			factoradic.append(k // factorial)
			k %= factorial	

		og_seq = []
		for i in range(3, -1, -1): og_seq.insert(factoradic[i], p[mon].data.blocks[i])

		a = cast(og_seq[0].block, POINTER(block_A))
		b = cast(og_seq[1].block, POINTER(block_B))
		c = cast(og_seq[2].block, POINTER(block_C))
		d = cast(og_seq[3].block, POINTER(block_D))

		pk.append([a,b,c,d])

	return pk

def pokemon_data_encrypt(p,n,box=0):
	for mon in range(n):
		p[mon].header.chksum = sum(p[mon].data.bitstream) & 0xFFFF
		crypto(p[mon].data.bitstream,64,p[mon].header.chksum)
		if not box: crypto(p[mon].battle_stats,50,p[mon].header.personality)

	return

def nop():
	return

def edit_pokemon(mon):
	a, b, c, d = range(4)

	ep_sel = -1
	while ep_sel != 0:
		edit_array = [
			(
				'Return',
				nop,
				[]
			),
			(
				"Name: " + read_string(mon[c].contents.nickname),
				edit_string,
				[
					'Pokémon Name',
					mon[c].contents.nickname,
					11
				]
			),
			(
				'Experience: ' + str(mon[a].contents.exp),
				edit_number,
				['Experience', mon[a].contents, 'exp', 2**32-1]
			),
			(
				'Friendship: ' + str(mon[a].contents.friendship),
				edit_number,
				['Friendship', mon[a].contents, 'friendship', 255]
			),
			(
				'Ability: ' + str(mon[a].contents.ability),
				edit_number,
				['Ability', mon[a].contents, 'ability', 255]
			),
			(
				'Markings: ' + str(mon[a].contents.markings),
				edit_number,
				['Markings', mon[a].contents, 'markings', 255]
			),
			(
				'Sheen: ' + str(mon[a].contents.sheen),
				edit_number,
				['Sheen', mon[a].contents, 'sheen', 255]
			),
			(
				'Cool: ' + str(mon[a].contents.cool),
				edit_number,
				['Cool', mon[a].contents, 'cool', 255]
			),
			(
				'Beauty: ' + str(mon[a].contents.beauty),
				edit_number,
				['Beauty', mon[a].contents, 'beauty', 255]
			),
			(
				'Cute: ' + str(mon[a].contents.cute),
				edit_number,
				['Cute', mon[a].contents, 'cute', 255]
			),
			(
				'Smart: ' + str(mon[a].contents.smart),
				edit_number,
				['Smart', mon[a].contents, 'smart', 255]
			),
			(
				'Tough: ' + str(mon[a].contents.tough),
				edit_number,
				['Tough', mon[a].contents, 'tough', 255]
			),
		]

		edit_menu = [x[0] for x in edit_array]
		ep_sel = menu('Edit Pokémon',edit_menu,0,1,[])
		ret = edit_array[ep_sel][1](*edit_array[ep_sel][2])

	return

def pokemon_menu(p,n):
	a, b, c, d = range(4)
	pk = pokemon_data_decrypt(p,n)

	pk_sel = -1
	while pk_sel != 0:
		poke_array = [
			(
				'Return',
				nop,
				[]
			),
		]

		for mon in range(n):
			poke_array.append(
				(
					'{0:11}  {1:11}  OT ID: {2:5}  Exp: {3:7}  Friendship: {4:3}'.format(
						read_string(pk[mon][c].contents.nickname),
						national_dex[pk[mon][a].contents.species_id],
						pk[mon][a].contents.ot_id,
						pk[mon][a].contents.exp,
						pk[mon][a].contents.friendship,
					),
					edit_pokemon,
					[
						pk[mon],
					]
				)
			)

		poke_menu = [x[0] for x in poke_array]
		pk_sel = menu('Pokémon Menu',poke_menu,0,1,[])
		ret = poke_array[pk_sel][1](*poke_array[pk_sel][2])

	pokemon_data_encrypt(p,n)

	return

def honey_tree_menu(p):
	tree_dict = {
		"Combee": [0,0,0],
		"Wurmple": [1,0,0],
		"Burmy": [2,0,0],
		"Cherubi": [3,0,0],
		"Aipom": [4,0,0],
		"Heracross": [5,1,0],
		"Munchlax": [5,2,0],
	}
	sub_sel = -1
	while sub_sel != 0:
		tree_array = [
			(
				'Return',
				nop,
				[]
			),
		]

		for key in tree_dict:
			tree_array.append(
				(
					key,
					honey_tree_hack,
					[
						p,
						key,
						tree_dict[key],
					]
				)
			)

		tree_menu = [x[0] for x in tree_array]
		sub_sel = menu('Select encounter for all Honey Trees (you will have 18 game hours to encounter):',tree_menu,0,1,[])
		ret = tree_array[sub_sel][1](*tree_array[sub_sel][2])

	return

def honey_tree_hack(p,mon,e):
	for i, t in enumerate(p,1):
		t.timer = 1080
		t.encounter_slot = e[0]
		t.encounter_tableindex = e[1]
		t.encounter_group = e[2]
		t.shakes = 1

	print("All Honey Trees loaded with " + mon + "; you have 18 game hours to encounter.\n")

	return

def box_pokemon(p,q):
	a, b, c, d = range(4)
	pk = pokemon_data_decrypt(p,30,1)

	pk_sel = -1
	while pk_sel != 0:
		poke_array = [
			(
				'Return',
				nop,
				[]
			)
		]

		for mon in range(30):
			if p[mon].header.personality == 0:
				poke_array.append(
					(
						"BLANK",
						nop,
						[]
					)
				)
				continue

			poke_array.append(
				(
					'{0:11}  {1:11}  OT ID: {2:5}  Exp: {3:7}  Friendship: {4:3}'.format(
						read_string(pk[mon][c].contents.nickname),
						national_dex[pk[mon][a].contents.species_id],
						pk[mon][a].contents.ot_id,
						pk[mon][a].contents.exp,
						pk[mon][a].contents.friendship,
					),
					edit_pokemon,
					[
						pk[mon],
					]
				)
			)

		poke_array.append(
			(
				"Edit Box Name: " + read_string(q),
				edit_string,
				[
					'Box Name',
					q,
					20
				]
			)
		)

		poke_menu = [x[0] for x in poke_array]
		pk_sel = menu('Box Pokémon Menu: ' + read_string(q),poke_menu,0,1,[])
		ret = poke_array[pk_sel][1](*poke_array[pk_sel][2])

	pokemon_data_encrypt(p,30,1)

	return

def box_mon_list(p):
	a, b, c, d = range(4)
	pk = pokemon_data_decrypt(p,30,1)
	poke_array = []

	for mon in range(30):
		if p[mon].header.personality == 0:
			poke_array.append("BLANK")
			continue

		poke_array.append(
			'{0:11}  {1:11}'.format(
				read_string(pk[mon][c].contents.nickname),
				national_dex[pk[mon][a].contents.species_id],
			)
		)

	pokemon_data_encrypt(p,30,1)

	return poke_array

# this function was AI generated because I was lazy, however, human cleanup, because, well it too verbose
def box_mon_swap_prompt():
	B_LOWER_LIMIT = 1
	B_UPPER_LIMIT = 18
	P_LOWER_LIMIT = 1
	P_UPPER_LIMIT = 30
	
	b1, b2 = None, None
	p1, p2 = None, None
	x = 0

	b_pattern = re.compile(r"^b(\d*),(\d*)$")
	p_pattern = re.compile(r"^p(\d+),(\d+)$")

	while True:
		user_input = input("Enter command: ").strip().lower()

		if user_input == 'x' or user_input == '0':
			x = 1
			break

		p_match = p_pattern.match(user_input)
		if p_match:
			p1_str, p2_str = p_match.groups()
			p1_val, p2_val = int(p1_str), int(p2_str)

			if (P_LOWER_LIMIT <= p1_val <= P_UPPER_LIMIT and P_LOWER_LIMIT <= p2_val <= P_UPPER_LIMIT):
				p1, p2 = p1_val, p2_val
				break
			else:
				print(f"\n'p' values must be between {P_LOWER_LIMIT} and {P_UPPER_LIMIT}.\n")
				continue

		b_match = b_pattern.match(user_input)
		if b_match:
			b1_str, b2_str = b_match.groups()
			
			if not b1_str and not b2_str:
				print("\nAt least one value must be provided for 'b'.\n")
				continue

			valid_update = True
			temp_b1, temp_b2 = b1, b2

			if b1_str:
				b1_val = int(b1_str)
				if not (B_LOWER_LIMIT <= b1_val <= B_UPPER_LIMIT):
					print(f"\nb values must be between {B_LOWER_LIMIT} and {B_UPPER_LIMIT}.\n")
					valid_update = False
				else:
					temp_b1 = b1_val
			
			if b2_str:
				b2_val = int(b2_str)
				if not (B_LOWER_LIMIT <= b2_val <= B_UPPER_LIMIT):
					print(f"\nb values must be between {B_LOWER_LIMIT} and {B_UPPER_LIMIT}.\n")
					valid_update = False
				else:
					temp_b2 = b2_val
			
			if valid_update:
				b1, b2 = temp_b1, temp_b2
				break
			
			continue

		print(f"\nInvalid input format, usage 'b2,3', 'b,4', 'p5,6', or 'x'.\n")

	return (b1,b2,p1,p2,x)

def box_mon_swap(p):
	box1 = 0
	box2 = 1
	done = 0

	while done == 0:
		print('Swap Pokémon')
		print()
		print(
			'{:2}. {:24}   {:2}. {:24}'.format(
				box1+1,
				read_string(p.box_names[box1].name),
				box2+1,
				read_string(p.box_names[box2].name),
			)
		)
		print()

		box1list = box_mon_list(p.box[box1].pokemon)
		box2list = box_mon_list(p.box[box2].pokemon)

		for i in range(30):
			print(
				'{:2}. {:24}   {:2}. {:24}'.format(
					i+1,
					box1list[i],
					i+1,
					box2list[i],
				)
			)

		print(
'''
Commands:

b[1-18],[1-18] to choose boxes
b[1-18],       to choose first box only
b,[1-18]       to choose second box only
p[1-30],[1-30] to swap box1,p1 with box2,p2
x or 0         to exit
'''
		)

		b1, b2, p1, p2, done = box_mon_swap_prompt()

		if b1 != None: box1 = b1 - 1
		if b2 != None: box2 = b2 - 1

		if p1 != None and p2 != None:
			p1 -= 1
			p2 -= 1
			buf_size = sizeof(p.box[box1].pokemon[p1])
			buf = (c_char * buf_size)()
			memmove(buf, byref(p.box[box1].pokemon[p1]), buf_size)
			memmove(byref(p.box[box1].pokemon[p1]), byref(p.box[box2].pokemon[p2]), buf_size)
			memmove(byref(p.box[box2].pokemon[p2]), buf, buf_size)

		print()

	return

def box_menu(p):
	sub_sel = -1
	while sub_sel != 0:
		box_array = [
			(
				'Return',
				nop,
				[]
			),
		]

		for i, j in enumerate(p.box_names):
			box_array.append(
				(
					read_string(j.name),
					box_pokemon,
					[
						p.box[i].pokemon,
						j.name
					]
				)
			)

		box_array.append(
			(
				"Swap Pokémon",
				box_mon_swap,
				[
					p
				]
			)
		)

		box_menu = [x[0] for x in box_array]
		sub_sel = menu('Select box to edit:',box_menu,0,1,[])
		ret = box_array[sub_sel][1](*box_array[sub_sel][2])

	return

def dump_signature(p,filename):
	w, h = 192, 64
	matrix = [[0 for j in range(w)] for i in range(h)] 

	for i in range(8):
		for j in range(24):
			for k in range(8):
				byte = p.row[i].col[j].byte[k]
				for bit in range(8):
					#matrix[i*8 + k][j*8 + bit] = 0 if byte & 1 else 1
					matrix[i*8 + k][j*8 + bit] = 1 - (byte & 1)
					byte >>= 1

	image = Image.new('1', (w, h))
	pixel_data = [pixel for row in matrix for pixel in row]	
	image.putdata(pixel_data)
	image.save(filename)

def read_signature(filename,p):
	try:
		image = Image.open(filename).convert('1')
		image = image.resize((192, 64), Image.Resampling.NEAREST)
		w, h = image.size

		pixel_list = list(image.getdata())
		matrix = [pixel_list[i * w:(i + 1) * w] for i in range(h)]

		for i in range(8):
			for j in range(24):
				for k in range(8):
					byte = 0
					for bit in range(7,-1,-1):
						byte |= (0 if matrix[i*8 + k][j*8 + bit] else 1 << bit)
					p.row[i].col[j].byte[k] = byte

	except FileNotFoundError:
		print(f"\nError: '{filename}' was not found.\n")
		return None
	except Exception as e:
		print(f"\nAn error occurred: {e}\n")
		return None

	return

def all_sinnoh_seen(p):
	seen=int.from_bytes(p.seen, byteorder='little')

	for national_id in range(1, 491):
		if national_dex[national_id] in sinnoh_dex_id:
			seen |= (1 << (national_id-1))

	tmp = seen.to_bytes(sizeof(p.seen), byteorder='little')
	c_ubyte_array = c_ubyte * sizeof(p.seen)
	p.seen = c_ubyte_array.from_buffer_copy(tmp)

	return

def full_dex(p):
	caught=int.from_bytes(p.caught, byteorder='little')
	seen=int.from_bytes(p.seen, byteorder='little')

	for national_id in range(490):
		seen |= (1 << (national_id))
		caught |= (1 << (national_id))

	tmp = seen.to_bytes(sizeof(p.seen), byteorder='little')
	c_ubyte_array = c_ubyte * sizeof(p.seen)
	p.seen = c_ubyte_array.from_buffer_copy(tmp)

	tmp = caught.to_bytes(sizeof(p.caught), byteorder='little')
	c_ubyte_array = c_ubyte * sizeof(p.caught)
	p.caught = c_ubyte_array.from_buffer_copy(tmp)

	return

def read_pokedex(p,order,national,missing):
	caught=int.from_bytes(p.caught, byteorder='little')
	seen=int.from_bytes(p.seen, byteorder='little')
	first_seen_gender=int.from_bytes(p.first_seen_gender, byteorder='little')
	second_seen_gender=int.from_bytes(p.second_seen_gender, byteorder='little')
	genders = ['Male Only','Male First, Female Second','Female First, Male Second','Female Only']
	caught_c = seen_c = total = 0
	dex = []

	for national_id in range(1, 491):
		sinnoh_id = 0
		if national_dex[national_id] in sinnoh_dex_id: sinnoh_id = sinnoh_dex_id[national_dex[national_id]]
		gender = ''
		if seen & 1:
			i = (first_seen_gender & 1) ^ (second_seen_gender & 1) + 1
			gender = genders[i]
		if national or (sinnoh_id and not national):
			dex.append((
				national_id,
				national_dex[national_id],
				sinnoh_id,
				pokeball if caught & 1 else ' ',
				pokeseen if seen & 1 else ' ',
				gender
			))
			total += 1		
			if caught & 1: caught_c += 1
			if seen & 1: seen_c += 1
		caught >>= 1
		seen >>= 1
		first_seen_gender >>= 1
		second_seen_gender >>= 1

	if missing == 1: dex = (t for t in dex if t[3] != pokeball)
	if missing == 2: dex = (t for t in dex if t[4] != pokeseen)

	if order == 'id':
		if national:
			sorter = lambda x: (x[0], x[1], x[2], x[3], x[4], x[5])
		else:
			sorter = lambda x: (x[2], x[1], x[0], x[3], x[4], x[5])
	else:
		sorter = lambda x: (x[1], x[0], x[2], x[3], x[4], x[5])

	sorted_dex = sorted(dex, key=sorter)

	if not sorted_dex:
		if missing == 1: print("All Caught!")
		if missing == 2: print("All Seen!")
		print()
		return

	dex_lines = []
	for i in sorted_dex:
		dex_lines.append(
			'{0:-3} {2:-3} {1:12} {3:1} {4:1}'.format(*i)
		)

	sep = '  |  '
	term_cols = os.get_terminal_size().columns
	line_length = len(max(dex_lines,key=len))
	cols = term_cols // (line_length + len(sep))
	if len(dex_lines) < 20: cols = 1
	lines = math.ceil(len(dex_lines) / cols)
	header = '{0:3} {1:3} {2:12}'.format('Nat','Sin','Name')
	header += ' ' * (line_length - len(header))

	for i in range(cols):
		print(header, end='')
		if i != cols - 1: print(sep, end='')

	print()

	for i in range(cols):
		print('-' * len(header), end='')
		if i != cols - 1: print(sep.replace(' ','-').replace('|','+'), end='')

	print()

	for i in range(lines):
		for j in range(cols):
			if i + j*lines < len(dex_lines): print(dex_lines[i + j*lines], end='')
			if j != cols - 1: print(sep, end='')
		print()

	print()
	print(
		'Total: {}  Seen: {}  Unseen: {}  Obtained: {}  Unobtained: {}'.format(total,seen_c,total-seen_c,caught_c,total-caught_c)
	)
	print()
		
	return


### main

if len(sys.argv) != 2:
	print("\nUsage: " + sys.argv[0] + " [.sav filename]\n")
	sys.exit(1)

try:
	sav = bytearray(open(sys.argv[1],'rb').read())
except Exception as err:
	print(f"Unexpected {err=}, {type(err)=}")
	raise

savedata = save_data.from_buffer(sav,0)

if savedata.general0.footer.chksum != 0xFFFF:
	assert savedata.general0.footer.chksum == crc_ccitt_16(bytes(savedata.general0.data) + bytes(savedata.general0.padding))
if savedata.general1.footer.chksum != 0xFFFF:
	assert savedata.general1.footer.chksum == crc_ccitt_16(bytes(savedata.general1.data) + bytes(savedata.general1.padding))
if savedata.storage0.footer.chksum != 0xFFFF:
	assert savedata.storage0.footer.chksum == crc_ccitt_16(bytes(savedata.storage0.data) + bytes(savedata.storage0.padding))
if savedata.storage1.footer.chksum != 0xFFFF:
	assert savedata.storage1.footer.chksum == crc_ccitt_16(bytes(savedata.storage1.data) + bytes(savedata.storage1.padding))

if savedata.general0.footer.saves > savedata.general1.footer.saves:
	g = pointer(savedata.general0)
else:
	g = pointer(savedata.general1)

if savedata.general0.footer.saves == 0xFFFFFFFF:
	g = pointer(savedata.general1)
if savedata.general1.footer.saves == 0xFFFFFFFF:
	g = pointer(savedata.general0)

try:
	g
except Exception as err:
	print(f"Unexpected {err=}, {type(err)=}")
	raise

if g.contents.footer.link == savedata.storage0.footer.link:
	s = pointer(savedata.storage0)
if g.contents.footer.link == savedata.storage1.footer.link:
	s = pointer(savedata.storage1)

try:
	s
except Exception as err:
	print(f"Unexpected {err=}, {type(err)=}")
	raise

# redundtant
assert g.contents.footer.chksum == crc_ccitt_16(bytes(g.contents.data) + bytes(g.contents.padding))
assert s.contents.footer.chksum == crc_ccitt_16(bytes(s.contents.data) + bytes(s.contents.padding))

print("\nPokémon Gen IV (Platinum only for now) Editor v" + version)
print(
"""
Tested Roms:

ab828b0d13f09469a71460a34d0de51b  Pokemon - Platinum Version (USA) (Rev 1).nds
"""
)
print("USE AT YOUR OWN PERIL!!!\n")
print("Let's go shopping!\n")

sel = -1
while sel != 0:
	print('Play Time: {0:02d}:{1:02d}:{2:02d}'.format(
		g.contents.data.hours_played,
		g.contents.data.minutes_played,
		g.contents.data.seconds_played,
	))
	print('RTC Time: {0:d}.{1:02d}.{2:02d} {4:d}:{5:02d}:{6:02d}'.format(
		g.contents.data.rtc_year,
		g.contents.data.rtc_month,
		g.contents.data.rtc_date,
		g.contents.data.rtc_weekday,
		g.contents.data.rtc_hour,
		g.contents.data.rtc_minute,
		g.contents.data.rtc_second,
	))
	from datetime import datetime
	print("[Initial] Save Timestamp:",datetime.fromtimestamp(g.contents.data.save_timestamp+946684800).strftime("%A, %B %d, %Y %I:%M:%S"))
	print("HoF Timestamp:",datetime.fromtimestamp(g.contents.data.hof_timestamp+946684800).strftime("%A, %B %d, %Y %I:%M:%S"))
	print()
	menu_array = [
		(
			'Exit (and [over]write "' + outputfilename + '")',
			writeout,
			[outputfilename,savedata,g,s]
		),
		(
			'Items',
			items,
			[g.contents.data.items, 'ITEMS', ITEMS_SLOTS]
		),
		(
			'Medicine',
			items,
			[g.contents.data.med_items, 'MEDICINE', MEDICAL_SLOTS]
		),
		(
			'Poké Balls',
			items,
			[g.contents.data.balls_items, 'BALLS', BALLS_SLOTS]
		),
		(
			'TM & HM',
			items,
			[g.contents.data.tmhm_items, 'TMHMS', TMHMS_SLOTS]
		),
		(
			'Berries',
			items,
			[g.contents.data.berry_items, 'BERRIES', BERRY_SLOTS]
		),
		(
			'Mail',
			items,
			[g.contents.data.mail_items, 'MAIL', MAIL_SLOTS]
		),
		(
			'Battle Items',
			items,
			[g.contents.data.battle_items, 'BATTLE_ITEMS', BATTLE_ITEMS_SLOTS]
		),
		(
			'Key Items',
			items,
			[g.contents.data.key_items, 'KEY_ITEMS', KEY_ITEMS_SLOTS]
		),
		(
			'Sort Items',
			sort_items,
			[g.contents.data.items, 'ITEMS', ITEMS_SLOTS]
		),
		(
			'Sort Medicine',
			sort_items,
			[g.contents.data.med_items, 'MEDICINE', MEDICAL_SLOTS]
		),
		(
			'Sort Poké Balls',
			sort_items,
			[g.contents.data.balls_items, 'BALLS', BALLS_SLOTS]
		),
		(
			'Sort Mail',
			sort_items,
			[g.contents.data.mail_items, 'MAIL', MAIL_SLOTS]
		),
		(
			'Sort Battle Items',
			sort_items,
			[g.contents.data.battle_items, 'BATTLE_ITEMS', BATTLE_ITEMS_SLOTS]
		),
		(
			'Sort Key Items',
			sort_items,
			[g.contents.data.key_items, 'KEY_ITEMS', KEY_ITEMS_SLOTS]
		),
		(
			'Sort All Items',
			sort_all_items,
			[
				[
					[g.contents.data.items,'ITEMS',ITEMS_SLOTS],
					[g.contents.data.med_items,'MEDICINE',MEDICAL_SLOTS],
					[g.contents.data.balls_items,'BALLS',BALLS_SLOTS],
					[g.contents.data.mail_items,'MAIL',MAIL_SLOTS],
					[g.contents.data.battle_items,'BATTLE_ITEMS',BATTLE_ITEMS_SLOTS],
					[g.contents.data.key_items,'KEY_ITEMS',KEY_ITEMS_SLOTS],
				],
			],
		),
		(
			'Pokémon',
			pokemon_menu,
			[g.contents.data.pokemon, g.contents.data.num_mon]
		),
		(
			'Cold Storage [Boxes]',
			box_menu,
			[s.contents.data]
		),
		(
			'Pokédex: Sinnoh Id',
			read_pokedex,
			[g.contents.data.pokedex,'id',0,0]
		),
		(
			'Pokédex: Sinnoh Name',
			read_pokedex,
			[g.contents.data.pokedex,'name',0,0]
		),
		(
			'Pokédex: Sinnoh Id Unobtained',
			read_pokedex,
			[g.contents.data.pokedex,'id',0,1]
		),
		(
			'Pokédex: Sinnoh Name Unobtained',
			read_pokedex,
			[g.contents.data.pokedex,'name',0,1]
		),
		(
			'Pokédex: Sinnoh Id Unseen',
			read_pokedex,
			[g.contents.data.pokedex,'id',0,2]
		),
		(
			'Pokédex: Sinnoh Name Unseen',
			read_pokedex,
			[g.contents.data.pokedex,'name',0,2]
		),
		(
			'Pokédex: Sinnoh All Seen (WARNING: Cannot be unseen!)',
			all_sinnoh_seen,
			[g.contents.data.pokedex]
		),
		(
			'Pokédex: National Id',
			read_pokedex,
			[g.contents.data.pokedex,'id',1,0]
		),
		(
			'Pokédex: National Name',
			read_pokedex,
			[g.contents.data.pokedex,'name',1,0]
		),
		(
			'Pokédex: National Id Unobtained',
			read_pokedex,
			[g.contents.data.pokedex,'id',1,1]
		),
		(
			'Pokédex: National Name Unobtained',
			read_pokedex,
			[g.contents.data.pokedex,'name',1,1]
		),
		(
			'Pokédex: National All Caught (WARNING: Cannot be undone!)',
			full_dex,
			[g.contents.data.pokedex]
		),
		(
			'Trainer ID: ' + str(g.contents.data.trainer_id),
			edit_number,
			['Trainer ID', g.contents.data, 'trainer_id', 65535]
		),
		(
			'Secret ID: ' + str(g.contents.data.secret_id),
			edit_number,
			['Secret ID', g.contents.data, 'secret_id', 65535]
		),
		(
			'Trainer Name: ' + read_string(g.contents.data.trainer_name, 8),
			edit_string,
			['Trainer Name', g.contents.data.trainer_name, 8]
		),
		(
			'Gender: ' + ('Boy' if not g.contents.data.gender else 'Girl'),
			toggle_number,
			[g.contents.data, 'gender']
		),
		(
			'Money: ' + str(g.contents.data.money),
			edit_number,
			['Money', g.contents.data, 'money', 999999]
		),
		(
			'Coins: ' + str(g.contents.data.coins),
			edit_number,
			['Coins', g.contents.data, 'coins', 65535]
		),
		(
			'Honey Trees',
			honey_tree_menu,
			[g.contents.data.honey_trees]
		),
		(
			'Lotto Number: ' + str(g.contents.data.lotto_number),
			edit_number,
			['Lotto Number', g.contents.data, 'lotto_number', 65535]
		),
		(
			'Mystery Gift: ' + ('unlocked' if g.contents.data.myster_gift_unlocked else 'locked'),
			toggle_number,
			[g.contents.data, 'myster_gift_unlocked']
		),
		(
			'Clock Change Penality: ' + str(g.contents.data.clock_change_penality),
			edit_number,
			['Clock Change Penality', g.contents.data, 'clock_change_penality', 2**32-1]
		),
		(
			'Rival Name: ' + read_string(g.contents.data.rival_name, 8),
			edit_string,
			['Rival Name', g.contents.data.rival_name, 8]
		),
		(
			'Save Signature to "sig.png"',
			dump_signature,
			[g.contents.data.signature,"sig.png"]
		),
		(
			'Read Signature from "sig.png"',
			read_signature,
			["sig.png",g.contents.data.signature]
		),
		(
			'[Over]write "' + outputfilename + '" and continue editing',
			writeout,
			[outputfilename,savedata,g,s]
		),
		(
			'Abort! (all changes since last write lost)',
			sys.exit,
			[0]
		),
	]

	main_menu = [x[0] for x in menu_array]
	sel = menu('Main Menu',main_menu,0,1,[])
	ret = menu_array[sel][1](*menu_array[sel][2])

sys.exit(0)


from ctypes import *
from offsets import *
from constants import *

class footer(Structure):
	_pack_ = 1
	_fields_ = [
		('link', c_uint32),
		('saves', c_uint32),
		('blocksize', c_uint32),
		('K', c_uint32),
		('id', c_uint16),
		('chksum', c_uint16),
	]

class nds_char(Structure):
	_pack_ = 1
	_fields_ = [
		('char', c_uint16),
	]

class badges(Structure):
	_pack_ = 1
	_fields_ = [
		('coal', c_ubyte, 1),
		('forest', c_ubyte, 1),
		('cobble', c_ubyte, 1),
		('fen', c_ubyte, 1),
		('relic', c_ubyte, 1),
		('mine', c_ubyte, 1),
		('icicle', c_ubyte, 1),
		('beacon', c_ubyte, 1),
	]

class pokemon_header_bits(Structure):
	_pack_ = 1
	_fields_ = [
		('skip_chksum', c_uint16, 2),
		('bad_egg', c_uint16, 1),
		('unused', c_uint16, 13),
	]

class pokemon_header(Structure):
	_pack_ = 1
	_fields_ = [
		('personality', c_uint32),
		('bits', pokemon_header_bits),
		('chksum', c_uint16),
	]

class block_A(Structure):
	_pack_ = 1
	_fields_ = [
		('species_id', c_uint16),
		('held_item', c_uint16),
		('ot_id', c_uint16),
		('ot_secret_id', c_uint16),
		('exp', c_uint32),
		('friendship', c_uint8),
		('ability', c_uint8),
		('markings', c_uint8),
		('lang_of_origin', c_uint8),
		('hp_ev', c_uint8),
		('attack_ev', c_uint8),
		('def_ev', c_uint8),
		('speed_ev', c_uint8),
		('sp_atk_ev', c_uint8),
		('sp_def_ev', c_uint8),
		('cool', c_uint8),
		('beauty', c_uint8),
		('cute', c_uint8),
		('smart', c_uint8),
		('tough', c_uint8),
		('sheen', c_uint8),
		('ribbons', 4 * c_uint8),
	]

class block_B(Structure):
	_pack_ = 1
	_fields_ = [
		('data', 32 * c_uint8),
	]

class block_C(Structure):
	_pack_ = 1
	_fields_ = [
		('nickname', 11 * nds_char),
		('data', 10 * c_uint8),
	]

class block_D(Structure):
	_pack_ = 1
	_fields_ = [
		('ot_name', 8 * nds_char),
		('data', 16 * c_uint8),
	]

class pokemon_block(Structure):
	_pack_ = 1
	_fields_ = [
		('block', 16 * c_uint16),
	]

class pokemon_blocks(Union):
	_pack_ = 1
	_fields_ = [
		('blocks', 4 * pokemon_block),
		('bitstream', 64 * c_uint16),
	]

class pokemon(Structure):
	_pack_ = 1
	_fields_ = [
		('header', pokemon_header),
		('data', pokemon_blocks),
		('battle_stats', 50 * c_uint16),
	]

class box_pokemon(Structure):
	_pack_ = 1
	_fields_ = [
		('header', pokemon_header),
		('data', pokemon_blocks),
	]

class item(Structure):
	_pack_ = 1
	_fields_ = [
		('id', c_uint16),
		('q', c_uint16),
	]

class honey_tree(Structure):
	_pack_ = 1
	_fields_ = [
		('timer', c_int32),
		('encounter_slot', c_uint8),
		('encounter_tableindex', c_uint8),
		('encounter_group', c_uint8),
		('shakes', c_uint8),
	]

class pokedex(Structure):
	_pack_ = 1
	_fields_ = [
		('caught', 0x40 * c_uint8),
		('seen', 0x40 * c_uint8),
		('first_seen_gender', 0x40 * c_uint8),
		('second_seen_gender', 0x40 * c_uint8),
	]

class signature_block(Structure):
	_pack_ = 1
	_fields_ = [
		('byte', 8 * c_uint8),
	]

class signature_row(Structure):
	_pack_ = 1
	_fields_ = [
		('col', 24 * signature_block),
	]

class signature(Structure):
	_pack_ = 1
	_fields_ = [
		('row', 8 * signature_row),
	]

class general_block_data(Structure):
	_pack_ = 1
	_fields_ = [
		('rtc_offset', c_int64),
		('mac_address', 6 * c_uint8),
		('ds_profile_birth_month', c_uint8),
		('ds_profile_birth_day', c_uint8),
		('canary', 4 * c_uint8),
		('rtc_year', c_uint32),
		('rtc_month', c_uint32),
		('rtc_date', c_uint32),
		('rtc_weekday', c_uint32),
		('rtc_hour', c_uint32),
		('rtc_minute', c_uint32),
		('rtc_second', c_uint32),
		('day', c_uint32),
		('save_timestamp', c_int64),
		('hof_timestamp', c_int64),
		('clock_change_penality', c_uint32),
		('myster_gift_unlocked', c_uint8),
		('padding_0', c_uint8),
		('network_profile_id', 4 * c_uint8),
		('padding_1', 26 * c_uint8),
		('trainer_name', 8 * nds_char),
		('trainer_id', c_uint16),
		('secret_id', c_uint16),
		('money', c_uint32),
		('gender', c_uint8),
		('locale', c_uint8),
		('badges', badges),
		('avatar', c_uint8),
		('padding_2', 4 * c_uint8),
		('coins', c_uint16),
		('hours_played', c_uint16),
		('minutes_played', c_uint8),
		('seconds_played', c_uint8),
		('padding_3', 14 * c_uint8),
		('num_mon', c_uint8),
		('padding_4', 3 * c_uint8),
		('pokemon', 6 * pokemon),
		('padding_5', 8 * c_uint8),
		('items', ITEMS_SLOTS * item),
		('key_items', KEY_ITEMS_SLOTS * item),
		('tmhm_items', TMHMS_SLOTS * item),
		('mail_items', MAIL_SLOTS * item),
		('med_items', MEDICAL_SLOTS * item),
		('berry_items', BERRY_SLOTS * item),
		('balls_items', BALLS_SLOTS * item),
		('battle_items', BATTLE_ITEMS_SLOTS * item),
		('padding_7', (0xE24 - 0xDA0) * c_uint8),
		('lotto_number', c_uint16),
		('padding_8', (0x1141 - 0xE26) * c_uint8),
		('lotto_obtained', c_uint8),
		('padding_9', (0x132C - 0x1142) * c_uint8),
		('pokedex', pokedex),
		('padding_10', (0x27E8 - 0x142C) * c_uint8),
		('rival_name', 8 * nds_char),
		('padding_11', (0x5BA8 - 0x27F8) * c_uint8),
		('signature', signature),
		('padding_12', (0x7F38 - 0x61a8) * c_uint8),
		('honey_trees', 21 * honey_tree),
	]


# PKHeX.Core/Saves/SAV4Pt.cs has address at 0x1328
# pokedex 0x1328 (8*0x40) (0x1330)
# for structure: ./PKHeX.Core/Saves/Substructures/PokeDex/Zukan4.cs

class general_block(Structure):
	_pack_ = 1
	_fields_ = [
		('data', general_block_data),
		('padding', c_uint8 * (GENERAL_FOOTER - sizeof(general_block_data))),
		('footer', footer),
	]

class box_names(Structure):
	_pack_ = 1
	_fields_ = [
		('name', 20 * nds_char),
	]

class box(Structure):
	_pack_ = 1
	_fields_ = [
		('pokemon', 30 * box_pokemon),
	]

class storage_block_data(Structure):
	_pack_ = 1
	_fields_ = [
		('last_index', c_uint32),
		('box', 18 * box),
		('box_names', 18 * box_names),
		('box_wallpapers', 18 * c_uint8),
	]

class storage_block(Structure):
	_pack_ = 1
	_fields_ = [
		('data', storage_block_data),
		('padding', c_uint8 * (STORAGE_FOOTER - sizeof(storage_block_data))),
		('footer', footer),
	]

class save_data(Structure):
	_pack_ = 1
	_fields_ = [
		('general0', general_block),
		('storage0', storage_block),
		('padding0', c_uint8 * (BLOCK2 - sizeof(general_block) - sizeof(storage_block))),
		('general1', general_block),
		('storage1', storage_block),
		('padding1', c_uint8 * (BLOCK2 - sizeof(general_block) - sizeof(storage_block))),
	]

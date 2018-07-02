import libtcodpy as tcod
import shelve

from initialize_fov import initialize_fov
from Keymap import Keymap
from Object import Object
from pathlib import Path

# Actual size of the displayed screen
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

# Map size
MAP_WIDTH = 75
MAP_HEIGHT = 43

# Panel console height
PANEL_HEIGHT = 7

# GUI
BAR_WIDTH = 20
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

# FOV
FOV_ALGO = 0
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

LIMIT_FPS = 25

# Useful runtime constants
INVENTORY_WIDTH = 50
ABILITY_WIDTH = 50
INFORMATION_WIDTH = 50

LEVEL_UP_BASE = 200
LEVEL_UP_FACTOR = 150
LEVEL_UP_SCREEN_WIDTH = 40

CHARACTER_SCREEN_WIDTH = 30

# Parameters for dungeon generator
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 20

# Spells
HEAL_AMOUNT = 40
LIGHTNING_DAMAGE = 40
LIGHTNING_RANGE = 5
CONFUSE_NUM_TURNS = 10
CONFUSE_RANGE = 8
FIREBALL_RADIUS = 3
FIREBALL_DAMAGE = 25
HOLD_NUM_TURNS = 10
HOLD_RANGE = 8

# Consoles
con = tcod.console_new(MAP_WIDTH, MAP_HEIGHT)
targeting = tcod.console_new(MAP_WIDTH, MAP_HEIGHT)
panel = tcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)

# Runtime global variables
abilities = []
boner_dome = Object(0, 0, 'D', 'boner_dome', tcod.yellow)
dungeon_level = 1
dungeon_map = []
fov_map = tcod.map_new(MAP_WIDTH, MAP_HEIGHT)
fov_recompute = True
game_state = ''
game_messages = []
highlight_state = ''
inventory = []
key = tcod.Key()
keymap = Keymap()
look_mode = 'mouse'
mouse = tcod.Mouse()
new_x = None
new_y = None
objects = []
old_x = None
old_y = None
player = Object(0, 0, '@', 'player', tcod.white)
player_action = ''
selection_coordinates = (0, 0)
stairs_down = Object(0, 0, '>', 'stairs down', tcod.white)
stairs_up = Object(0, 0, '<', 'stairs up', tcod.white)

keycode_to_direction_tuple_map = {
	tcod.KEY_KP8: (0, -1),
	tcod.KEY_UP: (0, -1),
	tcod.KEY_KP9: (1, -1),
	tcod.KEY_RIGHT: (1, 0),
	tcod.KEY_KP6: (1, 0),
	tcod.KEY_KP3: (1, 1),
	tcod.KEY_DOWN: (0, 1),
	tcod.KEY_KP2: (0, 1),
	tcod.KEY_KP1: (-1, 1),
	tcod.KEY_LEFT: (-1, 0),
	tcod.KEY_KP4: (-1, 0),
	tcod.KEY_KP7: (-1, -1),
	tcod.KEY_KP5: (0, 0)
}


def init():
	font_path = 'assets/fonts/arial10x10.png'
	font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
	tcod.console_set_custom_font(font_path, font_flags)

	window_title = "Roguelike"
	fullscreen = False
	tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, window_title, fullscreen)

	tcod.sys_set_fps(LIMIT_FPS)


def init_new_game():
	global dungeon_map, game_messages, inventory, objects, player_action, keymap
	global highlight_state
	dungeon_map = []
	game_messages = []
	highlight_state = 'play'
	inventory = []
	objects = []
	player_action = ''

	# Deletes all of the existing level states
	p = Path('.')
	folder = p / 'save'
	for file in folder.iterdir():
		file.unlink()


def is_blocked(x, y):
	# first test the map tile
	if dungeon_map[x][y].blocked:
		return True

	for obj in objects:
		if obj.blocks and obj.x == x and obj.y == y:
			return True

	return False


def get_equipped_in_slot(slot):
	for obj in inventory:
		if obj.equipment and obj.equipment.slot == slot and obj.equipment.is_equipped:
			return obj.equipment
	return None


def from_dungeon_level(table):
	# returns a value that depends on level. the table specifies what occurs at any given level
	for (value, level) in reversed(table):
		if dungeon_level >= level:
			return value
	return 0


def get_all_equipped(obj):
	if obj == player:
		equipped_list = []
		for item in inventory:
			if item.equipment and item.equipment.is_equipped:
				equipped_list.append(item.equipment)
		return equipped_list
	else:
		return []


def save_game():
	file = shelve.open('savegame', 'n')
	file['map'] = dungeon_map
	file['objects'] = objects
	file['player_index'] = objects.index(player)
	file['inventory'] = inventory
	file['game_messages'] = game_messages
	file['game_state'] = game_state
	try:
		file['stairs_down_index'] = objects.index(stairs_down)
	except ValueError:
		file['stairs_down_index'] = None
	try:
		file['stairs_up_index'] = objects.index(stairs_up)
	except ValueError:
		file['stairs_up_index'] = None
	file['dungeon_level'] = dungeon_level
	file.close()


def save_level_state():
	file = shelve.open('save/level' + str(dungeon_level), 'n')
	file['map'] = dungeon_map
	file['objects'] = objects
	file['player_index'] = objects.index(player)
	try:
		file['stairs_down_index'] = objects.index(stairs_down)
	except ValueError:
		file['stairs_down_index'] = None
	try:
		file['stairs_up_index'] = objects.index(stairs_up)
	except ValueError:
		file['stairs_up_index'] = None
	file.close()


def load_game():
	global dungeon_map, objects, player, inventory, game_messages, game_state, stairs_down, stairs_up, dungeon_level
	global map_dict
	file = shelve.open('savegame', 'r')
	dungeon_map = file['map']
	objects = file['objects']
	player = objects[file['player_index']]
	inventory = file['inventory']
	game_messages = file['game_messages']
	game_state = file['game_state']
	if file['stairs_down_index'] is not None:
		stairs_down = objects[file['stairs_down_index']]
	if file['stairs_up_index'] is not None:
		stairs_up = objects[file['stairs_up_index']]
	dungeon_level = file['dungeon_level']
	file.close()

	initialize_fov()


def load_level_state():
	global dungeon_map, objects, player, inventory, game_messages, game_state, stairs_down, stairs_up, dungeon_level
	global map_dict
	file = shelve.open('save/level' + str(dungeon_level), 'r')
	dungeon_map = file['map']
	objects = file['objects']
	player = objects[file['player_index']]
	if file['stairs_down_index'] is not None:
		stairs_down = objects[file['stairs_down_index']]
	if file['stairs_up_index'] is not None:
		stairs_up = objects[file['stairs_up_index']]
	file.close()

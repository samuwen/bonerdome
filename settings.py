import libtcodpy as tcod
import shelve

from initialize_fov import initialize_fov
from Object import Object

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

font_path = 'assets/fonts/arial10x10.png'
font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD

con = tcod.console_new(MAP_WIDTH, MAP_HEIGHT)
panel = tcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)

boner_dome = Object(0, 0, 'D', 'boner_dome', tcod.yellow)
dungeon_level = 1
dungeon_map = []
fov_map = tcod.map_new(MAP_WIDTH, MAP_HEIGHT)
fov_recompute = True
game_state = ''
game_messages = []
inventory = []
key = tcod.Key()
mouse = tcod.Mouse()
objects = []
player = Object(0, 0, '@', 'player', tcod.white)
player_action = ''
stairs_down = Object(0, 0, '>', 'stairs down', tcod.white)
stairs_up = Object(0, 0, '<', 'stairs up', tcod.white)


def init():
	tcod.console_set_custom_font(font_path, font_flags)

	window_title = "Roguelike"
	fullscreen = False
	tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, window_title, fullscreen)

	tcod.sys_set_fps(LIMIT_FPS)


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


def closest_monster(max_range):
	# find closest enemy, up to a maximum range, and in the player's FOV
	closest_enemy = None
	closest_dist = max_range + 1  # start with slightly more than maximum range

	for obj in objects:
		if obj.fighter and not obj == player and tcod.map_is_in_fov(fov_map, obj.x, obj.y):
			dist = player.distance_to(obj)
			if dist < closest_dist:  # it's closer, so remember it
				closest_enemy = obj
				closest_dist = dist
	return closest_enemy


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


def get_names_under_mouse():
	# return a string with the names of all objects under the mouse
	(x, y) = (mouse.cx, mouse.cy)

	# create a list of all visible objects at the mouse position
	names = [obj.name for obj in objects if obj.x == x and obj.y == y and
		tcod.map_is_in_fov(fov_map, obj.x, obj.y)]
	names = ', '.join(names)
	return names.capitalize()


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


def load_game():
	global dungeon_map, objects, player, inventory, game_messages, game_state, stairs_down, stairs_up, dungeon_level
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

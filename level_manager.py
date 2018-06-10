import libtcodpy as tcod
import settings

from initialize_fov import initialize_fov
from map_handler import make_map
from message import message
from utilities import print_debug


def next_level():
	# advance to the next level
	message('You go down a floor.', tcod.light_violet)
	settings.save_level_state()
	settings.dungeon_level += 1
	try:
		settings.load_level_state()
	except:
		print_debug("map not found. making new map")
		make_map()
		settings.save_level_state()
	initialize_fov()


def previous_level():
	# advance to the previous level
	message("You go up a floor.", tcod.light_violet)
	settings.save_level_state()
	settings.dungeon_level -= 1
	settings.load_level_state()
	# settings.dungeon_map = settings.map_dict['d_map' + str(settings.dungeon_level)]
	initialize_fov()

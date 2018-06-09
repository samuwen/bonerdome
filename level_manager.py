import libtcodpy as tcod
import settings

from initialize_fov import initialize_fov
from map_handler import make_map
from message import message


def next_level():
	# advance to the next level
	message('You go down a floor.', tcod.light_violet)
	settings.dungeon_level += 1
	make_map()
	initialize_fov()


def previous_level():
	# advance to the previous level
	message("You go up a floor.", tcod.light_violet)
	settings.dungeon_level -= 1
	# replace this with an accessor for the previous map
	make_map()
	initialize_fov()

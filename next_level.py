import libtcodpy as tcod
import settings

from initialize_fov import initialize_fov
from map_handler import make_map
from message import message


def next_level():
	# advance to the next level
	message('You advance to the next level.', tcod.light_violet)
	settings.dungeon_level += 1
	make_map()
	initialize_fov()

import libtcodpy as tcod
import settings


def initialize_fov():
	settings.fov_recompute = True
	for y in range(settings.MAP_HEIGHT):
		for x in range(settings.MAP_WIDTH):
			tcod.map_set_properties(settings.fov_map, x, y, not settings.dungeon_map[x][y].block_sight,
				not settings.dungeon_map[x][y].blocked)

	tcod.console_clear(settings.con)

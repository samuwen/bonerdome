import libtcodpy as tcod
import settings

from render import render_all


def target_tile(max_range=None):
	# return the position of a tile that has been left-clicked within the player's FOV
	while True:
		# render the screen. This erases the inventory and shows the names of objects under the mouse
		tcod.console_flush()
		tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, settings.key, settings.mouse)
		render_all()

		(x, y) = (settings.mouse.cx, settings.mouse.cy)

		if (settings.mouse.lbutton_pressed and tcod.map_is_in_fov(settings.fov_map, x, y) and
			(max_range is None or settings.player.distance(x, y) <= max_range)):
			return (x, y)

		if settings.mouse.rbutton_pressed or settings.key.vk == tcod.KEY_ESCAPE:
			return (None, None)  # right click or escape to cancel


def target_monster(max_range):
	# returns a clicked monster in FOV up to a specific range
	while True:
		(x, y) = target_tile(max_range)
		if x is None:  # player cancelled
			return None

		for obj in settings.objects:
			if obj.x == x and obj.y == y and obj.fighter and obj != settings.player:
				return obj

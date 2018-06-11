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
			if obj.x == x and obj.y == y and obj.combatant and obj != settings.player:
				return obj


def combatant_is_adjacent(x, y):
	target = None
	for obj in settings.objects:
		if obj.combatant and obj.x == x and obj.y == y:
			target = obj
			return target
	return None


def closest_monster(max_range):
	# find closest enemy, up to a maximum range, and in the player's FOV
	closest_enemy = None
	closest_dist = max_range + 1  # start with slightly more than maximum range

	for obj in settings.objects:
		if obj.combatant and not obj == settings.player and tcod.map_is_in_fov(settings.fov_map,
			obj.x, obj.y):
			dist = settings.player.distance_to(obj)
			if dist < closest_dist:  # it's closer, so remember it
				closest_enemy = obj
				closest_dist = dist
	return closest_enemy

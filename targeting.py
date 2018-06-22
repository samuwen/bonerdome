import libtcodpy as tcod
import handle_keys
import settings

# from render import render_all


def target_tile(max_range=None):
	(x, y) = (settings.mouse.cx, settings.mouse.cy)

	if (settings.mouse.lbutton_pressed and tcod.map_is_in_fov(settings.fov_map, x, y) and
		(max_range is None or settings.player.distance(x, y) <= max_range)):
		return (x, y)

	if settings.mouse.rbutton_pressed or settings.key.vk == tcod.KEY_ESCAPE:
		settings.game_state = 'playing'
		settings.look_mode = 'mouse'
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


def get_mouse_coordinates_in_look_mode(max_range=1):
	if handle_keys.is_key_pressed() and settings.game_state == 'looking':
		settings.old_x = settings.player.x
		settings.old_y = settings.player.y
		settings.look_mode = 'keyboard'
	x, y = settings.mouse.cx, settings.mouse.cy
	return (x, y)


def get_keyboard_coordinates_in_look_mode(max_range=1):
	x, y = settings.old_x, settings.old_y
	if settings.mouse.dx != 0 or settings.mouse.dy != 0:
		settings.look_mode = 'mouse'
	try:
		dx, dy = handle_keys.handle_direction_keys()
		x = settings.old_x + dx
		y = settings.old_y + dy
		settings.old_x = x
		settings.old_y = y
		return (x, y)
	except TypeError:
		return (x, y)


def get_names_at_target_location(x, y):
	# return a string with the names of all objects under the mouse
	# if objects are combatants, we get the direction they are facing too
	names = []
	for obj in settings.objects:
		if obj.x == x and obj.y == y and tcod.map_is_in_fov(settings.fov_map, obj.x, obj.y):
			if obj.combatant:
				names.append(obj.name + " (facing: " + obj.direction + ")")
			else:
				names.append(obj.name)

	names = ', '.join(names)
	return names.capitalize()

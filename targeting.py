import colors
import libtcodpy as tcod
import settings


def handle_basic_targeting(x, y, max_range=None):
	if settings.mouse.rbutton_pressed or settings.key.vk == tcod.KEY_ESCAPE:
		return 'cancelled'
	return is_target_valid(x, y, max_range)


def is_target_valid(x, y, max_range=None):
	if (tcod.map_is_in_fov(settings.fov_map, x, y) and
		(max_range is None or settings.player.distance(x, y) <= max_range)):
		return True
	return False


def target_monster(max_range):
	# returns a clicked monster in FOV up to a specific range

	(x, y) = settings.selection_coordinates
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


def display_highlight_square(max_range=2):
	(x, y) = settings.selection_coordinates
	if settings.game_state == 'playing':
		main_color = colors.mlook_hilite_neut
		secondary_color = colors.mlook_hilite_neut_secondary
	elif settings.game_state == 'looking':
		main_color = colors.mlook_hilite_look
		secondary_color = colors.mlook_hilite_look_secondary

	for i in range(1 - max_range, max_range):
		for j in range(1 - max_range, max_range):
			if i == 0 and j == 0:
				tcod.console_set_char_background(settings.targeting, x, y, main_color)
			else:
				tcod.console_set_char_background(settings.targeting, x + i, y + j, secondary_color)

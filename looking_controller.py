import libtcodpy as tcod
import settings

from menu import information_menu
from message import message


def looking_input(selection_action, direction_keys=None, max_range=None):
	is_direction = direction_keys

	if settings.key.vk == tcod.KEY_ESCAPE:
		return 'exit'
	if settings.look_mode == 'mouse':
		if is_direction is not None:
			settings.look_mode = 'keyboard'
		settings.selection_coordinates = (settings.mouse.cx, settings.mouse.cy)

	if settings.look_mode == 'keyboard':

		if settings.old_x is None or settings.old_y is None:
			settings.old_x = settings.mouse.cx
			settings.old_y = settings.mouse.cy

		x = settings.old_x
		y = settings.old_y
		if is_direction is not None:
			x = settings.old_x + is_direction[0]
			y = settings.old_y + is_direction[1]
			settings.old_x = x
			settings.old_y = y

		settings.selection_coordinates = (x, y)

		if settings.mouse.dx != 0 or settings.mouse.dy != 0:
			settings.look_mode = 'mouse'
			settings.old_x = None
			settings.old_y = None

	target_in_map_coords = settings.translate_screen_coords_to_map(*settings.selection_coordinates)
	if settings.mouse.lbutton_pressed or settings.key.vk == tcod.KEY_ENTER:
		if selection_action == 'info':
			information_menu(*settings.selection_coordinates)
		elif selection_action == 'target':
			if settings.player.distance(*target_in_map_coords) <= max_range:
				# change the screen selection to the actual map coordinates we want
				(x, y) = settings.selection_coordinates
				settings.selection_coordinates = ((x - settings.SCREEN_WIDTH // 2) + settings.player.x,
					(y - settings.SCREEN_HEIGHT // 2) + settings.player.y)
				return 'target_selected'
			else:
				message("Target is out of range!", tcod.lighter_red)

	if settings.highlight_state == 'target' or settings.highlight_state == 'target-out-of-bound':
		if settings.player.distance(*target_in_map_coords) > max_range:
			settings.highlight_state = 'target-out-of-bound'
		elif settings.player.distance(*target_in_map_coords) <= max_range:
			settings.highlight_state = 'target'

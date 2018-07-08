import libtcodpy as tcod
import settings

from looking_controller import looking_input
from message import message
from render import handle_rendering_tasks

target = None


def handle_basic_targeting(x, y, max_range=None):
	if settings.mouse.rbutton_pressed or settings.key.vk == tcod.KEY_ESCAPE:
		return 'cancelled'
	return is_target_valid(x, y, max_range)


def is_target_valid(x, y, max_range=None):
	if (tcod.map_is_in_fov(settings.fov_map, x, y) and
		(max_range is None or settings.player.distance(x, y) <= max_range)):
		return True
	return False


def choose_target(max_range):
	global target
	if target is None:
		while True:
			tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, settings.key, settings.mouse)
			try:
				is_direction = settings.keycode_to_direction_tuple_map[settings.key.vk]
			except KeyError:
				is_direction = None

			result = looking_input('target', direction_keys=is_direction, max_range=max_range)
			handle_rendering_tasks()
			# returns a clicked monster in FOV up to a specific range

			if result == 'target_selected':
				(x, y) = settings.selection_coordinates

				for obj in settings.objects:
					if obj.x == x and obj.y == y and obj.combatant and obj != settings.player:
						return obj
			elif result == 'exit':
				return None
	else:
		return target


def combatant_is_adjacent(x, y):
	target = None
	for obj in settings.objects:
		if obj.combatant and obj.x == x and obj.y == y:
			target = obj
			return target
	return None


def is_attack_from_behind(user, target):
	direction = target.combatant.direction
	attack_direction = user.combatant.get_direction_to_target(target)

	if direction == attack_direction:
		return True
	return False


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


def select_target(max_range):
	message("Select a target. Right click or Escape to cancel", tcod.light_cyan)
	settings.highlight_state = 'target'
	monster = choose_target(max_range)
	if monster is None:
		settings.highlight_state = 'play'
		return 'cancelled'
	return monster


def get_direction_from_coordinates(x, y):
	if x < 0 and y == 0:
		return 'west'
	elif x > 0 and y == 0:
		return 'east'
	elif y < 0 and x == 0:
		return 'north'
	elif y > 0 and x == 0:
		return 'south'
	elif x < 0 and y < 0:
		return 'northwest'
	elif x > 0 and y < 0:
		return 'northeast'
	elif x < 0 and y > 0:
		return 'southwest'
	elif x > 0 and y > 0:
		return 'southeast'


def get_coordinates_from_direction(direction):
	if direction == 'west':
		return (-1, 0)
	elif direction == 'east':
		return (1, 0)
	elif direction == 'north':
		return (0, -1)
	elif direction == 'south':
		return (0, 1)
	elif direction == 'northwest':
		return (-1, -1)
	elif direction == 'northeast':
		return (1, -1)
	elif direction == 'southwest':
		return (-1, 1)
	elif direction == 'southeast':
		return (1, 1)

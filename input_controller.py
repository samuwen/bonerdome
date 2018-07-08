import libtcodpy as tcod
import settings

from level_manager import next_level
from level_manager import previous_level
from looking_controller import looking_input
from map_handler import is_at_vertex
from map_handler import is_in_room
from menu import msgbox
from menu import abilities_menu
from menu import character_menu
from menu import inventory_menu
from message import message
from targeting import combatant_is_adjacent
from time_controller import advance_time
from utilities import add_tuples


def input_controller(game_state):
	tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, settings.key, settings.mouse)
	if settings.key.vk == tcod.KEY_ESCAPE:
		return 'exit'
	elif settings.key.vk == tcod.KEY_ENTER and settings.key.lalt:
		tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

	if game_state == 'playing':
		player_action = playing_input()
		if type(player_action) is tuple:
			player_move_or_attack(*player_action)
			advance_time()
	elif game_state == 'looking':
		looking_input('info', handle_direction_keys())
	elif game_state == 'running':
		run_in_direction(settings.running_direction)


def playing_input():
	# movement keys
	is_direction = handle_direction_keys()
	if is_direction is not None:
		return is_direction
	key_char = chr(settings.key.c)
	if key_char == 'g':
		for obj in settings.objects:
			if obj.x == settings.player.x and obj.y == settings.player.y and obj.item:
				obj.item.pick_up(settings.player)
				break
	if key_char == 'i':
		chosen_item = inventory_menu('Press the key next to the item to use it, or any other key to cancel.\n')
		if chosen_item is not None:
			chosen_item.use(settings.player)
			advance_time()
	if key_char == 's':
		chosen_ability = abilities_menu('Press the key next to the skill to use it, or any other key to cancel.\n')
		if chosen_ability is not None:
			for ability in settings.player.combatant.abilities:
				if ability == chosen_ability:
					ability.use(settings.player, None, ability.max_range)
	if key_char == 'd':
		chosen_item = inventory_menu("Press the letter next to the item to drop it.\n")
		if chosen_item is not None:
			chosen_item.drop(settings.player)
	if key_char == 'l':
		settings.game_state = 'looking'
		settings.highlight_state = 'look'
	if key_char == '.' and settings.key.shift:
		if settings.stairs_down.x == settings.player.x and settings.stairs_down.y == settings.player.y:
			next_level()
	if key_char == ',' and settings.key.shift:
		if settings.stairs_up.x == settings.player.x and settings.stairs_up.y == settings.player.y:
			if settings.dungeon_level != 1:
				previous_level()
			else:
				if settings.boner_dome in settings.player.combatant.inventory:
					msgbox("You escape with the Dome of Boners!")
					return 'exit'
				else:
					msgbox("You cannot leave until you have the Dome of Boners")
	if key_char == ',':
		settings.game_state = 'running'
		settings.running_direction = prompt_user_for_direction()
		run_in_direction(settings.running_direction)
	if key_char == 'c':
		# show character stats
		character_menu("Details about your character.\n")
	if key_char == 't':
		settings.player.combatant.set_target()
	if key_char == 'o':
		message('target is ' + settings.player.combatant.target.name, tcod.blue)

	settings.selection_coordinates = (settings.mouse.cx, settings.mouse.cy)


def handle_direction_keys():
	try:
		return settings.keycode_to_direction_tuple_map[settings.key.vk]
	except KeyError:
		return None


def player_move_or_attack(dx, dy):
	if (dx, dy) == (0, 0):
		return
	# coordinates to which the player is moving or attacking
	x = settings.player.x + dx
	y = settings.player.y + dy

	# try to find an attackable object
	target = combatant_is_adjacent(x, y)

	# attack if target found, otherwise move
	if target is not None:
		settings.player.combatant.attack(target)
		settings.player.combatant.set_direction(dx, dy)
	else:
		settings.player.move(dx, dy)
		settings.fov_recompute = True


def prompt_user_for_direction():
	keypress = tcod.console_wait_for_keypress(True)
	if keypress.vk not in settings.keycode_to_direction_tuple_map:
		message("Aborted")
		return None
	direction = settings.keycode_to_direction_tuple_map[keypress.vk]
	if type(direction) is not tuple:
		return None
	return direction


def is_key_pressed():
	if settings.key.vk != tcod.KEY_NONE and settings.key.pressed:
		return True
	return False


def run_in_direction(direction):
	in_room = is_in_room(settings.player.x, settings.player.y)
	at_vertex = is_at_vertex(settings.player.x, settings.player.y)
	current_location = (settings.player.x, settings.player.y)
	target_location = add_tuples(current_location, direction)
	if not interrupt_auto():
		settings.game_state = 'playing'
	if not settings.is_blocked(*target_location):
		settings.player.move(*direction)
		settings.fov_recompute = True
		advance_time()
		if in_room != is_in_room(settings.player.x, settings.player.y):
			settings.game_state = 'playing'
		if at_vertex != is_at_vertex(settings.player.x, settings.player.y):
			settings.game_state = 'playing'
	else:
		settings.game_state = 'playing'


def interrupt_auto():
	for obj in settings.objects:
		if obj.combatant is not None and tcod.map_is_in_fov(settings.fov_map, obj.x, obj.y) and obj != settings.player:
			return False
	return True

import libtcodpy as tcod
import settings

from menu import msgbox
from menu import abilities_menu
from menu import information_menu
from menu import inventory_menu
from message import message
from level_manager import next_level
from level_manager import previous_level
from targeting import combatant_is_adjacent
from targeting import target_tile


def handle_keys():
	tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, settings.key, settings.mouse)
	if settings.game_state == 'playing':
		if settings.key.vk == tcod.KEY_ESCAPE:
			return 'exit'
		elif settings.key.vk == tcod.KEY_ENTER and settings.key.lalt:
			tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
		# movement keys
		is_direction = handle_direction_keys()
		if is_direction is not None:
			return is_direction
		key_char = chr(settings.key.c)
		if key_char == 'g':
			for obj in settings.objects:
				if obj.x == settings.player.x and obj.y == settings.player.y and obj.item:
					obj.item.pick_up()
					break
		if key_char == 'i':
			chosen_item = inventory_menu('Press the key next to the item to use it, or any other key to cancel.\n')
			if chosen_item is not None:
				chosen_item.use(settings.player)
		if key_char == 's':
			chosen_ability = abilities_menu('Press the key next to the skill to use it, or any other key to cancel.\n')
			if chosen_ability is not None:
				for ability in settings.player.combatant.abilities:
					if ability == chosen_ability:
						ability.use(settings.player)
		if key_char == 'd':
			chosen_item = inventory_menu("Press the letter next to the item to drop it.\n")
			if chosen_item is not None:
				chosen_item.drop()
		if key_char == 'l':
			settings.game_state = 'looking'
		if key_char == '.' and settings.key.shift:
			if settings.stairs_down.x == settings.player.x and settings.stairs_down.y == settings.player.y:
				next_level()
		if key_char == ',' and settings.key.shift:
			if settings.stairs_up.x == settings.player.x and settings.stairs_up.y == settings.player.y:
				if settings.dungeon_level != 1:
					previous_level()
				else:
					if settings.boner_dome in settings.inventory:
						msgbox("You escape with the Dome of Boners!")
						return 'exit'
					else:
						msgbox("You cannot leave until you have the Dome of Boners")
		if key_char == 'c':
			# show character stats
			level_up_exp = settings.LEVEL_UP_BASE + settings.player.combatant.level * settings.LEVEL_UP_FACTOR
			msgbox("Character information\n\nLevel: " + str(settings.player.combatant.level) + "\nExperience: " +
				str(settings.player.combatant.xp) + "\nExperience to level up:" + str(level_up_exp - settings.player.combatant.xp) +
				"\n\nMaximum Hp: " + str(settings.player.combatant.max_hp) + "\nAttack: " + str(settings.player.combatant.power) +
				"\nDefense: " + str(settings.player.combatant.defense), settings.CHARACTER_SCREEN_WIDTH)

	elif settings.game_state == 'looking' and is_key_pressed():
		try:
			(x, y) = target_tile(max_range=None)
			information_menu(x, y)
		except TypeError as err:
			pass
	return 'didnt-take-turn'


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
		settings.player.set_direction(dx, dy)
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

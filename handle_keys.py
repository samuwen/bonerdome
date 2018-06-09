import libtcodpy as tcod
import settings

from menu import msgbox
from menu import inventory_menu
from next_level import next_level


def handle_keys():
	if settings.key.vk == tcod.KEY_ENTER and settings.key.lalt:
			# alt + enter == fullscreen toggle
			tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
	elif settings.key.vk == tcod.KEY_ESCAPE:
		# escape key == quit game
		return 'exit'

	if settings.game_state == 'playing':
		# movement keys
		if settings.key.vk == tcod.KEY_UP or settings.key.vk == tcod.KEY_KP8:
			player_move_or_attack(0, -1)
		elif settings.key.vk == tcod.KEY_KP9:
			player_move_or_attack(1, -1)
		elif settings.key.vk == tcod.KEY_RIGHT or settings.key.vk == tcod.KEY_KP6:
			player_move_or_attack(1, 0)
		elif settings.key.vk == tcod.KEY_KP3:
			player_move_or_attack(1, 1)
		elif settings.key.vk == tcod.KEY_DOWN or settings.key.vk == tcod.KEY_KP2:
			player_move_or_attack(0, 1)
		elif settings.key.vk == tcod.KEY_KP1:
			player_move_or_attack(-1, 1)
		elif settings.key.vk == tcod.KEY_LEFT or settings.key.vk == tcod.KEY_KP4:
			player_move_or_attack(-1, 0)
		elif settings.key.vk == tcod.KEY_KP7:
			player_move_or_attack(-1, -1)
		elif settings.key.vk == tcod.KEY_KP5:
			pass
		else:
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
			if key_char == 'd':
				chosen_item = inventory_menu("Press the letter next to the item to drop it.\n")
				if chosen_item is not None:
					chosen_item.drop()
			if key_char == '.' and settings.key.shift:
				if settings.stairs_down.x == settings.player.x and settings.stairs_down.y == settings.player.y:
					next_level()
			if key_char == 'c':
				# show character stats
				level_up_exp = settings.LEVEL_UP_BASE + settings.player.level * settings.LEVEL_UP_FACTOR
				msgbox("Character information\n\nLevel: " + str(settings.player.level) + "\nExperience: " +
					str(settings.player.fighter.xp) + "\nExperience to level up:" + str(level_up_exp - settings.player.fighter.xp) +
					"\n\nMaximum Hp: " + str(settings.player.fighter.max_hp) + "\nAttack: " + str(settings.player.fighter.power) +
					"\nDefense: " + str(settings.player.fighter.defense), settings.CHARACTER_SCREEN_WIDTH)

			return 'didnt-take-turn'


def player_move_or_attack(dx, dy):
	# coordinates to which the player is moving or attacking
	x = settings.player.x + dx
	y = settings.player.y + dy

	# try to find an attackable object
	target = None
	for obj in settings.objects:
		if obj.fighter and obj.x == x and obj.y == y:
			target = obj
			break

	# attack if target found, otherwise move
	if target is not None:
		settings.player.fighter.attack(target)
	else:
		settings.player.move(dx, dy)
		settings.fov_recompute = True

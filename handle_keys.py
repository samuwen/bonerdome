import libtcodpy as tcod
import settings
import skills

from menu import msgbox
from menu import inventory_menu
from menu import skills_menu
from level_manager import next_level
from level_manager import previous_level
from targetting import combatant_is_adjacent


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
			if key_char == 's':
				chosen_skill = skills_menu('Press the key next to the skill to use it, or any other key to cancel.\n')
				if chosen_skill is not None:
					if chosen_skill == 'smash':
						skills.smash(settings.player)
					elif chosen_skill == 'bash':
						skills.bash(settings.player)
			if key_char == 'd':
				chosen_item = inventory_menu("Press the letter next to the item to drop it.\n")
				if chosen_item is not None:
					chosen_item.drop()
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
				level_up_exp = settings.LEVEL_UP_BASE + settings.player.level * settings.LEVEL_UP_FACTOR
				msgbox("Character information\n\nLevel: " + str(settings.player.level) + "\nExperience: " +
					str(settings.player.combatant.xp) + "\nExperience to level up:" + str(level_up_exp - settings.player.combatant.xp) +
					"\n\nMaximum Hp: " + str(settings.player.combatant.max_hp) + "\nAttack: " + str(settings.player.combatant.power) +
					"\nDefense: " + str(settings.player.combatant.defense), settings.CHARACTER_SCREEN_WIDTH)

			return 'didnt-take-turn'


def player_move_or_attack(dx, dy):
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

import libtcodpy as tcod
import settings

from menu import menu
from message import message


def check_level_up():
	# see if the player's exp enables them to level up
	level_up_exp = settings.LEVEL_UP_BASE + settings.player.level * settings.LEVEL_UP_FACTOR
	if settings.player.fighter.xp >= level_up_exp:
		settings.player.level += 1
		settings.player.fighter.xp -= level_up_exp
		message("You gained a level. You are now level: " + str(settings.player.level), tcod.yellow)
		choice = None
		while choice is None:
			choice = menu("Level up! Choose a stat to raise:\n",
				["Constitution: (+20 hp)",
				"Dexterity: (+1 defense)",
				"Strength: (+1 offense)"], settings.LEVEL_UP_SCREEN_WIDTH)
		if choice == 0:
			settings.player.fighter.hp += 20
			settings.player.fighter.max_hp = 20
		elif choice == 1:
			settings.player.fighter.defense = 1
		elif choice == 2:
			settings.player.fighter.power = 1

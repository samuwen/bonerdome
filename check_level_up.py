import libtcodpy as tcod
import settings

from message import message


def check_level_up():
	# see if the player's exp enables them to level up
	level_up_exp = settings.LEVEL_UP_BASE + settings.player.combatant.level * settings.LEVEL_UP_FACTOR
	if settings.player.combatant.xp >= level_up_exp:
		settings.player.combatant.level_up()
		settings.player.combatant.level += 1
		# player gained a level, so gets new abilities
		settings.player.combatant.xp -= level_up_exp
		message("You gained a level. You are now level: " + str(settings.player.combatant.level), tcod.yellow)

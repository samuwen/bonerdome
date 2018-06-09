import libtcodpy as tcod
import settings

from message import message


def player_death(player):
	# the game ended
	message("You died!", tcod.lighter_red)
	settings.game_state = 'dead'

	# transform the player into a corpse
	settings.player.char = '%'
	settings.player.color = tcod.dark_red

import libtcodpy as tcod

from message import message


def monster_death(monster):
	# transform the monster into a corpse. it doesn't block, can't be attacked and can't move
	message(monster.name.capitalize() + ' is dead. You gained ' + str(monster.combatant.xp) + 'exp!', tcod.light_green)
	monster.char = '%'
	monster.color = tcod.dark_red
	monster.blocks = False
	monster.combatant = None
	monster.ai = None
	monster.name = 'remains of ' + monster.name
	monster.send_to_back()

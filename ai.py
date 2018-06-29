import libtcodpy as tcod
import settings

from message import message


class BasicMonster:
	# AI for a basic monster
	def take_turn(self):
		# a basic enemy takes its turn. if you can see it, it can see you
		monster = self.owner
		if tcod.map_is_in_fov(settings.fov_map, monster.x, monster.y):
			if monster.distance_to(settings.player) >= 2:
				monster.move_astar(settings.player)
			elif settings.player.combatant.hp > 0:
				monster.combatant.attack(settings.player)


class ConfusedMonster:
	# AI for confused monster
	def __init__(self, old_ai, num_turns=settings.CONFUSE_NUM_TURNS):
		self.old_ai = old_ai
		self.num_turns = num_turns

	def take_turn(self):
		if self.num_turns > 0:
			# move in a random direction
			self.owner.move(tcod.random_get_int(0, -1, 1), tcod.random_get_int(0, -1, 1))
			self.num_turns -= 1
		else:
			self.owner.ai = self.old_ai
			message("The " + self.owner.name + " is no longer confused!", tcod.red)


class HeldMonster:
	def __init__(self, old_ai, num_turns=settings.HOLD_NUM_TURNS):
		self.old_ai = old_ai
		self.num_turns = num_turns

	def take_turn(self):
		if self.num_turns > 0:
			monster = self.owner
			if tcod.map_is_in_fov(settings.fov_map, monster.x, monster.y):
				if monster.distance_to(settings.player) < 2:
					monster.combatant.attack(settings.player)
			self.num_turns -= 1
		else:
			self.owner.ai = self.old_ai
			message("The " + self.owner.name + " is no longer held!", tcod.red)

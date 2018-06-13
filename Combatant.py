import libtcodpy as tcod
import settings

from message import message


class Combatant:
	# combat-related properties and methods(monster, player, NPC)
	def __init__(self, hp, defense, power, xp, level, death_function=None, profession=None):
		self._base_max_hp = hp
		self.hp = hp
		self._base_defense = defense
		self._base_power = power
		self.xp = xp
		self.level = level
		self.death_function = death_function
		self.profession = profession
		if self.profession:
			self.profession.owner = self
		self.abilities = []

	def attack(self, target):
		# a simple formula for attack damage
		damage = self.power - target.combatant.defense

		if damage > 0:
			# make the target take some damage
			damage_color = tcod.red
			if self.owner.name == 'player':
				damage_color = tcod.light_amber
			message(self.owner.name.capitalize() + ' attacks ' + target.name.capitalize() +
				' for ' + str(damage) + ' hit points.', damage_color)
			target.combatant.take_damage(damage)
		else:
			message(self.owner.name.capitalize() + ' attacks ' + target.name.capitalize() +
				' but doesn\'t do any damage', tcod.orange)

	def take_damage(self, damage):
		# apply damage if possible
		if damage > 0:
			self.hp -= damage
		if self.hp <= 0:
			function = self.death_function
			if function is not None:
				function(self.owner)
			if self.owner != settings.player:  # yield xp to the player
				settings.player.combatant.xp += self.xp

	def heal(self, amount):
		self.hp += amount
		if self.hp > self.max_hp:
			self.hp = self.max_hp

	@property
	def power(self):
		bonus = sum(equipment.power_bonus for equipment in settings.get_all_equipped(self.owner))
		return self._base_power + bonus

	@power.setter
	def power(self, value):
		self._base_power += value

	@property
	def defense(self):
		bonus = sum(equipment.defense_bonus for equipment in settings.get_all_equipped(self.owner))
		return self._base_defense + bonus

	@defense.setter
	def defense(self, value):
		self._base_defense += value

	@property
	def max_hp(self):
		bonus = sum(equipment.max_hp_bonus for equipment in settings.get_all_equipped(self.owner))
		return self._base_max_hp + bonus

	@max_hp.setter
	def max_hp(self, value):
		self._base_max_hp += value

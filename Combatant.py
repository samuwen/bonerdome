import libtcodpy as tcod
import settings

from Equipment import Equipment
from message import message
from handle_random import roll_dice
from handle_random import roll_to_hit


class Combatant:
	# combat-related properties and methods(monster, player, NPC)
	def __init__(self, xp, level, death_function=None, profession=None):
		self.level = level
		self.xp = xp
		self.death_function = death_function
		self.profession = profession
		if self.profession:
			self.profession.owner = self
		self.strn = profession.strn
		self.dex = profession.dex
		self.con = profession.con
		self.intel = profession.intel
		self.hit_dice = profession.hit_dice
		self._base_max_hp = self.hit_dice[1] + self.profession.get_bonus_values(self.con)
		self.hp = self._base_max_hp
		self._base_defense = 10 + self.profession.get_bonus_values(self.dex)
		self._base_power = self.profession.get_bonus_values(self.strn)
		self.abilities = []
		self.inventory = []
		self.damage_modifier = 0
		self.equipment_slots = {
			"head": None,
			"neck": None,
			"shoulders": None,
			"chest": None,
			"legs": None,
			"right hand": None,
			"left hand": None,
			"left index finger": None,
			"right index finger": None,
			"feet": None
		}

	def attack(self, target):
		to_hit = roll_to_hit()
		if to_hit > target.combatant.defense:
			damage = self.power - target.combatant.damage_modifier
		else:
			damage = 0
			message(self.owner.name.capitalize() + ' misses ' + target.name.capitalize(), tcod.pink)
			return

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
		bonus = sum(roll_dice(equipment.damage_dice) + equipment.damage_bonus for equipment in self.get_all_equipped('weapon'))
		# Unarmed strike
		if self.equipment_slots['right hand'] is None and self.equipment_slots['left hand'] is None:
			bonus += (roll_dice([1, 2]))
		return self._base_power + bonus

	@power.setter
	def power(self, value):
		self._base_power += value

	@property
	def defense(self):
		bonus = sum(equipment.defense_bonus for equipment in self.get_all_equipped('armor'))
		return self._base_defense + bonus

	@defense.setter
	def defense(self, value):
		self._base_defense += value

	@property
	def max_hp(self):
		bonus = sum(equipment.max_hp_bonus for equipment in self.get_all_equipped('armor'))
		return self._base_max_hp + bonus

	@max_hp.setter
	def max_hp(self, value):
		self._base_max_hp += value

	def get_all_equipped(self, type):
		equipped_list = []
		for item in self.inventory:
			if item.equipment and item.equipment.is_equipped and item.equipment.type == type:
				equipped_list.append(item.equipment)
		return equipped_list

	def get_equipped_in_slot(self, slot):
		for obj in self.inventory:
			if obj.equipment and obj.equipment.slot == slot and obj.equipment.is_equipped:
				return obj.equipment
		return None

	def toggle_equipment_state(self, item):
		if item.is_equipped is True:
			self.remove_item_from_slot(item)
		else:
			self.equip_item_to_slot(item)

	def equip_item_to_slot(self, item):
		if self.equipment_slots[item.slot] is not None:
			message("Remove item from " + item.slot + " before equipping", tcod.white)
		else:
			self.equipment_slots[item.slot] = item
			item.is_equipped = True

	def remove_item_from_slot(self, item):
		self.equipment_slots[item.slot] = None
		item.is_equipped = False

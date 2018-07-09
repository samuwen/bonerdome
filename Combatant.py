import libtcodpy as tcod
import random
import settings
import targeting

from message import message
from handle_random import roll_dice
from handle_random import roll_to_hit


class Combatant:
	# combat-related properties and methods(monster, player, NPC)
	def __init__(self, xp, level, death_function=None, profession=None, target=None, direction=None):
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
		self.current_speed = 0
		self.speed_value = profession.speed
		self.hit_dice = profession.hit_dice
		self._base_max_hp = self.hit_dice[1] + self.profession.get_bonus_values(self.con)
		self.hp = self._base_max_hp
		if self.level > 1:
			for i in range(self.level - 1):
				self.level_up()
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
		self.target = target
		self.direction = direction
		if direction is None:
			self.direction = random.choice(['north', 'east', 'west', 'south'])

	def attack(self, target, behind_target=False):
		if behind_target is True:
			return self.backstab(target)
		dir = self.get_direction_to_target(target)
		self.set_direction(direction=dir)
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

	def backstab(self, target):
		hp = target.combatant.hp
		message(self.owner.name.capitalize() + ' backstabs ' + target.name.capitalize() + 'for ' +
			str(hp) + ' damage!!', tcod.darkest_red)
		target.combatant.take_damage(hp)

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

	def level_up(self):
		number = roll_dice(self.hit_dice) + self.profession.get_bonus_values(self.con)
		self.hp += number
		self._base_max_hp += number
		self.profession.get_abilities_for_level()

	def set_target(self, target=None, max_range=999):
		if target:
			self.target = target
			return
		self.target = targeting.select_target(max_range=max_range)
		settings.highlight_state = 'play'
		if self.target != 'cancelled':
			enemy_direction = self.get_direction_to_target(self.target)
			self.direction = enemy_direction
		else:
			self.clear_target()
			return 'cancelled'

	def get_target(self, max_range):
		if self.target is None:
			self.set_target(max_range=max_range)
		return self.target

	def clear_target(self):
		self.target = None

	def get_direction_to_target(self, other):
		x_diff = other.x - self.owner.x
		y_diff = other.y - self.owner.y

		return targeting.get_direction_from_coordinates(x_diff, y_diff)

	def set_direction(self, x=None, y=None, direction=None):
		if direction is None:
			direction = targeting.get_direction_from_coordinates(x, y)
		self.direction = direction

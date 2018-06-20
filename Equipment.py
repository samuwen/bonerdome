import libtcodpy as tcod
import settings

from message import message


class Equipment:
	""" an object that can be equipped, providing bonuses. automatically adds the Item component """
	def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
		self.slot = slot
		self.is_equipped = False
		self.power_bonus = power_bonus
		self.defense_bonus = defense_bonus
		self.max_hp_bonus = max_hp_bonus

	def toggle_equip(self):
		""" equips or dequips an item, depending on current state"""
		if self.is_equipped:
			self.dequip()
		else:
			self.equip()

	def equip(self):
		""" equips an item. if an item is already equipped in the slot, dequips it before equipping the new item """
		old_equipment = settings.get_equipped_in_slot(self.slot)
		if old_equipment is not None:
			old_equipment.dequip()
		self.is_equipped = True
		message("Equipped " + self.owner.name + " on " + self.slot + ".", tcod.light_green)

	def dequip(self):
		if not self.is_equipped:
			return
		self.is_equipped = False
		message("Removed " + self.owner.name + " from " + self.slot + ".", tcod.light_yellow)

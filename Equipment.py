import equipment_data


class Equipment:
	""" an object that can be equipped, providing bonuses. automatically adds the Item component """

	# def __init__(self, slot, type, power_bonus=0, defense_bonus=0, max_hp_bonus=0, damage_dice=None, damage_bonus=0):
	def __init__(self, equipment):
		self.equipment_component = equipment_data.equipment[equipment.lower()]
		self.slot = self.equipment_component['slot']
		self.type = self.equipment_component['type']
		self.is_equipped = False
		self.damage_dice = self.equipment_component['damage_dice']
		self.damage_bonus = self.equipment_component['damage_bonus']
		self.defense_bonus = self.equipment_component['defense_bonus']
		self.max_hp_bonus = self.equipment_component['max_hp_bonus']

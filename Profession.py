from Ability import Ability

import ability_data
import job_data


class Profession:
	def __init__(self, profession):
		self.profession = profession
		self.profession_component = job_data.job_data[self.profession.lower()]
		self.strn = self.profession_component[0]
		self.dex = self.profession_component[1]
		self.intel = self.profession_component[2]
		self.con = self.profession_component[3]
		self.hit_dice = self.profession_component[5]

	# Creates class instances of new abilities, pulled from a class dictionary file
	# Users only have those skills for which they have achieved the proper level
	def get_abilities_for_level(self):
		ability_list = self.profession_component[4]
		for index, ability in enumerate(ability_list):
			if int(index) <= self.owner.level:
				self.owner.abilities.append(Ability(*ability_data.get_ability_data(ability)))

	def get_bonus_values(self, value):
		value_arr = [
			-99, -5, -4, -4, -3, -3, -2, -2, -1, -1, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6,
			7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17
		]
		return value_arr[value]

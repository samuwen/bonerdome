import Fighter

from Ability import Ability


class Profession:
	def __init__(self, profession):
		self.profession = profession

	# Creates class instances of new abilities, pulled from a class dictionary file
	# Users only have those skills for which they have achieved the proper level
	def get_abilities_for_level(self):
		for index, ability in enumerate(Fighter.ability_list):
			if int(index) <= self.owner.level:
				self.owner.abilities.append(Ability(ability['use_function'], ability['cost'], ability['distance'],
					ability['name'], ability['damage'], ability['cooldown_time'], ability['succ_message'], ability['fail_message']))

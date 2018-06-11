import libtcodpy as tcod

from message import message


class Spell:
	def __init__(self, use_function, cost, cooldown_time=0, succ_message="success",
		fail_message="fail"):
		self.use_function = use_function
		self.cost = cost
		self.cooldown_time = cooldown_time
		self.succ_message = succ_message
		self.fail_message = fail_message

	def use(self, user, target):
		if self.use_function is None:
			message(self.owner.name + " cannot be used!", tcod.light_red)
		elif self.cooldown_time > 0:
			message("You're too tired to use that ability!")
		else:
			result = self.use_function(user, target)
			if result == 'fail':
				message(self.fail_message, tcod.light_red)
			elif result == 'success':
				message(self.succ_message, tcod.light_green)

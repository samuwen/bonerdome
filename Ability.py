import libtcodpy as tcod

from message import message


class Ability:
	def __init__(self, use_function, cost, distance, name, damage=0, cooldown_time=0, succ_message="success",
		fail_message="fail", max_range=1):
		self.use_function = use_function
		self.cost = cost
		self.distance = distance
		self.name = name
		self.damage = damage
		self.cooldown_time = cooldown_time
		self.current_cooldown_time = 0
		self.succ_message = succ_message
		self.fail_message = fail_message
		self.max_range = max_range

	def use(self, user, target, max_range):
		if self.use_function is None:
			message(self.owner.name + " cannot be used!", tcod.light_red)
		elif self.current_cooldown_time != 0:
			message("You're too tired to use that ability!")
		else:
			result = self.use_function(user, target, max_range, self.damage, self.distance)
			if result == 'fail':
				message(self.fail_message, tcod.light_red)
			elif result == 'success':
				self.current_cooldown_time = self.cooldown_time
				message(self.succ_message, tcod.light_green)

	def advance_cooldown_timer(self):
		if self.current_cooldown_time < 0:
			raise ValueError("Cooldown times cannot be negative")
		if self.ability_is_on_cooldown():
			self.current_cooldown_time -= 1

	def ability_is_on_cooldown(self):
		return self.current_cooldown_time > 0

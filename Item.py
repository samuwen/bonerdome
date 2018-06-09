import libtcodpy as tcod
import settings

from message import message


class Item:
	def __init__(self, use_function=None, succ_message=None, fail_message="Item use has failed"):
		self.use_function = use_function
		self.succ_message = succ_message
		self.fail_message = fail_message

	# an item that can be picked up and used
	def pick_up(self):
		# add to the player's inventory and remove from the map
		if len(settings.inventory) >= 26:
			message("Your inventory is full!", tcod.red)
		else:
			settings.inventory.append(self.owner)
			settings.objects.remove(self.owner)
			message("You picked up a " + self.owner.name + ".", tcod.green)
			equipment = self.owner.equipment
			if equipment and settings.get_equipped_in_slot(equipment.slot) is None:
				equipment.equip()

	def use(self, user):
		"""
		user is an object with a fighter component. ie a player or a monster
		"""
		if self.owner.equipment:
			self.owner.equipment.toggle_equip()
			return
		if self.use_function is None:
			message(self.owner.name + " cannot be used!", tcod.light_red)
		else:
			result = self.use_function(user)
			if result == 'fail':
				message(self.fail_message, tcod.light_red)
			elif result == 'success':
				message(self.succ_message, tcod.light_green)
				settings.inventory.remove(self.owner)

	def drop(self):
		# add to the map and remove from the player's inventory
		settings.objects.append(self.owner)
		settings.inventory.remove(self.owner)
		self.owner.x = settings.player.x
		self.owner.y = settings.player.y
		message("You dropped a " + self.owner.name + ".", tcod.yellow)
		if self.owner.equipment:
			self.owner.equipment.dequip()

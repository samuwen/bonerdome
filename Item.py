import libtcodpy as tcod
import settings

from message import message


class Item:
	def __init__(self, use_function=None, succ_message=None, fail_message="Item use has failed"):
		self.use_function = use_function
		self.succ_message = succ_message
		self.fail_message = fail_message

	# an item that can be picked up and used
	def pick_up(self, user):
		# add to the player's inventory and remove from the map
		if len(user.combatant.inventory) >= 26 and user == settings.player:
			message("Your inventory is full!", tcod.red)
		else:
			user.combatant.inventory.append(self.owner)
			settings.objects.remove(self.owner)
			message("You picked up a " + self.owner.name + ".", tcod.green)
			equipment = self.owner.equipment
			if equipment and settings.get_equipped_in_slot(equipment.slot) is None:
				equipment.equip()

	def use(self, user):
		"""
		user is an object with a combatant component. ie a player or a monster
		"""
		if self.owner.equipment:
			user.combatant.toggle_equipment_state(self.owner.equipment)
			return
		if self.use_function is None:
			message(self.owner.name + " cannot be used!", tcod.light_red)
		else:
			result = self.use_function(user)
			if result == 'fail':
				message(self.fail_message, tcod.light_red)
			elif result == 'success':
				message(self.succ_message, tcod.light_green)
				user.combatant.inventory.remove(self.owner)

	def drop(self, user):
		# add to the map and remove from the player's inventory
		settings.objects.append(self.owner)
		user.combatant.inventory.remove(self.owner)
		self.owner.x = settings.player.x
		self.owner.y = settings.player.y
		message("You dropped a " + self.owner.name + ".", tcod.yellow)
		if self.owner.equipment:
			self.owner.equipment.dequip()

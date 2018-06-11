import handle_keys
import settings

from message import message
from utilities import add_tuples


def smash(player, target):
	distance = 1
	damage = 20
	direction = handle_keys.prompt_user_for_direction()
	if direction == (0, 0) or type(direction) is not tuple:
		return 'fail'
	targets = fire_beam_in_direction((settings.player.x, settings.player.y), direction, distance)
	for obj in targets:
		message(obj.name.capitalize() + " takes " + str(damage) + " damage.")
		obj.combatant.take_damage(damage)
	return 'success'


def bash(obj=None):
	print("bash")


def fire_beam_in_direction(start_location, direction, distance):
	loc = add_tuples(start_location, direction)
	affected_list = []
	while distance > 0:
		for obj in settings.objects:
			if obj.combatant and (obj.x, obj.y) == loc:
				affected_list.append(obj)
		distance -= 1
		loc = add_tuples(loc, direction)
	return affected_list

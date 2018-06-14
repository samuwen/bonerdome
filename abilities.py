import ai
import handle_keys
import libtcodpy as tcod
import settings

from message import message
from targeting import target_monster
from targeting import target_tile
from utilities import add_tuples


def cast_heal(obj):
	if obj.combatant.hp == obj.combatant.max_hp:
		return 'cancelled'
	obj.combatant.heal(settings.HEAL_AMOUNT)
	return 'success'


def cast_lightning():
	# find closest enemy within a maximum range and damage it
	monster = settings.closest_monster(settings.LIGHTNING_RANGE)
	if monster is None:
		message("No enemy is close enough to strike", tcod.white)
		return 'cancelled'
	# zap it
	message("A lightning bolt strikes the " + monster.name + " with a loud thunder! The damage is " +
		str(settings.LIGHTNING_DAMAGE) + " hit points.", tcod.light_blue)
	monster.combatant.take_damage(settings.LIGHTNING_DAMAGE)


def cast_confuse(player=None, target=None):
	# find closest enemy in range and confuse it
	message("Left click an enemy to confuse it. Right click to cancel", tcod.light_cyan)
	monster = target_monster(settings.CONFUSE_RANGE)
	if monster is None:
		return 'cancelled'
	old_ai = monster.ai
	monster.ai = ai.ConfusedMonster(old_ai)
	monster.ai.owner = monster
	message(monster.name + ' looks confused!', tcod.green)


def cast_fireball():
	# ask the player for a target location to which the fireball shall be thrown
	message("Left-click a target tile for the fireball or right-click to cancel", tcod.light_cyan)
	(x, y) = target_tile()
	if x is None:
		return 'cancelled'
	message("The fireball explodes! Burning everything within " + str(settings.FIREBALL_RADIUS) + " tiles!", tcod.orange)

	for obj in settings.objects:
		if obj.distance(x, y) <= settings.FIREBALL_RADIUS and obj.combatant:
			message("The " + obj.name + " gets burned for " + str(settings.FIREBALL_DAMAGE) + " hit points.", tcod.red)
			obj.combatant.take_damage(settings.FIREBALL_DAMAGE)


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

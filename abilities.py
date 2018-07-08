import ai
import input_controller
import libtcodpy as tcod
import settings

from menu import msgbox
from message import message
from targeting import handle_basic_targeting
from time_controller import end_player_turn
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


def cast_confuse(user=None, target=None, max_range=settings.CONFUSE_RANGE):
	monster = user.combatant.get_target(max_range)
	if monster == 'cancelled':
		return 'cancelled'
	old_ai = monster.ai
	monster.ai = ai.ConfusedMonster(old_ai)
	monster.ai.owner = monster
	message(monster.name + ' looks confused!', tcod.green)
	end_player_turn()


def cast_hold_in_place(user=None, target=None, max_range=settings.HOLD_RANGE):
	monster = user.combatant.get_target(max_range)
	if monster == 'cancelled':
		return 'cancelled'
	old_ai = monster.ai
	monster.ai = ai.HeldMonster(old_ai)
	monster.ai.owner = monster
	message(monster.name + ' looks unable to move!', tcod.green)
	end_player_turn()


def cast_fireball():
	fireball_max_range = 10
	# ask the player for a target location to which the fireball shall be thrown
	message("Left-click a target tile for the fireball or right-click to cancel", tcod.light_cyan)
	target = handle_basic_targeting(*settings.selection_coordinates, fireball_max_range)
	if not target:
		msgbox("Invalid target")
		return 'cancelled'
	if target == 'cancelled':
		return 'cancelled'
	message("The fireball explodes! Burning everything within " + str(settings.FIREBALL_RADIUS) + " tiles!", tcod.orange)

	for obj in settings.objects:
		if obj.distance(*settings.selection_coordinates) <= settings.FIREBALL_RADIUS and obj.combatant:
			message("The " + obj.name + " gets burned for " + str(settings.FIREBALL_DAMAGE) + " hit points.", tcod.red)
			obj.combatant.take_damage(settings.FIREBALL_DAMAGE)


def smash(player, target, max_range):
	distance = 1
	damage = 20
	direction = input_controller.prompt_user_for_direction()
	if direction == (0, 0) or type(direction) is not tuple:
		return 'fail'
	targets = fire_beam_in_direction((settings.player.x, settings.player.y), direction, distance)
	for obj in targets:
		message(obj.name.capitalize() + " takes " + str(damage) + " damage.")
		obj.combatant.take_damage(damage)
	end_player_turn()


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


def backflip(user, target=None, max_range=None, damage=None, distance=None):
	target = user.combatant.get_target(max_range)
	if target is None:
		return 'cancelled'
	# get the direction that, if the user keeps on that line, will move them 2 directly back from the target
	direction = target.combatant.get_direction_to_target(user)
	(x, y) = user.combatant.get_coordinates_from_direction(direction)
	for i in range(distance):
		user.move(x, y)
	end_player_turn()
	return 'success'


def frontflip(user, target=None, max_range=None, damage=None, distance=None):
	target = user.combatant.get_target(max_range)
	if target is None:
		return 'cancelled'
	direction = user.combatant.get_direction_to_target(target)
	(x, y) = user.combatant.get_coordinates_from_direction(direction)
	for i in range(distance):
		user.x += x
		user.y += y
	user.combatant.direction = user.combatant.get_direction_to_target(target)
	return 'success'

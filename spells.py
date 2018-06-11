import ai
import libtcodpy as tcod
import settings

from message import message
from targetting import target_monster
from targetting import target_tile


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


def cast_confuse():
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

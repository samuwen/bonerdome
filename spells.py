import libtcodpy as tcod

HEAL_AMOUNT = 40

LIGHTNING_DAMAGE = 40
LIGHTNING_RANGE = 5

CONFUSE_NUM_TURNS = 10
CONFUSE_RANGE = 8

FIREBALL_RADIUS = 3
FIREBALL_DAMAGE = 25


def cast_heal(obj):
	if obj.fighter.hp == obj.fighter.max_hp:
		return 'cancelled'
	obj.fighter.heal(HEAL_AMOUNT)
	return 'success'


def cast_lightning():
	# find closest enemy within a maximum range and damage it
	monster = closest_monster(LIGHTNING_RANGE)
	if monster is None:
		message("No enemy is close enough to strike", tcod.white)
		return 'cancelled'
	# zap it
	message("A lightning bolt strikes the " + monster.name + " with a loud thunder! The damage is " +
		str(LIGHTNING_DAMAGE) + " hit points.", tcod.light_blue)
	monster.fighter.take_damage(LIGHTNING_DAMAGE)


def cast_confuse():
	# find closest enemy in range and confuse it
	message("Left click an enemy to confuse it. Right click to cancel", tcod.light_cyan)
	monster = target_monster(CONFUSE_RANGE)
	if monster is None:
		return 'cancelled'
	old_ai = monster.ai
	monster.ai = ConfusedMonster(old_ai)
	monster.ai.owner = monster
	message(monster.name + ' looks confused!', tcod.green)


def cast_fireball():
	# ask the player for a target location to which the fireball shall be thrown
	message("Left-click a target tile for the fireball or right-click to cancel", tcod.light_cyan)
	(x, y) = target_tile()
	if x is None:
		return 'cancelled'
	message("The fireball explodes! Burning everything within " + str(FIREBALL_RADIUS) + " tiles!", tcod.orange)

	for obj in objects:
		if obj.distance(x, y) <= FIREBALL_RADIUS and obj.fighter:
			message("The " + obj.name + " gets burned for " + str(FIREBALL_DAMAGE) + " hit points.", tcod.red)
			obj.fighter.take_damage(FIREBALL_DAMAGE)
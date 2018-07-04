import ai
import abilities
import libtcodpy as tcod
# No idea why I can't just do a from Profession import Profession
import Profession
import settings

from Combatant import Combatant
from Item import Item
from monster_death import monster_death
from Object import Object
from handle_random import random_choice


def place_objects(room):
	max_monsters = settings.from_dungeon_level([[2, 1], [3, 4], [5, 6]])
	monster_chances = {}
	monster_chances['orc'] = 80
	monster_chances['troll'] = settings.from_dungeon_level([[15, 3], [30, 5], [60, 7]])

	max_items = settings.from_dungeon_level([[1, 1], [2, 4]])

	item_chances = {}
	item_chances['heal'] = 35
	item_chances['lightning'] = settings.from_dungeon_level([[25, 4]])
	item_chances['fireball'] = settings.from_dungeon_level([[25, 6]])
	item_chances['confuse'] = settings.from_dungeon_level([[10, 2]])
	item_chances['sword'] = settings.from_dungeon_level([[5, 4]])
	item_chances['shield'] = settings.from_dungeon_level([[15, 8]])

	# num_monsters = tcod.random_get_int(0, 0, max_monsters)

	# for i in range(num_monsters):
	# 	x = tcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
	# 	y = tcod.random_get_int(0, room.y1 + 1, room.y2 - 1)
	# 	ai_component = ai.BasicMonster()

	# 	if not settings.is_blocked(x, y):
	# 		choice = random_choice(monster_chances)
	# 		if choice == 'orc':
	# 			profession_component = Profession.Profession(profession='orc')
	# 			combatant_component = Combatant(xp=35, level=1, death_function=monster_death,
	# 				profession=profession_component)
	# 			monster = Object(x, y, 'o', 'orc', tcod.desaturated_green, blocks=True, combatant=combatant_component,
	# 				ai=ai_component)
	# 		elif choice == 'troll':
	# 			profession_component = Profession.Profession(profession='troll')
	# 			combatant_component = Combatant(xp=100, level=1, death_function=monster_death,
	# 				profession=profession_component)
	# 			monster = Object(x, y, 'T', 'troll', tcod.darkest_green, blocks=True, combatant=combatant_component,
	# 				ai=ai_component)

	# 		settings.objects.append(monster)

	num_items = tcod.random_get_int(0, 0, max_items)
	for i in range(num_items):
		x = tcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
		y = tcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

		choice = random_choice(item_chances)
		if choice == 'heal':
			# create a healing potion 70% chance
			item_component = Item(use_function=abilities.cast_heal, succ_message="Using healing potion",
				fail_message="Already at max health!")
			item = Object(x, y, '!', 'healing potion', tcod.violet, item=item_component, always_visible=True)
		elif choice == 'lightning':
			# create a lightning bolt scroll 10% chance
			item_component = Item(use_function=abilities.cast_lightning, succ_message="Casting lightning bolt!",
				fail_message="This failed for some reason")
			item = Object(x, y, '#', 'scroll of lightning bolt', tcod.light_yellow, item=item_component, always_visible=True)
		elif choice == 'fireball':
			# create a fireball scroll 10% chance
			item_component = Item(use_function=abilities.cast_fireball)
			item = Object(x, y, '#', 'scroll of fireball', tcod.light_orange, item=item_component, always_visible=True)
		elif choice == 'confuse':
			# create a confuse scroll, 10% chance
			item_component = Item(use_function=abilities.cast_confuse)
			item = Object(x, y, '#', 'scroll of confusion', tcod.white, item=item_component, always_visible=True)

		if not settings.is_blocked(x, y):
			settings.objects.append(item)
			item.send_to_back()

import ai
import libtcodpy as tcod
import settings
import spells

from Equipment import Equipment
from Fighter import Fighter
from Item import Item
from monster_death import monster_death
from Object import Object
from random_choice import random_choice


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

	num_monsters = tcod.random_get_int(0, 0, max_monsters)

	for i in range(num_monsters):
		x = tcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
		y = tcod.random_get_int(0, room.y1 + 1, room.y2 - 1)
		ai_component = ai.BasicMonster()

		if not settings.is_blocked(x, y):
			choice = random_choice(monster_chances)
			if choice == 'orc':
				fighter_component = Fighter(hp=20, defense=0, power=4, xp=35, death_function=monster_death)
				monster = Object(x, y, 'o', 'orc', tcod.desaturated_green, blocks=True, fighter=fighter_component,
					ai=ai_component)
			elif choice == 'troll':
				fighter_component = Fighter(hp=30, defense=2, power=8, xp=100, death_function=monster_death)
				monster = Object(x, y, 'T', 'troll', tcod.darkest_green, blocks=True, fighter=fighter_component,
					ai=ai_component)

			settings.objects.append(monster)

	num_items = tcod.random_get_int(0, 0, max_items)
	for i in range(num_items):
		x = tcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
		y = tcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

		choice = random_choice(item_chances)
		if choice == 'heal':
			# create a healing potion 70% chance
			item_component = Item(use_function=spells.cast_heal, succ_message="Using healing potion",
				fail_message="Already at max health!")
			item = Object(x, y, '!', 'healing potion', tcod.violet, item=item_component, always_visible=True)
		elif choice == 'lightning':
			# create a lightning bolt scroll 10% chance
			item_component = Item(use_function=spells.cast_lightning, succ_message="Casting lightning bolt!",
				fail_message="This failed for some reason")
			item = Object(x, y, '#', 'scroll of lightning bolt', tcod.light_yellow, item=item_component, always_visible=True)
		elif choice == 'fireball':
			# create a fireball scroll 10% chance
			item_component = Item(use_function=spells.cast_fireball)
			item = Object(x, y, '#', 'scroll of fireball', tcod.light_orange, item=item_component, always_visible=True)
		elif choice == 'confuse':
			# create a confuse scroll, 10% chance
			item_component = Item(use_function=spells.cast_confuse)
			item = Object(x, y, '#', 'scroll of confusion', tcod.white, item=item_component, always_visible=True)
		elif choice == 'sword':
			equipment_component = Equipment(slot='right hand', power_bonus=3)
			item = Object(x, y, '/', 'sword', tcod.chartreuse, equipment=equipment_component)
		elif choice == 'shield':
			equipment_component = Equipment(slot='left hand', defense_bonus=1)
			item = Object(x, y, '[', 'shield', tcod.darker_orange, equipment=equipment_component)

		if not settings.is_blocked(x, y):
			settings.objects.append(item)
			item.send_to_back()

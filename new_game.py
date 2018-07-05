import libtcodpy as tcod
import settings

from create_character import choose_job
from Combatant import Combatant
from Equipment import Equipment
from Profession import Profession
from initialize_fov import initialize_fov
from map_handler import make_map
from Object import Object
from player_death import player_death


def new_game():
	settings.init_new_game()

	profession = choose_job()

	if profession is None:
		return None

	profession_component = Profession(profession=profession)
	combatant_component = Combatant(xp=0, level=1, death_function=player_death,
		profession=profession_component)
	settings.player = Object(0, 0, '@', 'player', tcod.white, blocks=True, combatant=combatant_component)
	settings.player.combatant.profession.get_abilities_for_level()
	settings.dungeon_level = 1
	settings.mouse_x = settings.player.x
	settings.mouse_y = settings.player.y

	make_map()
	settings.save_level_state()
	initialize_fov()

	settings.game_state = 'playing'

	equipment = 'dagger'
	equipment_component = Equipment(equipment=equipment)
	obj = Object(0, 0, '-', 'dagger', tcod.light_blue, equipment=equipment_component)
	settings.player.combatant.inventory.append(obj)
	settings.player.combatant.equip_item_to_slot(equipment_component)
	obj.always_visible = True

	equipment = 'clothes'
	equipment_component = Equipment(equipment=equipment)
	obj = Object(0, 0, '#', 'clothes', tcod.light_gray, equipment=equipment_component)
	settings.player.combatant.inventory.append(obj)
	settings.player.combatant.toggle_equipment_state(equipment_component)
	obj.always_visible = True
	return "go"

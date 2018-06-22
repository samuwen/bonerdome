import libtcodpy as tcod
import settings

from create_character import choose_job
from Combatant import Combatant
from Equipment import Equipment
from Profession import Profession
from initialize_fov import initialize_fov
from map_handler import make_map
from message import message
from Object import Object
from player_death import player_death


def new_game():
	settings.init_new_game()

	choose_job()

	profession_component = Profession(profession=settings.profession)
	combatant_component = Combatant(hp=100, defense=1, power=2, xp=0, level=1, death_function=player_death,
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

	message('Welcome to the boner dome.', tcod.cyan)

	equipment_component = Equipment(slot='right hand', power_bonus=2)
	obj = Object(0, 0, '-', 'dagger', tcod.light_blue, equipment=equipment_component)
	settings.inventory.append(obj)
	equipment_component.equip()
	obj.always_visible = True

import libtcodpy as tcod
import settings

from Combatant import Combatant
from Equipment import Equipment
from Fighter import Fighter
from initialize_fov import initialize_fov
from map_handler import make_map
from message import message
from Object import Object
from player_death import player_death


def new_game():
	profession_component = Fighter()
	combatant_component = Combatant(hp=100, defense=1, power=2, xp=0, death_function=player_death, profession=profession_component)
	settings.player = Object(0, 0, '@', 'player', tcod.white, blocks=True, combatant=combatant_component)
	settings.skills = settings.player.combatant.profession.skills

	settings.player.level = 1
	settings.dungeon_level = 1

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

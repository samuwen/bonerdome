import libtcodpy as tcod
import settings

from check_level_up import check_level_up
from handle_keys import handle_keys
from handle_keys import player_move_or_attack
from render import render_all


def play_game():
	# clear the root console (Clears the startup images)
	tcod.console_clear(0)

	settings.mouse = tcod.Mouse()
	settings.key = tcod.Key()
	settings.highlight_xy = (settings.player.x, settings.player.y)

	# MAIN LOOP
	while not tcod.console_is_window_closed():
		if settings.game_state == 'playing':
			handle_rendering_tasks()
			check_level_up()

			settings.player_action = handle_keys()
			# movement action are returned as tuples
			if type(settings.player_action) is tuple:
				player_move_or_attack(*settings.player_action)
			if settings.player_action == 'exit':
				settings.save_game()
				break

			if settings.player_action != 'didnt-take-turn':
				for obj in settings.objects:
					if obj.ai:
						obj.ai.take_turn()
					if obj.combatant:
						for ability in obj.combatant.abilities:
							ability.advance_cooldown_timer()
		elif settings.game_state == 'looking':
			handle_rendering_tasks()

			settings.player_action = handle_keys()
			if settings.player_action == 'exit':
				settings.game_state = 'playing'


def handle_rendering_tasks():
	render_all()
	tcod.console_flush()
	for obj in settings.objects:
		obj.clear()

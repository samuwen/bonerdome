import libtcodpy as tcod
import settings

from check_level_up import check_level_up
from input_controller import input_controller
from render import handle_rendering_tasks


def play_game():
	# clear the root console (Clears the startup images)
	tcod.console_clear(0)

	settings.mouse = tcod.Mouse()
	settings.key = tcod.Key()
	settings.highlight_xy = (settings.player.x, settings.player.y)

	# MAIN LOOP
	while not tcod.console_is_window_closed():
		handle_rendering_tasks()
		check_level_up()

		settings.player_action = input_controller(settings.game_state)
		if settings.player_action == 'exit' and settings.game_state == 'playing':
			settings.save_game()
			break
		elif settings.player_action == 'exit':
			settings.game_state = 'playing'
			settings.highlight_state = 'play'

		if settings.player_action == 'time-should-advance':
			for obj in settings.objects:
				if obj.ai:
					obj.ai.take_turn()
				if obj.combatant:
					for ability in obj.combatant.abilities:
						ability.advance_cooldown_timer()

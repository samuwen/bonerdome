import libtcodpy as tcod
import settings

from check_level_up import check_level_up
from handle_keys import handle_keys
from render import render_all


def play_game():
	settings.mouse = tcod.Mouse()
	settings.key = tcod.Key()

	# clear the root console to get rid of the dumb extra garbage
	tcod.console_clear(0)

	# MAIN LOOP
	while not tcod.console_is_window_closed():
		tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, settings.key, settings.mouse)

		render_all()
		tcod.console_flush()
		check_level_up()

		for obj in settings.objects:
			obj.clear()

		settings.player_action = handle_keys()
		if settings.player_action == 'exit':
			settings.save_game()
			break

		if settings.game_state == 'playing' and settings.player_action != 'didnt-take-turn':
			for obj in settings.objects:
				if obj.ai:
					obj.ai.take_turn()

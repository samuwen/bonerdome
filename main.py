import libtcodpy as tcod
import settings

from menu import menu
from menu import msgbox
from new_game import new_game
from play_game import play_game

settings.init()

if __name__ == "__main__":
	img = tcod.image_load('assets/images/menu_background1.png')
	while not tcod.console_is_window_closed():
		tcod.image_blit_2x(img, 0, 0, 0)

		tcod.console_set_default_foreground(0, tcod.light_yellow)
		tcod.console_print_ex(0, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 - 4, tcod.BKGND_NONE, tcod.CENTER,
			'Legend of the Boner Dome')
		tcod.console_print_ex(0, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 2, tcod.BKGND_NONE, tcod.CENTER,
			'By Jack Chick')

		choice = menu('', ['Play a new game', 'Continue last game', 'Quit'], 24)

		if choice == 0:
			new_game()
			play_game()
		elif choice == 1:
			try:
				settings.load_game()
			except (KeyError) as err:
				print("***ERROR: Key not found: " + str(err))
				msgbox("No savegame found", 24)
				continue
			play_game()
		elif choice == 2:
			break

import colors
import libtcodpy as tcod
import settings


def render_all():
	if settings.fov_recompute:
		settings.fov_recompute = False
		tcod.map_compute_fov(settings.fov_map, settings.player.x, settings.player.y, settings.TORCH_RADIUS,
			settings.FOV_LIGHT_WALLS, settings.FOV_ALGO)

	for y in range(settings.MAP_HEIGHT):
		for x in range(settings.MAP_WIDTH):
			visible = tcod.map_is_in_fov(settings.fov_map, x, y)
			wall = settings.dungeon_map[x][y].block_sight
			if not visible:
				if settings.dungeon_map[x][y].explored:
					# its out of the player's FOV
					if wall:
						tcod.console_set_char_background(settings.con, x, y, colors.color_dark_wall,
							tcod.BKGND_SET)
					else:
						tcod.console_set_char_background(settings.con, x, y, colors.color_dark_ground,
							tcod.BKGND_SET)
			else:
				# its visible
				if wall:
					tcod.console_set_char_background(settings.con, x, y, colors.color_light_wall,
						tcod.BKGND_SET)
				else:
					tcod.console_set_char_background(settings.con, x, y, colors.color_light_ground,
						tcod.BKGND_SET)
				settings.dungeon_map[x][y].explored = True

	# draw all objects in the list
	for obj in settings.objects:
		if obj != settings.player:
			obj.draw()
	settings.player.draw()

	tcod.console_blit(settings.con, 0, 0, settings.MAP_WIDTH, settings.MAP_HEIGHT, 0, 0, 0)

	# prepare to render the GUI panel
	tcod.console_set_default_background(settings.panel, tcod.black)
	tcod.console_clear(settings.panel)

	# print the game messages
	y = 1
	for (line, color) in settings.game_messages:
		tcod.console_set_default_foreground(settings.panel, color)
		tcod.console_print_ex(settings.panel, settings.MSG_X, y, tcod.BKGND_NONE, tcod.LEFT, line)
		y += 1

	# show player's stats
	render_bar(1, 1, settings.BAR_WIDTH, "HP", settings.player.combatant.hp, settings.player.combatant.max_hp,
		tcod.light_red, tcod.darker_red)
	tcod.console_print_ex(settings.panel, 1, 3, tcod.BKGND_NONE, tcod.LEFT, 'Dungeon level ' +
		str(settings.dungeon_level))
	tcod.console_set_default_foreground(settings.panel, tcod.light_gray)
	tcod.console_print_ex(settings.panel, 1, 0, tcod.BKGND_NONE, tcod.LEFT, settings.get_names_under_mouse())

	tcod.console_blit(settings.panel, 0, 0, settings.SCREEN_WIDTH, settings.PANEL_HEIGHT, 0, 0, settings.PANEL_Y)


def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
	# render a bar (HP, exp, etc)
	# calculate the width of the bar
	bar_width = int(float(value) / maximum * total_width)

	# render background first
	tcod.console_set_default_background(settings.panel, back_color)
	tcod.console_rect(settings.panel, x, y, total_width, 1, False, tcod.BKGND_SCREEN)

	# now render the bar on top
	tcod.console_set_default_background(settings.panel, bar_color)
	if bar_width > 0:
		tcod.console_rect(settings.panel, x, y, bar_width, 1, False, tcod.BKGND_SCREEN)

	# finally, some centered text with the values
	tcod.console_set_default_foreground(settings.panel, tcod.white)
	display_value = name + ': ' + str(value) + '/' + str(maximum)

	tcod.console_print_ex(settings.panel, x + total_width // 2, y, tcod.BKGND_NONE, tcod.CENTER, display_value)

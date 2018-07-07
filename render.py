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
						tcod.console_set_char_background(settings.con, x, y, colors.dark_wall,
								tcod.BKGND_SET)
					else:
						tcod.console_set_char_background(settings.con, x, y, colors.dark_ground,
								tcod.BKGND_SET)
			else:
				# its visible
				if wall:
					tcod.console_set_char_background(settings.con, x, y, colors.light_wall,
							tcod.BKGND_SET)
				else:
					tcod.console_set_char_background(settings.con, x, y, colors.light_ground,
							tcod.BKGND_SET)
				settings.dungeon_map[x][y].explored = True

	# draw all objects in the list
	for obj in settings.objects:
		if obj != settings.player:
			obj.draw()
	settings.player.draw()

	half_screen_x = settings.SCREEN_WIDTH // 2
	half_screen_y = settings.SCREEN_HEIGHT // 2

	tcod.console_blit(settings.con, settings.player.x - half_screen_x, settings.player.y - half_screen_y,
		settings.MAP_WIDTH, settings.MAP_HEIGHT, 0, 0, 0)
	display_highlight_square()
	tcod.console_blit(settings.targeting, 0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, 0, 0, 0, 0.0, 0.15)
	tcod.console_clear(settings.targeting)

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
	try:
		render_bar(1, 1, settings.BAR_WIDTH, "HP", settings.player.combatant.hp, settings.player.combatant.max_hp,
			tcod.light_red, tcod.darker_red)
	except AttributeError as err:
		print(err)
	tcod.console_print_ex(settings.panel, 1, 3, tcod.BKGND_NONE, tcod.LEFT, 'Dungeon level ' +
		str(settings.dungeon_level))
	tcod.console_set_default_foreground(settings.panel, tcod.light_gray)
	tcod.console_print_ex(settings.panel, 1, 0, tcod.BKGND_NONE, tcod.LEFT,
		get_names_at_target_location(*settings.selection_coordinates))

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


def display_highlight_square(max_range=2):
	(x, y) = settings.selection_coordinates
	if settings.highlight_state == 'play':
		main_color = colors.mlook_hilite_neut
		secondary_color = colors.mlook_hilite_neut_secondary
	elif settings.highlight_state == 'look':
		main_color = colors.mlook_hilite_look
		secondary_color = colors.mlook_hilite_look_secondary
	elif settings.highlight_state == 'target':
		main_color = colors.target_hilite_main
		secondary_color = colors.target_hilite_secondary
	elif settings.highlight_state == 'target-out-of-bound':
		main_color = colors.target_hilite_oob_main
		secondary_color = colors.target_hilite_oob_secondary

	for i in range(1 - max_range, max_range):
		for j in range(1 - max_range, max_range):
			if i == 0 and j == 0:
				tcod.console_set_char_background(settings.targeting, x, y, main_color)
			else:
				tcod.console_set_char_background(settings.targeting, x + i, y + j, secondary_color)


def get_names_at_target_location(x, y):
	# return a string with the names of all objects under the mouse
	# if objects are combatants, we get the direction they are facing too
	names = []
	(x1, y1) = settings.translate_screen_coords_to_map(x, y)
	for obj in settings.objects:
		if obj.x == x1 and obj.y == y1 and tcod.map_is_in_fov(settings.fov_map, obj.x, obj.y):
			if obj.combatant:
				names.append(obj.name + " (facing: " + obj.combatant.direction + ") ")
			else:
				names.append(obj.name)

	names = ', '.join(names)
	return names.capitalize()


def handle_rendering_tasks():
	render_all()
	tcod.console_flush()
	for obj in settings.objects:
		obj.clear()

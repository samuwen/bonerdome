import libtcodpy as tcod
import settings


def menu(header, options, width, new_game=None):
	if len(options) > 26:
		raise ValueError('Cannot have a menu with more than 26 options')
	# calculate the total height for the header (after auto-wrap) and one line per option
	header_height = tcod.console_get_height_rect(settings.con, 0, 0, width, settings.SCREEN_HEIGHT, header)
	if header == '':
		header_height = 0
	height = len(options) + header_height

	# new console to handle the menu options
	window = tcod.console_new(width, height)

	# print the header with auto-wrap
	tcod.console_set_default_foreground(window, tcod.white)
	tcod.console_print_rect_ex(window, 0, 0, width, height, tcod.BKGND_NONE, tcod.LEFT, header)

	y = header_height
	letter_index = ord('a')
	for option_text in options:
		text = '(' + chr(letter_index) + ') ' + option_text
		tcod.console_print_ex(window, 0, y, tcod.BKGND_NONE, tcod.LEFT, text)
		y += 1
		letter_index += 1

	x = 0
	y = 0
	if new_game:
		x = settings.SCREEN_WIDTH // 2 - width // 2
		y = settings.SCREEN_HEIGHT // 2 - height // 2
	tcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 1.0)

	# present console to the player and wait for keypress
	tcod.console_flush()
	key = tcod.console_wait_for_keypress(True)

	# once a player presses a key
	index = key.c - ord('a')
	if key.vk == tcod.KEY_ENTER and key.lalt:
		# alt + enter == fullscreen toggle
		tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
	if index >= 0 and index < len(options):
		return index
	return None


def msgbox(text, width=50):
	menu(text, [], width)  # menu is a jury-rigged message box


def inventory_menu(header):
	# show a menu with each item of the inventory as an option
	if len(settings.player.combatant.inventory) == 0:
		options = ['Inventory is empty.']
	else:
		options = []
		for item in settings.player.combatant.inventory:
			text = item.name
			if item.equipment and item.equipment.is_equipped:
				text = text + ' (on ' + item.equipment.slot + ')'
			options.append(text)
	index = menu(header, options, settings.INVENTORY_WIDTH)
	if index is None or len(settings.player.combatant.inventory) == 0:
		return None
	return settings.player.combatant.inventory[index].item


def abilities_menu(header):
	options = []
	abilities = settings.player.combatant.abilities
	for ability in abilities:
		avail = ""
		if ability.current_cooldown_time > 0:
			avail = " (" + str(ability.current_cooldown_time) + " turns until ready)"
		options.append(ability.name + avail)
	index = menu(header, options, settings.ABILITY_WIDTH)
	if index is None or len(abilities) == 0:
		return None
	return abilities[index]


def information_menu(x, y):
	for obj in settings.objects:
		if obj.x == x and obj.y == y and tcod.map_is_in_fov(settings.fov_map, obj.x, obj.y):
			index = menu(obj.name.capitalize(), ["Here's a bunch of info about this object."], 50)
			return index


def character_menu(header):
	level_up_exp = settings.LEVEL_UP_BASE + settings.player.combatant.level * settings.LEVEL_UP_FACTOR
	try:
		num_dice = settings.player.combatant.get_equipped_in_slot('right hand').damage_dice[0]
		dice_faces = settings.player.combatant.get_equipped_in_slot('right hand').damage_dice[1]
	except AttributeError:
		num_dice = str(1)
		dice_faces = str(2)

	msgbox("Character information\n\nLevel: " + str(settings.player.combatant.level) +
		"\nExperience: " + str(settings.player.combatant.xp) +
		"\nExperience to level up:" + str(level_up_exp - settings.player.combatant.xp) +
		"\n\nMaximum Hp: " + str(settings.player.combatant.max_hp) +
		"\nAttack: " + str(num_dice) + 'd' + str(dice_faces) +
		"\nDefense: " + str(settings.player.combatant.defense) +
		"\nStrength: " + str(settings.player.combatant.strn) +
		"\nDexterity: " + str(settings.player.combatant.dex) +
		"\nIntelligence: " + str(settings.player.combatant.intel) +
		"\nConstitution: " + str(settings.player.combatant.con), settings.CHARACTER_SCREEN_WIDTH)

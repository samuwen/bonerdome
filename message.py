import libtcodpy as tcod
import settings
import textwrap


def message(new_msg, color=tcod.white):
	# split the message if necessary, among multiple lines
	new_msg_lines = textwrap.wrap(new_msg, settings.MSG_WIDTH)

	for line in new_msg_lines:
		# if the buffer is full, remove the first line to make room for the new one
		if len(settings.game_messages) == settings.MSG_HEIGHT:
			del settings.game_messages[0]

		# add the new line as a tuple: (text, color)
		settings.game_messages.append((line, color))

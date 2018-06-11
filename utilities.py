debug_mode = False


def print_debug(text):
	if debug_mode:
		print(text)


def add_tuples(xs, ys):
	return tuple(x + y for x, y in zip(xs, ys))

debug_mode = False


def print_debug(text):
	if debug_mode:
		print(text)


def add_tuples(xs, ys):
	'''
	Takes in two tuples and adds their values together. ie:
	(1, 1), (2, 2) = (3, 3)
	'''
	return tuple(x + y for x, y in zip(xs, ys))

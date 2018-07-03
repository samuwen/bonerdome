import libtcodpy as tcod


def random_choice(chances_dict):
	chances = chances_dict.values()
	strings = list(chances_dict)
	return strings[random_choice_index(chances)]


def random_choice_index(chances):  # choose 1 option from a list of chances, returning its index
	# the dice will land on some number between 1 and the sum of the chances
	dice = tcod.random_get_int(0, 1, sum(chances))

	# go through all chances, keeping the sum so far
	running_sum = 0
	choice = 0
	for w in chances:
		running_sum += w

		# see if the dice landed in the part that corresponds to this choice
		if dice <= running_sum:
			return choice
		choice += 1


def roll_dice(die_tuple):
	result = 0
	for i in range(die_tuple[0]):
		result += tcod.random_get_int(0, 1, die_tuple[1])
	return result


def roll_to_hit():
	return roll_dice((1, 20))

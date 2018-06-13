import abilities

# from pathlib import Path

smash = {
	'use_function': abilities.smash,
	'cost': 0,
	'distance': 1,
	'name': 'smash',
	'damage': 20,
	'cooldown_time': 5,
	'succ_message': "smashed enemy",
	'fail_message': 'failed to smash enemy'
}

# ability_list should be ordered by level. Lower ordinal abilities are available at lower levels
ability_list = [smash]


# def get_ability_list(profession):
# 	p = Path('.')
# 	folder = p / 'data'
# 	for file in folder.iterdir():
# 		f = open(file)
# 		ability_list = []
# 		for line in f:
# 			ability_list.append(line.split(','))
# 	return ability_list

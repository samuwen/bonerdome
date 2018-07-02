import abilities

ability = {
	'smash': {
		'use_function': abilities.smash,
		'cost': 0,
		'distance': 1,
		'name': 'smash',
		'damage': 20,
		'cooldown_time': 5,
		'succ_message': "smashed enemy",
		'fail_message': 'failed to smash enemy',
		'max_range': 1
	},
	'confuse': {
		'use_function': abilities.cast_confuse,
		'cost': 0,
		'distance': 1,
		'name': 'confuse',
		'damage': 0,
		'cooldown_time': 5,
		'succ_message': "confused enemy",
		'fail_message': 'failed to confuse enemy',
		'max_range': 8
	},
	'hold_person': {
		'use_function': abilities.cast_hold_in_place,
		'cost': 0,
		'distance': 1,
		'name': 'hold position',
		'damage': 0,
		'cooldown_time': 5,
		'succ_message': "held enemy",
		'fail_message': 'failed to hold enemy',
		'max_range': 6
	}
}


def get_ability_data(key_name):
	return (ability[key_name]['use_function'], ability[key_name]['cost'], ability[key_name]['distance'],
		ability[key_name]['name'], ability[key_name]['damage'], ability[key_name]['cooldown_time'],
		ability[key_name]['succ_message'], ability[key_name]['fail_message'], ability[key_name]['max_range'])

equipment = {
	'dagger': {
		'slot': 'right hand',
		'type': 'weapon',
		'damage_dice': (1, 4),
		'damage_bonus': 0,
		'defense_bonus': 0,
		'max_hp_bonus': 0
	},
	'clothes': {
		'slot': 'chest',
		'type': 'armor',
		'damage_dice': (0, 0),
		'damage_bonus': 0,
		'defense_bonus': 1,
		'max_hp_bonus': 0
	}
}


def get_equipment_data(key_name):
	return (equipment[key_name]['slot'], equipment[key_name]['type'], equipment[key_name]['damage_dice'],
		equipment[key_name]['defense_bonus'])

# data fields here are as follows:
# strength, dexterity, intelligence, constitution, ability array (as strings), hit dice [num_dice, dice_faces]
job_data = {
	'fighter': [15, 10, 8, 15, ['smash', 'hold_person', 'confuse'], (1, 8)],
	'wizard': [8, 10, 15, 10, ['confuse', 'hold_person', 'smash'], (1, 4)],
	'orc': [12, 8, 5, 16, [], [1, 7]],
	'troll': [17, 10, 3, 17, [], [2, 9]]
}

from menu import menu


def choose_job():
	profession_list = ['Pickpocket', 'Wizard']
	profession_choice = menu('Choose a profession', profession_list, 24, new_game=True)
	if profession_choice is not None:
		return profession_list[profession_choice]
	else:
		return None

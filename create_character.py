from menu import menu


def choose_job():
	profession_list = ['Fighter', 'Wizard']
	profession_choice = menu('Choose a profession', profession_list, 24)
	if profession_choice is not None:
		return profession_list[profession_choice]
	else:
		return None

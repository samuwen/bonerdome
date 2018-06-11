import settings

from menu import menu


def choose_job():
	profession_list = ['Fighter', 'Wizard']
	profession_choice = menu('Choose a profession', profession_list, 24)
	settings.profession_choice = profession_list[profession_choice]

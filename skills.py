import settings

from message import message


def smash(obj):
	# need to have it so that this prompts the player to input a direction
	target = None
	if target is not None:
		message("The enemy hath been smashed")


def bash(obj):
	if obj.combatant.x:
		print("bash")

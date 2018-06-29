import settings


def advance_time():
	for obj in settings.objects:
		if obj.ai:
			obj.ai.take_turn()
		if obj.combatant:
			for ability in obj.combatant.abilities:
				ability.advance_cooldown_timer()

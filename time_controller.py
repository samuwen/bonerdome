import settings


def advance_time():
	for obj in settings.objects:
		if obj.ai:
			obj.ai.take_turn()
		if obj.combatant:
			for ability in obj.combatant.abilities:
				ability.advance_cooldown_timer()
		if obj.combatant and obj.combatant.target:
			obj.combatant.direction = obj.combatant.get_direction_to_target(obj.combatant.target)

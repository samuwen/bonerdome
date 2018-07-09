import settings


def end_player_turn():
	counter = settings.player.combatant.speed_value
	for obj in settings.objects:
		if obj.ai:
			while obj.combatant.current_speed < counter:
				obj.ai.take_turn()
				obj.combatant.current_speed += obj.combatant.speed_value
			obj.combatant.current_speed -= counter
		if obj.combatant:
			for ability in obj.combatant.abilities:
				ability.advance_cooldown_timer()
		if obj.combatant and obj.combatant.target:
			obj.combatant.direction = obj.combatant.get_direction_to_target(obj.combatant.target)
		if obj.combatant and obj.combatant.target and not obj.combatant.target.combatant:
			obj.combatant.clear_target()

import libtcodpy as tcod
import math
import settings
import utilities

from Item import Item


class Object:
	# This is a generic object class. Character, enemy, item, etc
	# Objects always have a representative character on the screen
	def __init__(self, x, y, char, name, color, blocks=False, combatant=None, ai=None, item=None,
		always_visible=False, equipment=None, direction='left'):
		self.x = x
		self.y = y
		self.char = char
		self.name = name
		self.color = color
		self.blocks = blocks
		self.always_visible = always_visible

		self.combatant = combatant
		if self.combatant:
			self.combatant.owner = self

		self.ai = ai
		if self.ai:
			self.ai.owner = self

		self.item = item
		if self.item:
			self.item.owner = self

		self.equipment = equipment
		if self.equipment:
			self.equipment.owner = self
			self.item = Item()
			self.item.owner = self

		self.direction = direction

	def move(self, dx, dy):
		if not settings.is_blocked(self.x + dx, self.y + dy):
			self.x += dx
			self.y += dy
		self.set_direction(dx, dy)

	def move_astar(self, target):
		# Create a FOV map for the actor in question
		fov = tcod.map_new(settings.MAP_WIDTH, settings.MAP_HEIGHT)

		# Scan the current map and set all walls as unwalkable
		for y1 in range(settings.MAP_HEIGHT):
			for x1 in range(settings.MAP_WIDTH):
				tcod.map_set_properties(fov, x1, y1, not settings.dungeon_map[x1][y1].block_sight,
					not settings.dungeon_map[x1][y1].blocked)

		# Scan all objects to see if anything must be navigated around
		# Check also that the object isn't self or the target (so that start and endpoints are free)
		for obj in settings.objects:
			if obj.blocks and obj != self and obj != target:
				tcod.map_set_properties(fov, obj.x, obj.y, True, False)

		# Allocating the A* path
		# The 1.41 is the normal diagonal cost of moving.
		my_path = tcod.path_new_using_map(fov, 1.41)

		tcod.path_compute(my_path, self.x, self.y, target.x, target.y)

		# Check if the path exists and is shorter than 25 tiles
		# The path size matters for the monster to use alternative longer paths (player in another room, corridor, etc)
		# If the path size is too big monsters will run weird routes around the map
		if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
			x, y = tcod.path_walk(my_path, True)
			if x or y:
				# set self's coords to the next path tile
				self.set_direction(x - self.x, y - self.y)
				self.x = x
				self.y = y
		else:
			self.move_towards(target.x, target.y)

		tcod.path_delete(my_path)

	def move_towards(self, target_x, target_y):
		dx = target_x - self.x
		dy = target_y - self.y
		distance = math.sqrt(dx ** 2 + dy ** 2)

		dx = round(dx // distance)
		dy = round(dy // distance)
		self.move(dx, dy)

	def distance_to(self, other):
		dx = other.x - self.x
		dy = other.y - self.y
		return math.sqrt(dx ** 2 + dy ** 2)

	def distance(self, x, y):
		# return the distance to some coordinates
		return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

	def send_to_back(self):
		# make this object be drawn first, so that all others will appear above it if they're in the same tile
		settings.objects.remove(self)
		settings.objects.insert(0, self)

	def draw(self):
		# Set color & draw the character that represents this object at its location
		if (tcod.map_is_in_fov(settings.fov_map, self.x, self.y) or
			(self.always_visible and settings.dungeon_map[self.x][self.y].explored)):
			tcod.console_set_default_foreground(settings.con, self.color)
			tcod.console_put_char(settings.con, self.x, self.y, self.char, tcod.BKGND_NONE)

	def clear(self):
		# erase the character that represents this object
		tcod.console_put_char(settings.con, self.x, self.y, ' ', tcod.BKGND_NONE)

	def set_direction(self, x, y):
		if x < 0 and y == 0:
			self.direction = 'left'
		elif x > 0 and y == 0:
			self.direction = 'right'
		elif y < 0 and x == 0:
			self.direction = 'up'
		elif y > 0 and x == 0:
			self.direction = 'down'
		elif x < 0 and y < 0:
			self.direction = 'up_left'
		elif x > 0 and y < 0:
			self.direction = 'up_right'
		elif x < 0 and y > 0:
			self.direction = 'down_left'
		elif x > 0 and y > 0:
			self.direction = 'down_right'
		utilities.print_debug(self.direction)

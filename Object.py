import libtcodpy as tcod
import math
import settings

from Item import Item


class Object:
	# This is a generic object class. Character, enemy, item, etc
	# Objects always have a representative character on the screen
	def __init__(self, x, y, char, name, color, blocks=False, fighter=None, ai=None, item=None,
		always_visible=False, equipment=None):
		self.x = x
		self.y = y
		self.char = char
		self.name = name
		self.color = color
		self.blocks = blocks
		self.always_visible = always_visible

		self.fighter = fighter
		if self.fighter:
			self.fighter.owner = self

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

	def move(self, dx, dy):
		if not settings.is_blocked(self.x + dx, self.y + dy):
			self.x += dx
			self.y += dy

	def move_towards(self, target_x, target_y):
		dx = target_x - self.x
		dy = target_y - self.y
		distance = math.sqrt(dx ** 2 + dy ** 2)

		dx = int(round(dx / distance))
		dy = int(round(dy / distance))
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

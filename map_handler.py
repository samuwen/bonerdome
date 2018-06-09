import libtcodpy as tcod
import settings

from place_objects import place_objects
from Item import Item
from Object import Object
from Rect import Rect
from Tile import Tile


def create_room(room):
	# go through the tiles in the rectangle and make them passable
	for x in range(room.x1 + 1, room.x2):
		for y in range(room.y1 + 1, room.y2):
			settings.dungeon_map[x][y].blocked = False
			settings.dungeon_map[x][y].block_sight = False


def create_h_tunnel(x1, x2, y):
	for x in range(min(x1, x2), max(x1, x2) + 1):
		settings.dungeon_map[x][y].blocked = False
		settings.dungeon_map[x][y].block_sight = False


def create_v_tunnel(y1, y2, x):
	for y in range(min(y1, y2), max(y1, y2) + 1):
		settings.dungeon_map[x][y].blocked = False
		settings.dungeon_map[x][y].block_sight = False


def make_map():
	settings.objects = [settings.player]
	# fill map with "unblocked" tiles
	settings.dungeon_map = [[Tile(True)
		for y in range(settings.MAP_HEIGHT)]
			for x in range(settings.MAP_WIDTH)]

	rooms = []
	num_rooms = 0

	for r in range(settings.MAX_ROOMS):
		# random width and height
		w = tcod.random_get_int(0, settings.ROOM_MIN_SIZE, settings.ROOM_MAX_SIZE)
		h = tcod.random_get_int(0, settings.ROOM_MIN_SIZE, settings.ROOM_MAX_SIZE)
		# random position contained in boundaries of the map
		x = tcod.random_get_int(0, 0, settings.MAP_WIDTH - w - 1)
		y = tcod.random_get_int(0, 0, settings.MAP_HEIGHT - h - 1)

		new_room = Rect(x, y, w, h)
		failed = False
		# run through all of the rooms to validate none intersect
		for other_room in rooms:
			if new_room.intersect(other_room):
				failed = True
				break
		if not failed:
			# paint room to the maps tiles
			create_room(new_room)

			# center coordinates of the new room
			(new_x, new_y) = new_room.center()

			if num_rooms == 0:
				# this is the first room, where the player will start
				settings.player.x = new_x
				settings.player.y = new_y
				place_stairs(new_x, new_y, '<', 'stairs up')
			else:
				# connect all subsequent rooms with tunnels

				# center coordinates of previous room
				(prev_x, prev_y) = rooms[num_rooms - 1].center()

				# get a 1 or a 0
				if tcod.random_get_int(0, 0, 1) == 1:
					# horizontal first
					create_h_tunnel(prev_x, new_x, prev_y)
					create_v_tunnel(prev_y, new_y, new_x)
				else:
					# vertical first
					create_v_tunnel(prev_y, new_y, prev_x)
					create_h_tunnel(prev_x, new_x, new_y)

			place_objects(new_room)

			rooms.append(new_room)
			num_rooms += 1

	# create stairs at the center of the last room
	if settings.dungeon_level < 20:
		place_stairs(new_x, new_y, '>', 'stairs down')
	else:
		item_component = Item()
		settings.boner_dome = Object(new_x + 1, new_y, 'D', 'Dome of Boners', tcod.yellow,
			item=item_component, always_visible=True)
		settings.objects.append(settings.boner_dome)
	place_stairs(new_x, new_y, '>', 'stairs down')


# assigns and appends stairs as appropriate
def place_stairs(x, y, char, name):
	stairs = Object(x, y, char, name, tcod.white, always_visible=True)
	if stairs.char == '<':
		settings.stairs_up = stairs
	else:
		settings.stairs_down = stairs
	settings.objects.append(stairs)
	stairs.send_to_back()

class Tile:
	# a tile of the map and its properties
	def __init__(self, blocked, block_sight=None):
		self.blocked = blocked

		# by default if a tile is blocked, it also blocks sight
		block_sight = blocked if block_sight is None else None
		self.block_sight = block_sight
		self.explored = True

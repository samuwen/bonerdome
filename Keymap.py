class Keymap:
	def __init__(self):
		self.keymap = {}

	def populate_keymap(self):
		f = open('keys.txt', 'r')
		for line in f:
			key_list = line.split(',')
			self.keymap[key_list[0]] = key_list[1]
		f.close()

	def set_keybinding(self, old_key, new_key):
		with open('keys.txt', 'r') as file:
			data = file.readlines()
			for indx, val in enumerate(data):
				current_key = val.split(',')
				if current_key[0] == old_key:
					data[indx] = new_key + "," + current_key[1]
		file.close()
		with open('keys.txt', 'w') as file:
			file.writelines(data)
		file.close()

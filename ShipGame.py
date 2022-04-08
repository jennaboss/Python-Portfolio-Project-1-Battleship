# Author: Jenna Boss
# GitHub username: jennaboss
# Date: 3/11/2022
# Description: allows two people to play the game Battleship. Each player has their own 10x10 grid they place their
# ships on. On their turn, they can fire a torpedo at a square on the enemy's grid. Player 'first' gets the first turn
# to fire a torpedo, after which players alternate firing torpedoes. A ship is sunk when all of its squares have been
# hit. When a player sinks their opponent's final ship, they win.


class Ship:
	"""
	Represents a ship in a game of Battleship.
	"""
	def __init__(self):
		"""takes no parameters, sets all data members to their initial values"""
		self._occupied_squares = []
		self._hit_squares = []

	def get_occupied_squares(self):
		"""gets a Ship's occupied squares"""
		return self._occupied_squares

	def set_occupied_squares(self, list_of_values):
		"""sets a Ship's occupied squares to given values"""
		self._occupied_squares = list_of_values

	def get_hit_squares(self):
		"""gets a Ship's squares hit by a torpedo"""
		return self._hit_squares

	def set_hit_square(self, hit_square):
		"""sets a Ship's square to hit"""
		self._hit_squares.append(hit_square)

	def is_sunk(self):
		"""determines if a particular Ship has had all squares hit and returns True if so"""
		if self._occupied_squares == self._hit_squares:
			return True


class ShipGame:
	"""
	Represents a game of Battleship.
	"""

	def __init__(self):
		"""takes no parameters, sets all data members to their initial values"""
		self._first_player_ship_objs = []  # stores ship objects on first player board
		self._second_player_ship_objs = []  # stores ship objects on second player board
		self._active_player = 'first'
		self._rows = 'ABCDEFGHIJ'

	def place_ship(self, player, ship_length, ship_coord, ship_orientation):
		"""
		:param player: either 'first' or 'second'
		:param ship_length: number of spaces ship occupies
		:param ship_coord: the coordinates of the square it will occupy that is closest to A1
		:param ship_orientation: 'R' if its squares occupy the same row, or 'C' if its squares occupy the same column
		:return:
		"""
		row_letter = ship_coord[0]
		column_number = ship_coord[1]
		new_ship_squares = []
		if ship_orientation == 'C':
			if self._rows.index(row_letter) + ship_length > 10:  # out of range of board
				return False
			for i in range(ship_length):
				# finds index of row_letter, increments, then returns to letter before attaching column_number
				new_ship_squares.append(self._rows[self._rows.index(row_letter) + i] + column_number)
		else:
			if int(column_number) + ship_length > 11:  # out of range of board
				return False
			for i in range(ship_length):
				column_number = int(column_number)
				column_number += i
				new_ship_squares.append(row_letter + str(column_number))

		for new_square in new_ship_squares:
			if player == 'first':
				for ship in self._first_player_ship_objs:
					for square in ship.get_occupied_squares():
						if square == new_square:  # square already occupied
							return False
			else:
				for ship in self._second_player_ship_objs:
					for square in ship.get_occupied_squares():
						if square == new_square:  # square already occupied
							return False
		if ship_length < 2:  # ship too short
			return False
		else:
			# creates new ship after passing all requirements
			new_ship = Ship()
			new_ship.set_occupied_squares(new_ship_squares)
			if player == 'first':
				self._first_player_ship_objs.append(new_ship)
			else:
				self._second_player_ship_objs.append(new_ship)
			return True

	def get_current_state(self):
		"""returns the current state of the game: either 'FIRST_WON', 'SECOND_WON', or 'UNFINISHED'."""
		# can assume both players will place at least one ship
		if self._first_player_ship_objs == []:
			return 'UNFINISHED'
		elif self._second_player_ship_objs == []:
			return 'UNFINISHED'
		else:
			# both players have placed ships, so we check if any have been reduced to 0 ships remaining
			if self.get_num_ships_remaining('first') == 0:
				return 'SECOND_WON'
			if self.get_num_ships_remaining('second') == 0:
				return 'FIRST_WON'
			return 'UNFINISHED'

	def fire_torpedo(self, firing_player, target_coord):
		"""
		fires torpedo from one player to another player's board.

		:param firing_player: player firing the torpedo (either 'first' or 'second')
		:param target_coord: the coordinates of the target square, e.g. 'B7'.
		:return: True (allowed to fire) or False (not allowed to fire)
		"""
		if firing_player != self._active_player:  # wrong player firing
			return False
		if self.get_current_state() != 'UNFINISHED':  # if the game is not unfinished, a player has already won
			return False
		if self._active_player == 'first':
			for ship in self._second_player_ship_objs:
				for square in ship.get_occupied_squares():
					if target_coord == square:  # detects if a square in one of the ships is the same as the target
						ship.set_hit_square(target_coord)
			self._active_player = 'second'  # switches players
		else:
			for ship in self._first_player_ship_objs:
				for square in ship.get_occupied_squares():
					if target_coord == square:  # detects if a square in one of the ships is the same as the target
						ship.set_hit_square(target_coord)
			self._active_player = 'first'  # switches players
		return True

	def get_num_ships_remaining(self, player):
		"""
		counts the number of ships remaining for a particular player

		:param player: either "first" or "second"
		:return: how many ships the specified player has left
		"""

		if player == 'first':
			ships_remaining = len(self._first_player_ship_objs)  # number of ships for first player
			for ship in self._first_player_ship_objs:
				if ship.is_sunk() is True:  # if a ship is sunk, decrease ships remaining by 1
					ships_remaining -= 1
		else:
			ships_remaining = len(self._second_player_ship_objs)  # number of ships for second player
			for ship in self._second_player_ship_objs:
				if ship.is_sunk() is True:  # if a ship is sunk, decrease ships remaining by 1
					ships_remaining -= 1
		return ships_remaining



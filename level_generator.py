from os import listdir
from os.path import isfile, join

from collision_handler import CollisionHandler
from constants import *
from sprite import *

def read_file(file):
	"""Returns the content of a file"""
	with open(file, 'r') as f:
		file_content = f.readlines()

	return file_content

def load_player_anim():
	"""Loads the player animation from files"""
	player_anim = []

	player_files = [ 'player' + '\\' + f for f in listdir('player') if isfile(join('player', f)) ]

	for player_file in player_files:
		frame = ""
		player_lines = read_file(player_file)

		for player_line in player_lines:
			frame += player_line

		player_anim.append(frame)

	return player_anim

def load_levels():
	"""Loads all the levels and instanciates the elements, camera and player"""
	levels = []

	level_files = [ 'levels' + '\\' + f for f in listdir('levels') if isfile(join('levels', f)) ]

	player_anim = load_player_anim()
	collision_handler = CollisionHandler()
	
	for level_file in level_files:
		level = []

		with open(level_file, 'r') as f:
			level_lines = f.readlines()

		x = 0
		y = 0
		size = 0

		for level_line in  level_lines:
			level_line = level_line.rstrip("\n")

			if size == 0:
				size = len(level_line)

			for char in level_line:
				if char == "+":
					level.append(Block(DARK_BLUE, (x, y)))

				if char == 'W':
					level.append(Spike(WHITE, (x, y)))

				if char == "P":
					player = Player(player_anim, BLACK, (x, y), collision_handler)

				x += SIZE
			y += SIZE
			x = 0

		levels.append((player, level, size))

	return levels
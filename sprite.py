import pygame

from pygame.locals import *

from constants import *
from util import draw

spike = """
--+---+---+---+-
--+---+---+---+-
--+---+---+---+-
--+---+---+---+-
-+++-+++-+++-+++
-+++-+++-+++-+++
-+++-+++-+++-+++
-+++-+++-+++-+++
-+++-+++-+++-+++
-+++-+++-+++-+++
-+++-+++-+++-+++
-+++-+++-+++-+++
++++++++++++++++
++++++++++++++++
++++++++++++++++
++++++++++++++++
"""

class Sprite(pygame.sprite.Sprite):
	"""Base class for all sprites in the game"""
	def __init__(self, image, color, pos, is_harmful=False):
		"""Ctor"""
		pygame.sprite.Sprite.__init__(self)
		
		self.image = image
		self.rect = image.get_rect(topleft = pos)
		self.starting_pos = pos
		self.position = Rect(self.rect[0]*100, self.rect[1]*100, self.rect[2]*100, self.rect[3]*100)
		self.__harmful = is_harmful

	def set_pos(self, x, y):
		"""Manually sets the position of a sprite"""
		self.position.x = x * 100
		self.position.y = y * 100

	def move(self, dx, dy):
		"""Moves a sprite by a certain x, y distance"""
		self.position.move_ip(dx * 100, dy * 100)

	def update_rect(self):
		"""Updates the rect object of a sprite"""
		self.rect.top = self.position.top/100
		self.rect.left = self.position.left/100

	@property
	def is_harmful(self):
		"""Returns whether a sprite is harmful of not"""
		return self.__harmful 

	def reset(self):
		"""Resets the position of a sprite to its starting position"""
		x = self.starting_pos[0]
		y = self.starting_pos[1]
		self.set_pos(x, y)
		self.update_rect()

class Block(Sprite):
	"""A Block Sprite"""
	def __init__(self, color, pos):
		"""Ctor"""
		Sprite.__init__(self, draw([SIZE, SIZE], None, color), color, pos)

class Spike(Sprite):
	"""A spike Sprite"""
	def __init__(self, color, pos):
		"""Ctor"""
		Sprite.__init__(self, draw([SIZE, SIZE], spike, color), color, pos, True)

class Player(Sprite):
	"""The player's sprite"""
	def __init__(self, images, color, pos, collision_handler=None):
		"""Ctor"""
		Sprite.__init__(self, draw([SIZE, SIZE], images[0], color), color, pos)

		self.collision_handler = collision_handler

		self.alive = True
		self.frame_count = len(images)
		self.frame = 0
		self.vertical_speed = MOVE_DISTANCE
		self.horizontal_speed = 0
		self.__jumping = False

		r_images = []
		l_images = []
		self.images = {RIGHT : r_images, LEFT : l_images}
		self.collision_group = None

		# We must have left and right images
		for image in images:
			img = draw([SIZE, SIZE], image, color)
			r_images.append(img)
			l_images.append(pygame.transform.flip(img, 1, 0))

	def set_direction(self, direction):
		"""Sets in which direction is the player looking at"""
		if direction == STAND:
			self.horizontal_speed = 0
		elif direction == RIGHT:
			self.horizontal_speed = MOVE_DISTANCE
		else:
			self.horizontal_speed = -MOVE_DISTANCE

	def set_collision_group(self, group):
		"""Sets the collision group of the player"""
		self.collision_group = group

	def jump(self):
		"""Makes the player jump if it wasn't already jumping"""
		if not self.__jumping and self.vertical_speed == MOVE_DISTANCE:
			self.vertical_speed = -1
			self.__jumping = True

	def reset(self):
		"""Resets the position and revive"""
		Sprite.reset(self)
		self.alive = True

	def update(self):
		""""Updates the player's position"""
		if self.horizontal_speed == 0:
			self.frame = 0
		else:
			self.frame +=1

		dx = self.horizontal_speed
		dy = self.vertical_speed

		if self.__jumping:
			if self.vertical_speed <= -MOVE_DISTANCE:
				self.vertical_speed += 1
				self.__jumping = False
			else:
				self.vertical_speed -= 1
		else:
			if self.vertical_speed >= MOVE_DISTANCE:
				self.vertical_speed = MOVE_DISTANCE
			else:
				self.vertical_speed += 1

		self.move(dx, dy)
		self.update_rect()
		self.collision_handler.handle_collisions(self, dx)
		self.update_rect()

		if self.horizontal_speed < 0:
			images = self.images[LEFT]
		else:
			images = self.images[RIGHT]

		index = self.frame % self.frame_count
		self.image = images[index]
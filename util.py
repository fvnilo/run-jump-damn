import pygame

from constants import *

def draw(size, pixels, color):
	image = pygame.Surface(size, pygame.SRCALPHA, 32)
	image = image.convert_alpha()
	image.set_colorkey(WHITE)

	if not pixels:
		image.fill(color)
	else:
		x=0
		y=0
		for line in pixels.split("\n"):
			for char in line:
				if char == "+":
					image.fill(color, (x, y, 1, 1))
				x += 1

			y += 1
			x = 0

	return image
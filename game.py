import pygame, sys, os
import pygame._view
import level_generator

from camera import Camera
from pygame.locals import *
from constants import *

def get_level(number, levels, screen):
	"""Loads the levels of the game, the camera and player"""
	player = levels[number][0]
	level_group = pygame.sprite.Group()

	level_elements = levels[number][1]

	for element in level_elements:
		level_group.add(element)

	player.set_collision_group(level_group)

	size =  levels[number][2] * SIZE

	camera = Camera(player, level_group, screen, size)

	return player, camera


def main():
	if sys.platform in ("win32", "win64"):
		os.environ["SDL_VIDEO_CENTERED"] = "1"

	pygame.init()
	pygame.display.set_caption("Run, Jump, Damn !")
	pygame.mouse.set_visible(0)
	screen = pygame.display.set_mode((320, 240))

	clock = pygame.time.Clock()

	levels = level_generator.load_levels()
	level_number = 0

	player, camera = get_level(level_number, levels, screen)

	while 1: # main game loop
		if camera.is_level_finished():
			level_number += 1
			player, camera = get_level(level_number, levels, screen)
			continue

		if not player.alive:
			player.reset()
			camera.reset()

		events = pygame.event.get()

		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_RIGHT:
					player.set_direction(RIGHT)
				if event.key == K_LEFT:
					player.set_direction(LEFT)
				if event.key == K_SPACE:
					player.jump()
			if event.type == KEYUP and (event.key == K_LEFT or event.key == K_RIGHT):
				player.set_direction(STAND)

		player.update()
		player.update_rect()
		camera.update()

		screen.fill(LIGHT_BLUE)

		camera.draw()

		clock.tick(24)
		pygame.display.flip()

if __name__ == "__main__":
	main()
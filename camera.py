from constants import STANDARD_SCROLL

class Camera:
	"""
	This class represents what we see in the game.

	It handles the camera scrolling aswell as if the level is finished or not.
	"""

	def __init__(self, sprite_to_focus, level_group, screen, level_size):
		"""Ctor"""
		self.sprite = sprite_to_focus
		self.level_group = level_group
		self.screen = screen
		self.level_scroll = 0
		self.level_size = level_size
		self.max_scroll = level_size - screen.get_width()

	def update(self):
		"""Updates the view by scrolling forward if necessary or resetting the view if the player is off screen"""

		# Reset the view if the player is off screen
		if self.sprite.rect.bottom > self.screen.get_height():
			self.reset()
			return

		# We will scroll forward if the player is at the center of the screen
		if self.sprite.rect.centerx >= self.screen.get_width()/2:
			if self.level_scroll <= self.max_scroll:

				# We need to check if we should scroll the standard distance or what is left
				diff = self.max_scroll-self.level_scroll

				if diff >= STANDARD_SCROLL:
					scroll = STANDARD_SCROLL
				else:
					scroll = diff
				
				self.level_scroll += scroll
				self.sprite.move(-scroll/2, 0) # The player itself will be scrolled half of the scroll
				self.sprite.update_rect()

				for sprite in self.level_group:
					sprite.move(-scroll, 0)
					sprite.update_rect()

	def draw(self):
		"""Draws the level and the player on the screen"""
		self.level_group.draw(self.screen)
		self.screen.blit(self.sprite.image, self.sprite.rect)

	def reset(self):
		"""Resets the view"""
		self.level_scroll = 0

		for sprite in self.level_group:
			sprite.reset()

		self.sprite.reset()

	def is_level_finished(self):
		"""Returns whether the level is finished or not"""
		return self.sprite.rect.right >= self.screen.get_width()
from constants import MOVE_DISTANCE

class CollisionHandler(object):
	"""This class handles the collissions between the players and the level elements"""

	def on_top(self, character, sprite):
		"""Checks whether the character is on top of an element or not"""
		diff_top = character.rect.bottom-sprite.rect.top
		return diff_top <= MOVE_DISTANCE and diff_top >= 0

	def on_left(self, character, sprite):
		"""At the left of an element but not on top."""
		diff = character.rect.right-sprite.rect.left
		return diff > 0 and not self.on_top(character, sprite)

	def on_right(self, character, sprite):
		"""At the right of an element but not on top."""
		diff = sprite.rect.right-character.rect.left
		return diff > 0 and not self.on_top(character, sprite)

	def handle_collisions(self, character, dx):
		"""Adjusts the player's position according to occuring collisions"""
		for spr in character.collision_group:
			if spr.position.colliderect(character.position):
				# Adjust bottom position of the character
				if self.on_top(character, spr):
					character.position.bottom = spr.position.top

				# Adjust side position to not go through blocks
				if dx > 0 and self.on_left(character, spr):
					character.position.right = spr.position.left
				elif dx < 0 and self.on_right(character, spr):
					character.position.left = spr.position.right

				# Kill the character if element was harmful
				if spr.is_harmful:
					character.alive = False

		# Avoid player to get off screen to the left
		if character.position.left < 0:
			character.position.left = 0
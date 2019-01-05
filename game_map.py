import pygame
from pygame.locals import *

import numpy as np

class GameMap:

	def __init__(self, gconv, map_fn):
		self.gconv = gconv
		self.game_map = map_fn # Temporary, to add
	
		wall_left = Platform(self.gconv, 1, 40, (-0.9, 40), (255, 0, 125))
		wall_right = Platform(self.gconv, 1, 40, (self.gconv.W*self.gconv.mpp-0.1, 40), (255, 0, 125))
		plat1 = Platform(self.gconv, 1.15, 0.1, (0.1, 0.1), (255, 165, 0))
		plat2 = Platform(self.gconv, self.gconv.W*self.gconv.mpp-1.25-0.1, 0.5, (1.25, 0.5), (255, 165, 0))
		self.platforms = [wall_left, wall_right, plat1, plat2]
		
	def draw_self(self, screen):
		for plat in self.platforms:
			plat.draw_self(screen)

	# Returns a numpy array of possible floor values
	def get_floor_height(self, x_vec):
		h = np.zeros(1)
		x = x_vec[0]
		if (0.1 <= x < 1.25):
			h[0] = 0.1
		elif (1.25 <= x < self.gconv.W*self.gconv.mpp-0.1):
			h[0] = 0.5
		else: # Big walls on edges of screen
			h[0] = 40

		return h


# Individual platform object (floors count too)
class Platform:

	def __init__(self, gconv, w, h, topleftpos, color):
		self.gconv = gconv
		self.w = w
		self.h = h
		self.color = color

		self.surf = pygame.Surface((w*self.gconv.ppm, h*self.gconv.ppm))
		self.surf.fill(color)
		self.rect = self.surf.get_rect()
		self.rect.topleft = self.gconv.l2s(topleftpos)
	
	def draw_self(self, screen):
		screen.blit(self.surf, self.rect)

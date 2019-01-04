import pygame
from pygame.locals import *

import numpy as np

class GameMap:

	def __init__(self, gconv, map_fn):
		self.gconv = gconv
		self.game_map = map_fn # Temporary, to add
		self.floor1_surf = pygame.Surface((1.25*self.gconv.ppm, 0.1*self.gconv.ppm))
		self.floor1_surf.fill((255, 165, 0))
		self.floor1_rect = self.floor1_surf.get_rect()
		self.floor1_rect.topleft = self.gconv.l2s([0, 0.1])
	
		self.floor2_surf = pygame.Surface(((5-1.25)*self.gconv.ppm, 0.5*self.gconv.ppm))
		self.floor2_surf.fill((255, 165, 0))
		self.floor2_rect = self.floor2_surf.get_rect()
		self.floor2_rect.topleft = self.gconv.l2s([1.25, 0.5])
	
	def draw_self(self, screen):
		screen.blit(self.floor1_surf, self.floor1_rect)
		screen.blit(self.floor2_surf, self.floor2_rect)

	# Returns a numpy array of possible floor values
	def get_floor_height(self, x_vec):
		h = np.zeros(1)
		x = x_vec[0]
		if (-100 <= x < 0):
			h[0] = 0.1
		elif (0 <= x < 1.25):
			h[0] = 0.1
		elif (1.25 <= x <= 5):
			h[0] = 0.5

		return h

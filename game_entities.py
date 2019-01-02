import pygame
from pygame.locals import *

import numpy as np
from math import *

class Jumper(pygame.sprite.Sprite):

	def __init__(self, W, H, position, floor=0.05, velocity=[0,0]):
		super(Jumper, self).__init__()

		# Window information
		self.W = W
		self.H = H
		self.ppm = 300 # Pixels per meter
		self.mpp = 1/self.ppm # Meters per pixel
		self.floor = 0

		# Setup the surface for the head
		self.head_surf = pygame.Surface((35, 35))
		self.head_surf.fill((255, 0, 255))
		self.head_rect = self.head_surf.get_rect()
		self.head_rect.center = position

		# Setup the surface for the upper portion of the body
		self.ub_len = 0.5 # Upper body length
		self.ub_ar = 0.2 # Aspect ratio for upper body linkage
		self.ub_base_surf = pygame.Surface((self.ub_len*self.ppm, self.ub_ar*self.ub_len*self.ppm), pygame.SRCALPHA)
		self.ub_base_surf.fill((255, 255, 255))
		self.make_ub_surf(0)
		self.ub_rect.center = position

		# Setup the surface for the lower portion of the body
		self.lb_len = 0.5 # Upper body length
		self.lb_ar = 0.2 # Aspect ratio for upper body linkage
		self.lb_base_surf = pygame.Surface((self.lb_len*self.ppm, self.lb_ar*self.lb_len*self.ppm), pygame.SRCALPHA)
		self.lb_base_surf.fill((50, 255, 50))
		self.make_lb_surf(0)		
		self.lb_rect.center = position

		# Physics parameters
		self.k = 900 # N/m
		self.b = 0.5 # Damping coefficient
		self.m = 2 # Mass (kg)
		self.g = 40 # Acceleration due to gravity
		self.s0 = 0.7 # Resting length of spring
		self.sc = 0.2 # Solid length of spring
		self.sm = 1.2 # Maximum length of spring
		self.s = self.s0 # Current length of spring

		self.x = np.array(self.s2l(position)) # Position vector
		self.v = np.array(velocity) # Velocity vector
		self.a = np.array([0, -self.g]) # Accleration vector

	# Draw each element of the jumper
	def draw_self(self, screen):
		screen.blit(self.head_surf, self.head_rect)
		screen.blit(self.ub_surf, self.ub_rect)
		screen.blit(self.lb_surf, self.lb_rect)
	
	def update(self, pressed_keys, dt):
		# Check for user input and do physics stuff
		spring_force = 0
		if (self.x[1] - self.floor < self.s0):
			self.s = self.x[1] - self.floor
			spring_force = self.k*(self.s0-self.s) - self.b*self.v[1]
		else:
			self.s = self.s0

		self.a = np.array([0, -self.g + spring_force/self.m])
		self.x = self.x + self.v*dt + self.a*dt*dt/2 # Update position 
		self.v = self.v + 0.5*self.a*dt # Update velocity

		# Velocity Verlet term
		spring_force = 0
		if (self.x[1] - self.floor < self.s0):
			temp_s = self.x[1] - self.floor
			spring_force = self.k*(self.s0-temp_s) - self.b*self.v[1]
		temp_a = np.array([0, -self.g + spring_force/self.m])
		self.v = self.v + 0.5*temp_a*dt

		self.head_rect.center = self.l2s(self.x.tolist())		
	
		self.update_body_surfs(self.x, self.s)

	# Update the surfaces of the body linkages
	def update_body_surfs(self, head_pos, b_len):
		# Find required angles of the lower and upper bodies
		#	self.ub_len*cos(a_ub) = self.lb_len*cos(a_lb)
		#	self.ub_len*sin(a_ub) + self.lb_len*sin(a_lb) = b_len
	
		# For now, restrict calculation to identical lower and upper body lengths
		ang = np.arcsin(b_len/(2*self.ub_len))
		self.make_ub_surf(ang);
		self.ub_rect.center = self.l2s(head_pos + np.array([-self.ub_len*np.cos(ang)/2, -self.ub_len*np.sin(ang)/2]))
		self.make_lb_surf(-ang)
		self.lb_rect.center = self.l2s(head_pos + np.array([-self.lb_len*np.cos(ang)/2, -b_len+self.lb_len*np.sin(ang)/2]))
	
	# Make a rotated upper body surf
	def make_ub_surf(self, ang):
		self.ub_surf = pygame.transform.rotate(self.ub_base_surf, np.rad2deg(ang))
		self.ub_rect = self.ub_surf.get_rect()
	
	# Make a rotated lower body surf
	def make_lb_surf(self, ang):
		self.lb_surf = pygame.transform.rotate(self.lb_base_surf, np.rad2deg(ang))
		self.lb_rect = self.lb_surf.get_rect()

	# Changes local coordinates to screen coordinates
	def l2s(self, x):
		px = x[0] * self.ppm
		py = self.H - x[1] * self.ppm
		
		return [px, py]

	# Changes screen coordinates to local coordinates
	def s2l(self, position):
		px = position[0] * self.mpp
		py = (self.H - position[1])*self.mpp
		
		return [px, py]

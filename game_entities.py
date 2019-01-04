import pygame
from pygame.locals import *

import numpy as np
from math import *

class Jumper(pygame.sprite.Sprite):

	def __init__(self, gconv, position, game_map, velocity=[0,0]):
		super(Jumper, self).__init__()

		# Window information
		self.gconv = gconv
		self.game_map = game_map
		self.floor = 0

		# Setup the surface for the head
		self.head_surf = pygame.Surface((35, 35))
		self.head_surf.fill((255, 0, 255))
		self.head_rect = self.head_surf.get_rect()
		self.head_rect.center = position

		# Setup the surface for the upper portion of the body
		self.ub_len = 0.5 # Upper body length
		self.ub_ar = 0.2 # Aspect ratio for upper body linkage
		self.ub_base_surf = pygame.Surface((self.ub_len*self.gconv.ppm, self.ub_ar*self.ub_len*self.gconv.ppm), pygame.SRCALPHA)
		self.ub_base_surf.fill((255, 255, 255))
		self.make_ub_surf(0)
		self.ub_rect.center = position

		# Setup the surface for the lower portion of the body
		self.lb_len = 0.5 # Upper body length
		self.lb_ar = 0.2 # Aspect ratio for upper body linkage
		self.lb_base_surf = pygame.Surface((self.lb_len*self.gconv.ppm, self.lb_ar*self.lb_len*self.gconv.ppm), pygame.SRCALPHA)
		self.lb_base_surf.fill((50, 255, 50))
		self.make_lb_surf(0)		
		self.lb_rect.center = position

		# Physics parameters
		self.k = 900 # N/m
		self.b = np.array([20, 0])  # Damping coefficient
		self.m = 2 # Mass (kg)
		self.g = 40 # Acceleration due to gravity
		self.lat_accel = 200 # Maximum lateral acceleration
		self.s0 = 0.7 # Resting length of spring
		self.sc = 0.2 # Solid length of spring
		self.sm = 1.2 # Maximum length of spring
		self.s = self.s0 # Current length of spring

		self.x = np.array(self.gconv.s2l(position)) # Position vector
		self.v = np.array(velocity) # Velocity vector
		self.a = np.array([0, -self.g]) # Accleration vector

	# Draw each element of the jumper
	def draw_self(self, screen):
		screen.blit(self.head_surf, self.head_rect)
		screen.blit(self.ub_surf, self.ub_rect)
		screen.blit(self.lb_surf, self.lb_rect)
	
	def update(self, pressed_keys, dt):
		has_velocity = False
		self.a = np.array([0, 0])
		# Check for user input
		if pressed_keys[K_LEFT]:
			has_velocity = True
			self.a[0] = -self.lat_accel
		if pressed_keys[K_RIGHT]:
			has_velocity = True	
			self.a[0] = self.lat_accel

		# Do physics integration
		spring_force = 0
		floor_h = self.game_map.get_floor_height(self.x)
		floor_h = floor_h[0]
		if (self.x[1] - floor_h  < self.s0):
			self.s = self.x[1] - floor_h
			spring_force = self.k*(self.s0-self.s)
		else:
			self.s = self.s0

		temp_a = self.a + np.array([0, -self.g + spring_force/self.m]) - self.b*self.v
		temp_x = self.x + self.v*dt + temp_a*dt*dt/2 # Update position 
		temp_v = self.v + 0.5*temp_a*dt # Update velocity
	
		# Check for sideways collisions with walls before moving
		temp_floor_h = self.game_map.get_floor_height(temp_x)
		temp_floor_h = temp_floor_h[0]
		if (temp_floor_h == floor_h or (temp_floor_h != floor_h and self.x[1] - temp_floor_h >= self.s0)):
			self.a = temp_a
			self.x = temp_x
			self.v = temp_v
			floor_h = temp_floor_h
		else:
			x_t = self.x[0] # Store previous x value
			self.a = temp_a
			self.a[0] = 0
			self.x = temp_x
			self.x[0] = x_t
			self.v = temp_v
			self.v[0] = 0

		# Half timestep Velocity Verlet term
		spring_force = 0
		if (self.x[1] - floor_h < self.s0):
			temp_s = self.x[1] - floor_h
			spring_force = self.k*(self.s0-temp_s)
		temp_a = np.array([0, -self.g + spring_force/self.m]) - self.b*self.v
		self.v = self.v + 0.5*temp_a*dt

		self.head_rect.center = self.gconv.l2s(self.x.tolist())		
	
		self.update_body_surfs(self.x, self.s)

	# Update the surfaces of the body linkages
	def update_body_surfs(self, head_pos, b_len):
		# Find required angles of the lower and upper bodies
		#	self.ub_len*cos(a_ub) = self.lb_len*cos(a_lb)
		#	self.ub_len*sin(a_ub) + self.lb_len*sin(a_lb) = b_len
	
		# For now, restrict calculation to identical lower and upper body lengths
		ang = np.arcsin(b_len/(2*self.ub_len))
		self.make_ub_surf(ang);
		self.ub_rect.center = self.gconv.l2s(head_pos + np.array([-self.ub_len*np.cos(ang)/2, -self.ub_len*np.sin(ang)/2]))
		self.make_lb_surf(-ang)
		self.lb_rect.center = self.gconv.l2s(head_pos + np.array([-self.lb_len*np.cos(ang)/2, -b_len+self.lb_len*np.sin(ang)/2]))
	
	# Make a rotated upper body surf
	def make_ub_surf(self, ang):
		self.ub_surf = pygame.transform.rotate(self.ub_base_surf, np.rad2deg(ang))
		self.ub_rect = self.ub_surf.get_rect()
	
	# Make a rotated lower body surf
	def make_lb_surf(self, ang):
		self.lb_surf = pygame.transform.rotate(self.lb_base_surf, np.rad2deg(ang))
		self.lb_rect = self.lb_surf.get_rect()

import pygame
from pygame.locals import *
from game_entities import *
from game_map import *
from game_conversion_utils import *

# Setup the window
pygame.init()
W=800; H=600
screen = pygame.display.set_mode((W, H))
background = pygame.Surface(screen.get_size())
background.fill((0,0,0))
clock = pygame.time.Clock()
FPS = 60
dt = 0.01

# Initialize game objects
gconv = GameConversionUtils(W, H, 300)
game_map = GameMap(gconv, "Temp")
jumper = Jumper(gconv, [int(W/2), int(H/5)], game_map)

running = True

while running:
	# Loop through event queue
	for event in pygame.event.get():
		# Check for KEYDOWN
		if event.type == KEYDOWN:
			# If escape is pressed, exit game
			if event.key == K_ESCAPE:
				running = False
		elif event.type == QUIT:
			running = False

	screen.blit(background, (0, 0)) # Redraw a blank screen
	pressed_keys = pygame.key.get_pressed()
	jumper.update(pressed_keys, dt)
	
	# Draw the player
	game_map.draw_self(screen)
	jumper.draw_self(screen)
	
	# Update the display
	pygame.display.flip()
	clock.tick(FPS)

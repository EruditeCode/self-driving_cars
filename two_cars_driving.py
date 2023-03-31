# Program to explore an autonomous car driving round a track.

# Video Walkthrough Link: XXXX

import pygame
from collections import deque
from race_track_barriers import barriers
from improved_car import Car

# Reorganise the boundary data as walls.
walls = []
for barrier in barriers:
	for i in range(len(barrier)):
		walls.append([barrier[i-1], barrier[i]])

# The main program function.
def main():
	pygame.init()
	WIDTH, HEIGHT = 900, 600
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	clock = pygame.time.Clock()

	bg = pygame.image.load('race_track.png')
	bg = pygame.transform.scale(bg, (900, 600))

	# Loading car image and initialising the car object.
	CAR_IMAGE = pygame.image.load('car.png')
	CAR_IMAGE = pygame.transform.scale(CAR_IMAGE, (42, 20))
	car1 = Car((350, 250), 115, 2, 6)
	car1.update(walls)
	CAR_2_IMAGE = pygame.image.load('car_2.png')
	CAR_2_IMAGE = pygame.transform.scale(CAR_2_IMAGE, (42, 20))
	car2 = Car((80, 150), 270, 2, 6)
	car2.update(walls)

	car_barriers, car_barriers_2 = [], []

	drive = False
	show_struct = False
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					drive = not drive
				if event.button == 3:
					show_struct = not show_struct

		if drive:
			car1.update(walls+car_barriers_2)
			car2.update(walls+car_barriers, car1.pos)
		car_barriers, car_barriers_2 = [], []

		# Displaying the background surface.
		screen.blit(bg, (0, 0))

		# Toggle for showing the rays from the car and the barriers on the map.
		if show_struct:
			for ray in car1.rays:
				pygame.draw.aaline(screen, (255,0,0), ray.pos, ray.terminus)

			for barrier in barriers:
				for i in range(0, len(barrier)):
					pygame.draw.line(screen, (255,255,255), barrier[i-1], barrier[i], 3)

		# Rotating and displaying the car object.
		car_temp = pygame.transform.rotate(CAR_IMAGE, -car1.dir)
		car_rect = car_temp.get_rect()
		car_rect.center = car1.pos
		screen.blit(car_temp, car_rect)
		car_barriers.extend([[car_rect.topleft, car_rect.topright], [car_rect.topright, car_rect.bottomright], [car_rect.bottomleft, car_rect.bottomright], [car_rect.topleft, car_rect.bottomleft]])

		car_2_temp = pygame.transform.rotate(CAR_2_IMAGE, -car2.dir)
		car_2_rect = car_2_temp.get_rect()
		car_2_rect.center = car2.pos
		screen.blit(car_2_temp, car_2_rect)
		car_barriers_2.extend([[car_2_rect.topleft, car_2_rect.topright], [car_2_rect.topright, car_2_rect.bottomright], [car_2_rect.bottomleft, car_2_rect.bottomright], [car_2_rect.topleft, car_2_rect.bottomleft]])

		pygame.display.update()
		clock.tick(60)


if __name__ == '__main__':
	main()

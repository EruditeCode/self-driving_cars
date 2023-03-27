# Program to explore an autonomous car driving round an ellipse.

# Video Walkthrough Link: https://www.youtube.com/watch?v=NbKCmxzS05k&feature=youtu.be

import pygame
from ellipse_path import path, inner, outer
from basic_car import Car

# Reorganise the boundary data as walls.
walls = []
for i in range(len(inner)):
	walls.append([inner[i-1], inner[i]])
for i in range(len(outer)):
	walls.append([outer[i-1], outer[i]])


# The main program function.
def main():
	pygame.init()
	WIDTH, HEIGHT = 900, 600
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	clock = pygame.time.Clock()

	CAR_IMAGE = pygame.image.load('car.png')
	CAR_IMAGE = pygame.transform.scale(CAR_IMAGE, (42, 20))

	bg = pygame.Surface((WIDTH, HEIGHT))
	bg.fill((20,20,20))

	car1 = Car(path[0], 90, 2, 4)
	car1.update(walls)

	drive = False
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.MOUSEBUTTONUP:
				drive = not drive

		if drive:
			car1.update(walls)

		# Displaying the background surface.
		screen.blit(bg, (0, 0))

		# Displaying the path and boundary walls.
		for step in path:
			pygame.draw.circle(screen, (30,30,30), step, 25)
		for i in range(0, len(outer)):
			pygame.draw.line(screen, (200,200,80), outer[i-1], outer[i], 2)
		for i in range(0, len(inner)):
			pygame.draw.line(screen, (200,200,80), inner[i-1], inner[i], 2)
		for i in range(0, len(path)):
			pygame.draw.aaline(screen, (200,200,200), path[i-1], path[i])

		for ray in car1.rays:
			pygame.draw.aaline(screen, (0,255,0), ray.pos, ray.terminus)

		# Rotating and displaying the car object.
		car_temp = pygame.transform.rotate(CAR_IMAGE, -car1.dir)
		car_rect = car_temp.get_rect()
		car_rect.center = car1.pos
		screen.blit(car_temp, car_rect)
		
		pygame.display.update()
		clock.tick(60)


if __name__ == '__main__':
	main()

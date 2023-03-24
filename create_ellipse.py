# Program to draw an ellipse and enable boundries to be created for a road.

import pygame
import math
from random import randint

MAJOR_AXIS = 300
MINOR_AXIS = 140

def create_ellipse(centre):
	points = []
	for i in range(0, 360):
		radians = i * (math.pi/180)
		x = centre[0] + MAJOR_AXIS * math.cos(radians)
		y = centre[1] + MINOR_AXIS * math.sin(radians)
		points.append((x, y))
	return points

def create_track_line(centre, next_p, length):
	# Find vector to draw line perpendicular to direction to next point.
	dir_to_next = (next_p[0] - centre[0], next_p[1] - centre[1])
	dir1 = (dir_to_next[1], -dir_to_next[0])
	dir2 = (-dir_to_next[1], dir_to_next[0])

	# Normalise the vector magnitude.
	dir1_mag = (dir1[0]*dir1[0] + dir1[1]*dir1[1]) ** 0.5
	dir1 = (dir1[0] / dir1_mag, dir1[1] / dir1_mag)
	dir2_mag = (dir2[0]*dir2[0] + dir2[1]*dir2[1]) ** 0.5
	dir2 = (dir2[0] / dir2_mag, dir2[1] / dir2_mag)

	point1 = (centre[0] + dir1[0]*length, centre[1] + dir1[1]*length)
	point2 = (centre[0] + dir2[0]*length, centre[1] + dir2[1]*length)
	return [point1, point2]


# The main program function.
def main():
	pygame.init()
	WIDTH, HEIGHT = 900, 600
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	clock = pygame.time.Clock()

	bg = pygame.Surface((WIDTH, HEIGHT))
	bg.fill((20,20,20))

	outer_boundry = []
	inner_boundry = []
	path = create_ellipse((WIDTH//2, HEIGHT//2))

	build_track = False
	count = 0
	c_i = 0
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.KEYUP:
				build_track = True

		if build_track:
			if count < len(path):
				track = create_track_line(path[count-1], path[count], 25)
			else:
				track = create_track_line(path[count], path[0], 25)
			count += 1
			outer_boundry.append(track[1])
			inner_boundry.append(track[0])

			if count >= len(path):
				count = 0
				build_track = False


		# Displaying the background surface.
		screen.blit(bg, (0, 0))

		if path:
			for i in range(0, c_i):
				pygame.draw.circle(screen, (30,30,30), path[i], 25)

		if outer_boundry:
			for i in range(0, len(outer_boundry)):
				pygame.draw.line(screen, (200,200,80), outer_boundry[i-1], outer_boundry[i], 2)

		if inner_boundry:
			for i in range(0, len(inner_boundry)):
				pygame.draw.line(screen, (200,200,80), inner_boundry[i-1], inner_boundry[i], 2)

		if len(path) > 1:
			for i in range(0, c_i):
				pygame.draw.aaline(screen, (200,200,200), path[i-1], path[i])
		
		if c_i < len(path):
			c_i += 1				

		pygame.display.update()
		clock.tick(30)


if __name__ == '__main__':
	main()

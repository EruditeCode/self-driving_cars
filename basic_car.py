# A class to contain an autonomous driving car - supports driving programs.

import math
from random import randint

class Car:
	def __init__(self, position, direction, speed, max_angle):
		self.pos = position
		self.dir = direction
		self.speed = speed
		self.max_angle = max_angle

		self.rays = []
		for angle in range(-60, 70, 60):
			ray = Ray(self.pos, angle, 2000)
			self.rays.append(ray)

	def update(self, walls):
		self.update_position()
		self.update_rays(walls)
		self.update_guidance()

	def update_position(self):
		angle = self.dir * (math.pi / 180)
		x = self.pos[0] + (self.speed * math.cos(angle))
		y = self.pos[1] + (self.speed * math.sin(angle))
		self.pos = (x, y)

	def update_rays(self, walls):
		for ray in self.rays:
			ray.update(self.pos, self.dir, walls)

	def update_guidance(self):
		# Find the longest ray.
		max_distance, max_index = 0, None
		for index, ray in enumerate(self.rays):
			if ray.distance >= max_distance:
				max_distance = ray.distance
				max_index = index

		# Bias the random direction change towards the longest ray.
		if max_index == 0:
			self.dir += randint(-self.max_angle, 0)
		elif max_index == 1:
			if self.rays[0].distance > self.rays[2].distance:
				self.dir += randint(-self.max_angle, 1)
			else:
				self.dir += randint(-1, self.max_angle)
		else:
			self.dir += randint(0, self.max_angle)

	def reset(self, position, direction):
		self.pos = position
		self.dir = direction


class Ray:
	def __init__(self, position, angle, max_length):
		self.pos = position
		self.init_angle = angle
		self.length = max_length
		self.dir = None
		self.terminus = None
		self.distance = self.length

	def update(self, point, direction, walls):
		self.pos = point
		self.update_direction(direction)
		self.update_terminus(walls)

	def update_direction(self, direction):
		a = self.init_angle + direction
		angle = math.radians(a)
		self.dir = (math.cos(angle), math.sin(angle))
	
	def update_terminus(self, walls):
		# Need to get the minimum intersection distance from the group of walls.
		distance, min_terminus = self.length, None
		for wall in walls:
			x1, y1 = wall[0][0], wall[0][1]
			x2, y2 = wall[1][0], wall[1][1]
			x3, y3 = self.pos[0], self.pos[1]
			x4, y4 = self.pos[0] + self.dir[0], self.pos[1] + self.dir[1]

			divisor = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
			if divisor == 0:
				# Line segment and ray are parallel, therefore no intersection.
				continue

			t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / divisor
			u = -((x1-x2)*(y1-y3) - (y1-y2)*(x1-x3)) / divisor

			# Check that the point is between the line segment start and end point.
			# Check that the point is on the positive part of the ray (not backwards!).
			if t >= 0 and t <= 1 and u > 0:
				x_point = x1 + t * (x2 - x1)
				y_point = y1 + t * (y2 - y1)
				dist_check = math.dist(self.pos, (x_point, y_point))
				if dist_check < distance:
					distance = dist_check
					min_terminus = (x_point, y_point)

		if distance != self.length:
			self.distance = distance
			self.terminus = min_terminus
			return

		point_x = self.pos[0] + self.dir[0] * self.length
		point_y = self.pos[1] + self.dir[1] * self.length
		self.terminus = (point_x, point_y)
		self.distance = self.length

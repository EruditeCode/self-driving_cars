# A class to contain an improved autonomous driving car - supports driving programs.

import math
from random import randint

class Car:
	def __init__(self, position, direction, speed, max_angle):
		self.pos = position
		self.dir = direction
		self.speed = speed
		self.max_angle = max_angle
		self.decision_counter = 0
		self.left = (0,0)
		self.right = (0,0)

		self.rays = []
		for angle in range(-60, 70, 60):
			ray = Ray(self.pos, angle, 2000)
			self.rays.append(ray)

	def update(self, walls, track=None):
		self.update_position()
		self.update_rays(walls)
		self.update_guidance(track)

	def update_position(self):
		self.pos = self.get_position(self.dir, self.speed)

	def update_rays(self, walls):
		for ray in self.rays:
			ray.update(self.pos, self.dir, walls)

	def update_guidance(self, target):
		min_ray, max_ray = self.find_min_max_rays()
		if self.rays[min_ray].distance < 80:
			self.evasive_action(max_ray)
		else:
			self.decision_counter_check(target)
		
	def find_min_max_rays(self):
		max_distance, max_index = self.rays[0].distance, 0
		min_distance, min_index = self.rays[0].distance, 0
		for index, ray in enumerate(self.rays):
			if ray.distance >= max_distance:
				max_distance, max_index = ray.distance, index
			if ray.distance <= min_distance:
				min_distance, min_index = ray.distance, index
		return min_index, max_index

	def evasive_action(self, max_ray):
		if max_ray == 0:
			self.dir += randint(-self.max_angle, 0)
		elif max_ray == 1:
			if self.rays[0].distance > self.rays[2].distance:
				self.dir += randint(-self.max_angle, 0)
			else:
				self.dir += randint(0, self.max_angle)
		else:
			self.dir += randint(0, self.max_angle)

	def decision_counter_check(self, target):
		if self.decision_counter >= 10:
			if target:
				self.turn_towards_target(target)
			else:
				self.dir += randint(-self.max_angle, self.max_angle)
			self.decision_counter = 0
		else:
			self.decision_counter += 1

	def turn_towards_target(self, target):
		#self.get_angle_to_target
		A, B, C = self.pos, self.get_position(self.dir, self.speed), target
		AB, AC = (B[0]-A[0], B[1]-A[1]), (C[0]-A[0], C[1]-A[1])
		AB_m, AC_m = (AB[0]**2 + AB[1]**2)**0.5, (AC[0]**2 + AC[1]**2)**0.5
		temp = ((AB[0]*AC[0]) + (AB[1]*AC[1]))/(AB_m * AC_m)
		angle_to_target = math.degrees(math.acos(temp))

		# The angle can go both ways +ve or -ve.
		distance_to_target = math.dist(self.pos, target)
		left_dist = math.dist(self.get_position(self.dir-angle_to_target, distance_to_target), target)
		self.left = self.get_position(self.dir-angle_to_target, distance_to_target)
		right_dist = math.dist(self.get_position(self.dir+angle_to_target, distance_to_target), target)
		self.right = self.get_position(self.dir+angle_to_target, distance_to_target)

		if right_dist < left_dist:
			self.dir += randint(0, self.max_angle)
		else:
			self.dir += randint(-self.max_angle, 0)

	def get_position(self, base_angle, length):
		angle = base_angle * (math.pi / 180)
		x = self.pos[0] + (length * math.cos(angle))
		y = self.pos[1] + (length * math.sin(angle))
		return (x,y)

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

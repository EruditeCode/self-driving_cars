# Program to explore an autonomous car driving round a track.

# Video Walkthrough Link: https://www.youtube.com/watch?v=NbKCmxzS05k&feature=youtu.be

import pygame
from track_barriers import barriers
from basic_car import Car

# Reorganise the boundary data as walls.
walls = []
for barrier in barriers:
    for i in range(len(barrier)):
        walls.append([barrier[i - 1], barrier[i]])


# The main program function.
def main():
    pygame.init()
    WIDTH, HEIGHT = 900, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    CAR_IMAGE = pygame.image.load('car.png')
    CAR_IMAGE = pygame.transform.scale(CAR_IMAGE, (42, 20))

    bg = pygame.image.load('track.png')
    bg = pygame.transform.scale(bg, (900, 600))

    car1 = Car((100, 150), 90, 2, 5)
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

        # for ray in car1.rays:
        #     pygame.draw.aaline(screen, (0, 255, 0), ray.pos, ray.terminus)
        #
        # for barrier in barriers:
        #     for i in range(0, len(barrier)):
        #         pygame.draw.line(screen, (255, 255, 255), barrier[i - 1], barrier[i], 3)

        # Rotating and displaying the car object.
        car_temp = pygame.transform.rotate(CAR_IMAGE, -car1.dir)
        car_rect = car_temp.get_rect()
        car_rect.center = car1.pos
        screen.blit(car_temp, car_rect)

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()

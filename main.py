from sys import argv
import pygame

from idm import start_simulator
from idm import run_simulator

if len(argv) != 3:
    print("Error: Insufficient Arguments")
    print("\t Correct Usage: python main.py [vehicle width] [number of vehicles]")
    exit(1)
elif isinstance(argv[1], int) or isinstance(argv[2], int):
    print("Error: Arguments must be Integers")
    print("\t Correct Usage: python main.py [vehicle width] [number of vehicles]")
    exit(1)

pygame.init()

w = abs(int(argv[1]))

start_simulator(abs(int(argv[2])))

screen = pygame.display.set_mode((1000,400))
clock = pygame.time.Clock()
running = True

t = 0


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        screen.fill("black")

        # render animation here
        vehicles = run_simulator(t)

        carnum = 0
        for car in vehicles:
            red_color = min(255, 200 * car.v/car.v0 + 20)
            if w > 10:
                pygame.draw.rect(screen, (255,0,0), (car.x, 200-1, car.L, w+2)) # border

            pygame.draw.rect(screen, (red_color, 55,55), (car.x, 200, car.L, w)) # car

            carnum += 1

        screen.blit(pygame.font.Font(None, 36).render(str(round(t, 2))+"s", True, (255,255,255)), (15, 15))

        pygame.display.flip()
        clock.tick(30)
        t += 0.1

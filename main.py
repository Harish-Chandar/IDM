import pygame

from idm import start_simulator
from idm import run_simulator

pygame.init()

screen = pygame.display.set_mode((1000,700))
clock = pygame.time.Clock()
running = True

start_simulator()
t = 0
dt = 0.1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        screen.fill("black")

        # render animation here
        vehicles = run_simulator(t, dt)

        carnum = 0
        for car in vehicles:
            print(f"Car {carnum}: Position = {car.x:.2f} m, Velocity = {car.v:.2f} m/s, Acceleration = {car.dvdt:.2f} m/s2")
            red_color = max(255, 200 * car.v/car.v0 + 50)
            pygame.draw.rect(screen, (red_color, 5,5), (car.x, 350, car.L, 2))
            carnum += 1

        pygame.display.flip()
        dt = clock.tick(30) / 1000
        t += dt

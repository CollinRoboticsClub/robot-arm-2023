import pygame
from pygame import Vector2

from arm import Arm, ArmComponent


if __name__ == "__main__":
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1600, 1000))
    pygame.display.set_caption("Robot Simulator")
    clock = pygame.time.Clock()
    running = True
    dt = 0

    bicep = ArmComponent(200, 0, (255, 0, 0))
    forearm = ArmComponent(150, 0.5 * 3.14, (0, 255, 0))
    hand = ArmComponent(100, 0.25 * 3.14, (0, 0, 255))

    arm = Arm(Vector2(*screen.get_rect().center), bicep, forearm, hand)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if the user clicks the X button
                running = False

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False

        # clear the screen
        screen.fill((10, 10, 20))

        # draw the arm
        arm.update(dt)
        arm.draw(screen)

        # update the screen
        pygame.display.flip()

        # limit the framerate to 75 FPS
        dt = clock.tick(75)

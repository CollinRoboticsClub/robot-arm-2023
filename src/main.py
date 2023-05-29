import pygame

from arm import Arm, ArmComponent


if __name__ == "__main__":
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1366, 768))
    pygame.display.set_caption("Robot Simulator")
    clock = pygame.time.Clock()
    running = True
    dt = 0

    bicep = ArmComponent(25, 0, (255, 0, 0))
    forearm = ArmComponent(25, 0, (0, 255, 0))
    hand = ArmComponent(25, 0, (0, 0, 255))

    bicep.next_component = forearm
    forearm.prev_component = bicep
    forearm.next_component = hand
    hand.prev_component = forearm

    arm = Arm(screen.get_rect().center, bicep, forearm, hand)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if the user clicks the X button
                running = False

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False

        # clear the screen
        screen.fill((0, 10, 0))

        # draw the arm
        arm.update(dt)
        arm.draw(screen)

        # update the screen
        pygame.display.flip()

        # limit the framerate to 75 FPS
        dt = clock.tick(75)

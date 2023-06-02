import pygame
from pygame import Vector2

from arm import Arm, ArmComponent


if __name__ == "__main__":
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("Robot Simulator")
    clock = pygame.time.Clock()
    running = True
    dt = 0

    # Create ArmComponents
    main_len = screen.get_width() * 0.2
    bicep_len = main_len * 0.9
    forearm_len = main_len * 0.6
    hand_len = main_len * 0.3

    bicep = ArmComponent(bicep_len, (255, 0, 0))
    forearm = ArmComponent(forearm_len, (0, 255, 0))
    hand = ArmComponent(hand_len, (0, 0, 255))

    # Create Arm
    arm = Arm(
        Vector2(*screen.get_rect().center) - Vector2(300, -200),
        bicep,
        forearm,
        hand,
    )

    font = pygame.font.SysFont("Calibri", 20)

    # main loop
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

        screen.blit(
            font.render(
                f"{arm.angle_diagnostic_text()}", True, (255, 255, 255)
            ),
            (10, 10),
        )

        # update the screen
        pygame.display.flip()

        # limit the framerate to 75 FPS
        dt = clock.tick(75)

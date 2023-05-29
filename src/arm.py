import math
import pygame
from pygame.math import Vector2


class ArmComponent:
    """
    Represents a component of an arm, such as the bicep, forearm, or hand.
    """

    def __init__(self, length=0.0, angleToGroundRadians=0.0, color=(0, 0, 0)):
        self.length = length
        self.angleToGroundRadians = angleToGroundRadians
        self.color = color

    def as_vector2(self) -> Vector2:
        return Vector2(
            self.length * math.cos(self.angleToGroundRadians),
            self.length * math.sin(self.angleToGroundRadians),
        )


class Arm:
    def __init__(
        self,
        root_pos: Vector2,
        bicep: ArmComponent,
        forearm: ArmComponent,
        hand: ArmComponent,
    ):
        self.root_pos = root_pos
        self.bicep = bicep
        self.forearm = forearm
        self.hand = hand
        self.arm_components = [bicep, forearm, hand]

    def update(self, dt):
        # Make the arm components rotate for demonstration purposes
        for i, arm_component in enumerate(self.arm_components):
            arm_component.angleToGroundRadians += 0.001 * (i + 1) * dt

    def draw(self, screen):
        # Calculate the positions of the arm components
        bicep_start = self.root_pos
        bicep_end = bicep_start + self.bicep.as_vector2()

        forearm_start = bicep_end
        forearm_end = forearm_start + self.forearm.as_vector2()

        hand_start = forearm_end
        hand_end = hand_start + self.hand.as_vector2()

        # Draw the arm components
        pygame.draw.line(screen, self.bicep.color, bicep_start, bicep_end, 8)
        pygame.draw.line(
            screen, self.forearm.color, forearm_start, forearm_end, 6
        )
        pygame.draw.line(screen, self.hand.color, hand_start, hand_end, 5)

        # Draw the end effector
        pygame.draw.circle(
            screen, (200, 255, 200), self.forward_kinematics(), 5
        )

    def forward_kinematics(self) -> Vector2:
        pos = self.root_pos.copy()

        for arm_component in self.arm_components:
            pos += arm_component.as_vector2()

        return pos

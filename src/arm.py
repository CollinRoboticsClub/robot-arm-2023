from math import pi, cos, sin, acos
import pygame
from pygame.math import Vector2


class ArmComponent:
    """
    Represents a component of an arm, such as the bicep, forearm, or hand.
    """

    def __init__(self, length=0.0, color=(0, 0, 0)):
        self.length = length
        self.angleToGroundRadians = 0.0
        self.color = color

    def as_vector2(self) -> Vector2:
        return Vector2(
            self.length * cos(self.angleToGroundRadians),
            self.length * sin(self.angleToGroundRadians),
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
        self.bicep.angleToGroundRadians += 0.0021 * dt
        self.forearm.angleToGroundRadians += 0.0032 * dt
        # self.hand.angleToGroundRadians += 0.0042 * dt

        self.bicep.angleToGroundRadians %= 2 * pi
        self.forearm.angleToGroundRadians %= 2 * pi
        self.hand.angleToGroundRadians %= 2 * pi

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

    # FIXME
    def inverse_kinematics(self, target_pos: Vector2, wrist_ground: float = 0):
        """
        Calculates IK, given a wrist angle. Useful when you care about the wrist angle!
        All angles in radians.
        """
        wrist_ground = wrist_ground % (2 * pi)

        wrist_setpoint = (
            target_pos
            - Vector2(cos(wrist_ground), sin(wrist_ground)) * self.hand.length
        )

        # Now it's just solving for the angles of an SSS triangle
        # [bicep, forearm, wrist_setpoint - root_pos]

        A = self.bicep.length
        B = self.forearm.length
        C = (wrist_setpoint - self.root_pos).length()

        # Law of cosines
        a = acos((B**2 + C**2 - A**2) / (2 * B * C))
        b = acos((A**2 + C**2 - B**2) / (2 * A * C))
        c = acos((A**2 + B**2 - C**2) / (2 * A * B))

        elbow_radians = c
        wrist_radians = wrist_ground + (pi - a)  # TODO: comment

        shoulder_radians = wrist_ground + b

        return shoulder_radians, elbow_radians, wrist_radians

    def angle_diagnostic_text(self) -> str:
        bicep, forearm, hand = self.inverse_kinematics(
            self.forward_kinematics()
        )

        # TODO: display in degrees
        # bicep_deg = bicep * 180 / pi
        # forearm_deg = forearm * 180 / pi
        # hand_deg = hand * 180 / pi

        return (
            f"IK: {bicep:.2f}, {forearm:.2f}, {hand:.2f}"
            + f"\nActual TO GROUND: {self.bicep.angleToGroundRadians:.2f}, {self.forearm.angleToGroundRadians:.2f}, {self.hand.angleToGroundRadians:.2f}"
        )

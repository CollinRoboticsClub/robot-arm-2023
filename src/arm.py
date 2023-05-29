import math
import pygame


class ArmComponent:
    length = 0.0
    angleToGround = 0.0  # in radians
    color = (0, 0, 0)

    def __init__(self, length, angleToGround, color, next=None, prev=None):
        self.length = length
        self.angleToGround = angleToGround
        self.color = color
        self.next_component = next
        self.prev_component = prev


class Arm:
    def __init__(
        self,
        root_pos,
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
        for arm_component in self.arm_components:
            arm_component.angleToGround += 0.001 * dt

    def draw(self, screen):
        cur_component = self.bicep
        last_end_pos = self.root_pos

        while cur_component != None:
            end_pos = (
                (
                    cur_component.length
                    * math.cos(cur_component.angleToGround),
                    cur_component.length
                    * math.sin(cur_component.angleToGround),
                ),
            )

            pygame.draw.line(
                screen,
                cur_component.color,
                last_end_pos,  # type: ignore
                end_pos,  # type: ignore
                width=5,
            )

            cur_component = cur_component.next_component
            last_end_pos = end_pos

    def forward_kinematics(self) -> tuple[float, float]:
        x = 0
        y = 0
        for arm_component in self.arm_components:
            x += arm_component.length * math.cos(arm_component.angleToGround)
            y += arm_component.length * math.sin(arm_component.angleToGround)
        return (x, y)

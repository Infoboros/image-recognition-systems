from math import cos, sin

import numpy as np

from models.model import Model


class Cup(Model):
    CIRCLE_RADIANS = 6.29

    UP = 0.2
    UP_RADIUS = 0.3

    DOWN = -0.2
    DOWN_RADIUS = 0.2

    def def_color_const(self):
        def _get_color(base):
            step = self.color_step
            if step > 50:
                step = 50 - step % 50
            if step == 50:
                step = 49

            return tuple(
                (component + step * 0.01) % 1.0
                for component in base
            )

        self.C1 = _get_color((0.0, 0.0, 0.5))
        self.C2 = _get_color((0.0, 0.5, 0.0))
        self.C3 = _get_color((0.5, 0.0, 0.0))

    def __init__(self,
                 context,
                 program,
                 edge_count: int,
                 color_step: int):
        super().__init__(context, program)
        self.edge_count = 3 if edge_count < 3 else edge_count
        self.color_step = color_step
        self.def_color_const()

    @staticmethod
    def get_point_by_angle(angle, radius, y) -> (float, float):
        return (
            radius * cos(angle),
            y,
            radius * sin(angle),
            1.0
        )

    def get_polygons(self) -> [[float]]:
        bottom_polygons = []
        upper_polygons = []

        step = self.CIRCLE_RADIANS / float(self.edge_count)

        for index in range(self.edge_count):
            start_angle_up = step * index
            end_angle_up = start_angle_up + step

            start_angle_down = (start_angle_up + end_angle_up) / 2.0
            end_angle_down = start_angle_down + step

            start_up = self.get_point_by_angle(start_angle_up, self.UP_RADIUS, self.UP)
            end_up = self.get_point_by_angle(end_angle_up, self.UP_RADIUS, self.UP)

            start_down = self.get_point_by_angle(start_angle_down, self.DOWN_RADIUS, self.DOWN)
            end_down = self.get_point_by_angle(end_angle_down, self.DOWN_RADIUS, self.DOWN)

            bottom_polygons.append(np.array(
                start_down + self.C2 +
                end_down + self.C2 +
                (0.0, self.DOWN, 0.0, 1.0) + self.C3
            ))

            bottom_polygons.append(np.array(
                (0.0, self.DOWN, 0.0, 1.0) + self.C2 +
                end_down + self.C1 +
                start_down + self.C1
            ))

            upper_polygons.append(np.array(
                start_up + self.C1 +
                end_up + self.C1 +
                start_down + self.C2
            ))
            upper_polygons.append(np.array(
                end_down + self.C2 +
                start_down + self.C2 +
                end_up + self.C1
            ))

            upper_polygons.append(np.array(
                start_down + self.C1 +
                end_up + self.C3 +
                start_up + self.C3
            ))
            upper_polygons.append(np.array(
                end_up + self.C3 +
                start_down + self.C1 +
                end_down + self.C1
            ))

        return bottom_polygons + upper_polygons

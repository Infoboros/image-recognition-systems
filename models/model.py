from abc import ABC, abstractmethod
from math import sqrt


class Model(ABC):

    def __init__(self, context, program):
        self.ctx = context
        self.prog = program

    @staticmethod
    def sub_lists(a: [float], b: [float]):
        return [
            a_item - b[index]
            for index, a_item in enumerate(a)
        ]

    @staticmethod
    def get_norm(a: [float], b: [float], c: [float]):
        v1 = Model.sub_lists(a, b)
        v2 = Model.sub_lists(b, c)

        N = [
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0]
        ]

        norma = sqrt(
            pow(v1[1] * v2[2] - v1[2] * v2[1], 2) +
            pow(v1[2] * v2[0] - v1[0] * v2[2], 2) +
            pow(v1[0] * v2[1] - v1[1] * v2[0], 2)
        )
        return tuple([
            n / norma
            for n in N
        ])

    @staticmethod
    def add_norm_to_polygon(*polygon: [[float]]) -> [float]:
        normal = Model.get_norm(*polygon[::2])

        return \
            polygon[0] + polygon[1] + normal + \
            polygon[2] + polygon[3] + normal + \
            polygon[4] + polygon[5] + normal


    @abstractmethod
    def get_polygons(self) -> [[float]]:
        raise NotImplemented()

    def get_vao_list(self) -> []:
        return [
            self.ctx.simple_vertex_array(
                self.prog,
                self.ctx.buffer(polygon.astype(f'f4').tobytes()),
                ['vert', 'tex_coord', 'normal']
            )
            for polygon in self.get_polygons()
        ]

from abc import ABC, abstractmethod


class Model(ABC):

    def __init__(self, context, program):
        self.ctx = context
        self.prog = program

    @abstractmethod
    def get_polygons(self) -> [[float]]:
        raise NotImplemented()

    def get_vao_list(self) -> []:
        return [
            self.ctx.simple_vertex_array(
                self.prog,
                self.ctx.buffer(polygon.astype(f'f4').tobytes()),
                ['vert', 'vert_color']
            )
            for polygon in self.get_polygons()
        ]

from ModernGL import VertexArray

from models.plate import Plate
from scenes.default_scene import DefaultScene


class PlateScene(DefaultScene):

    def __init__(self, screen):
        super().__init__(
            screen,
            [
                "СРО. Лабораторная работа №1",
                "Колесо мыши - масштабирование",
                "Зажатая кнопка мыши - повернуть сцену",
                "Стрелки - подвинуть сцену",
            ]
        )

    def get_vaoes(self) -> [VertexArray]:
        return \
            Plate(self.ctx, self.prog, 5) \
                .get_vao_list()

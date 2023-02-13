import ModernGL
import numpy as np
from ModernGL import VertexArray
from OpenGL import GL
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QVBoxLayout, QPlainTextEdit, QSizePolicy, QHBoxLayout, QTextEdit, QLabel, QDoubleSpinBox, \
    QSpinBox, QComboBox

from models.plate import Plate
from scenes.default_scene import DefaultScene


class PlateScene(DefaultScene):

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addStretch()

        label = QLabel('Тип проекции:', self)
        layout.addWidget(label)

        self.proect_type_input = QComboBox(self)
        self.proect_type_input.addItems([
            'Перспективная',
            'Ортографическая',
        ])
        self.proect_type_input.setFixedSize(100, 30)
        self.proect_type_input.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.proect_type_input.currentIndexChanged.connect(self.change_proect_type)
        layout.addWidget(self.proect_type_input)

        layout.addStretch()

        label = QLabel('Количество ребер:', self)
        layout.addWidget(label)

        self.edge_input = QSpinBox(self)
        self.edge_input.setFixedSize(100, 30)
        self.edge_input.setValue(self.edge_count)
        self.edge_input.setSingleStep(1)
        self.edge_input.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.edge_input.valueChanged.connect(self.change_edge_input)
        layout.addWidget(self.edge_input)

        layout.addStretch()

    def __init__(self, screen):
        super().__init__(
            screen,
            [
                "СРО. Лабораторная работа №1",
                "Колесо мыши - масштабирование",
                "Зажатая кнопка мыши - повернуть сцену",
                "Стрелки - подвинуть сцену",
                "Зажать Tab - анимация переливания цветов",
                "XYZ - вращение вокруг последнего двойного нажатия"
            ]
        )
        self.edge_count = 5
        self.color_step = 0
        self.init_ui()

    def get_vaoes(self) -> [VertexArray]:
        return \
            Plate(
                self.ctx,
                self.prog,
                self.edge_count,
                self.color_step
            ) \
                .get_vao_list()

    def change_edge_input(self, value):
        if value < 3:
            self.edge_input.setValue(3)
            value = 3

        self.edge_count = value

        self.initializeGL()
        self.update()

    def change_proect_type(self, index: int):
        self.proect = index
        self.update()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        super().keyPressEvent(event)
        if event.key() == 16777217:
            self.color_step += 1
            self.color_step %= 100

            self.initializeGL()
            self.update()

from abc import abstractmethod
from contextlib import suppress

import ModernGL
import numpy as np
from ModernGL import VertexArray
from OpenGL import GL
from PyQt6 import QtGui
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QScreen, QPainter, QMatrix4x4, QSurfaceFormat
from PyQt6.QtOpenGLWidgets import QOpenGLWidget


class DefaultScene(QOpenGLWidget):
    SCALE_STEP = 8.3e-5
    ROTATE_ANGLE = 2.0
    TRANSLATE_DELTA = 0.1

    def print_legend(self):
        title, *legend = self.legend
        self.setWindowTitle(title)

        painter = QPainter(self)
        painter.beginNativePainting()
        position = QPointF(10, 20)

        painter.drawText(10, 20, title)
        for row in legend:
            position += QPointF(0, 16)
            painter.drawText(position, row)
        painter.endNativePainting()

    def centralize(self, screen: QScreen):
        self.move(
            screen.availableGeometry().center()
            -
            self.rect().center()
        )

    def __init__(self, screen: QScreen, legend: [str]):
        self.legend = legend

        self.scale = 1.0
        self.last_mouse_down = QPointF()
        self.last_double_click = QPointF()
        self.rotate_matrix = self.init_matrix()
        self.base_rotate_matrix = self.init_matrix()
        self.translate_matrix = self.init_matrix()

        self.vaoes: [VertexArray] = []
        self.proect = 0

        q_format = QSurfaceFormat()
        q_format.setVersion(3, 3)
        q_format.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
        QSurfaceFormat.setDefaultFormat(q_format)

        super().__init__()
        self.resize(1000, 800)
        self.centralize(screen)

    @staticmethod
    def init_matrix() -> QMatrix4x4:
        matrix = QMatrix4x4()
        matrix.setToIdentity()
        return matrix

    def get_model_matrix(self) -> [float]:
        matrix = QMatrix4x4()
        matrix.setToIdentity()

        if self.proect == 0:
            matrix.perspective(30.0, self.width() / float(self.height()), 0.1, 20.0)
            matrix.translate(0.0, 0.0, -5.0)
            matrix *= self.translate_matrix

            matrix.scale(self.scale, self.scale, self.scale)
            matrix *= self.base_rotate_matrix * self.rotate_matrix.transposed()
        else:
            matrix *= self.translate_matrix

            matrix.scale(self.scale, self.scale, self.scale)
            matrix.rotate(30, 1, 0, 0)
            matrix *= self.base_rotate_matrix * self.rotate_matrix.transposed()

            matrix.translate(0.0, 0.0, 0.5)
            matrix.ortho(-1.0, -1.0, 1.0, 1.0, -1.5, 1.5)

        return tuple(matrix.data())

    def resizeGL(self, w: int, h: int) -> None:
        self.ctx.viewport = (0, 0, self.width(), self.height())

    @abstractmethod
    def get_vaoes(self) -> [VertexArray]:
        raise NotImplemented()

    def initializeGL(self):
        self.ctx = ModernGL.create_context()
        self.ctx.enable(ModernGL.CULL_FACE)

        self.ctx.enable(ModernGL.DEPTH_TEST)
        self.prog = self.ctx.program(
            [
                self.ctx.vertex_shader('''
                            #version 330
    
                            in vec4 vert;
                            in vec3 vert_color;
                            
                            uniform mat4 model_matrix;
                            
                            out vec3 frag_color;
    
                            void main() {
                                frag_color = vert_color;
                                gl_Position = model_matrix * vert;
                            }
                '''),
                self.ctx.fragment_shader('''
                            #version 330
    
                            in vec3 frag_color;
                            out vec4 color;

                            void main() {
                                color = vec4(frag_color, 1.0);
                            }
                ''')
            ]
        )

        self.vaoes = self.get_vaoes()

        self.rotate_polygon_center = [
            ((self.last_double_click.x() / float(self.width())) * 2.0 - 1.0),
            -1 * ((self.last_double_click.y() / float(self.height())) * 2.0 - 1.0)
        ]
        self.rotate_point_polygon = np.array([
            self.rotate_polygon_center[0], self.rotate_polygon_center[1] + 0.05, 0.0, 1.0,
            1.0, 0.0, 0.0,

            self.rotate_polygon_center[0] - 0.05, self.rotate_polygon_center[1] - 0.05, 0.0, 1.0,
            1.0, 0.0, 0.0,

            self.rotate_polygon_center[0] + 0.05, self.rotate_polygon_center[1] - 0.05, 0.0, 1.0,
            1.0, 0.0, 0.0,
        ])
        self.rotate_point = self.ctx.simple_vertex_array(
            self.prog,
            self.ctx.buffer(
                self.rotate_point_polygon.astype(f'f4').tobytes()
            ),
            ['vert', 'vert_color']
        )

    def paintGL(self):
        self.ctx.clear(1.0, 1.0, 1.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glEnable(GL.GL_DEPTH_TEST)

        self.prog.uniforms['model_matrix'].value = self.get_model_matrix()
        [
            vao.render(mode=ModernGL.TRIANGLE_STRIP)
            for vao in self.vaoes
        ]

        self.prog.uniforms['model_matrix'].value = tuple(self.init_matrix().data())
        self.rotate_point.render(mode=ModernGL.TRIANGLE_STRIP)

        self.ctx.finish()

        self.print_legend()

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        delta = event.angleDelta().y() * self.SCALE_STEP
        self.scale += delta
        if self.scale < 0.0:
            self.scale = 0.0
        if self.scale > 1.0:
            self.scale = 1.0
        self.update()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.last_mouse_down = event.pos()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        event_position = event.pos()
        delta = event_position - self.last_mouse_down

        self.rotate_matrix.rotate(self.ROTATE_ANGLE, -delta.y(), -delta.x(), 0.0)

        self.last_mouse_down = event_position

        self.update()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:

        self.base_rotate_matrix.translate(self.rotate_polygon_center[0], self.rotate_polygon_center[1])

        if (event.key() == 88) or (event.key() == 1063):
            self.base_rotate_matrix.rotate(self.ROTATE_ANGLE, 1.0, 0.0, 0.0)

        if (event.key() == 89) or (event.key() == 1053):
            self.base_rotate_matrix.rotate(self.ROTATE_ANGLE, 0.0, 1.0, 0.0)

        if (event.key() == 90) or (event.key() == 1071):
            self.base_rotate_matrix.rotate(self.ROTATE_ANGLE, 0.0, 0.0, 1.0)

        self.base_rotate_matrix.translate(-self.rotate_polygon_center[0], -self.rotate_polygon_center[1])

        with suppress(KeyError):
            direction = {
                16777235: QPointF(0.0, self.TRANSLATE_DELTA),
                16777237: QPointF(0.0, -self.TRANSLATE_DELTA),
                16777236: QPointF(self.TRANSLATE_DELTA, 0.0),
                16777234: QPointF(-self.TRANSLATE_DELTA, 0.0),
            }[event.key()]
            self.translate_matrix.translate(direction.x(), direction.y(), 0.0)

        self.initializeGL()
        self.update()

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        self.last_double_click = event.pos()
        self.initializeGL()
        self.update()

import struct

import ModernGL
from PyQt6 import QtOpenGL, QtOpenGLWidgets
from PyQt6.QtGui import QSurfaceFormat
from PyQt6.QtWidgets import QApplication


class QGLControllerWidget(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self):


        super().__init__()

    def initializeGL(self):
        self.ctx = ModernGL.create_context()

        prog = self.ctx.program([
            self.ctx.vertex_shader('''
                                #version 330
                                in vec2 vert;
                                void main() {
                                        gl_Position = vec4(vert, 0.0, 1.0);
                                }
                        '''),
            self.ctx.fragment_shader('''
                                #version 330
                                out vec4 color;
                                void main() {
                                        color = vec4(0.3, 0.5, 1.0, 1.0);
                                }
                        '''),
        ])

        vbo = self.ctx.buffer(struct.pack('6f', 0.0, 0.8, -0.6, -0.8, 0.6, -0.8))
        self.vao = self.ctx.simple_vertex_array(prog, vbo, ['vert'])

    def paintGL(self):
        self.ctx.viewport = (0, 0, self.width(), self.height())
        self.ctx.clear(0.9, 0.9, 0.9)
        self.vao.render()
        self.ctx.finish()


app = QApplication([])
window = QGLControllerWidget()
window.show()
app.exec()

from OpenGL import GL
from PyQt6.QtWidgets import QApplication

from scenes.plate_scene import PlateScene

if __name__ == '__main__':
    app = QApplication([])
    screens = app.screens()

    widget = PlateScene(
        screens[-1]
    )
    widget.show()
    app.exec()

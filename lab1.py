from PyQt6.QtCore import QCoreApplication, Qt
from PyQt6.QtGui import QSurfaceFormat

from scenes.default_scene import DefaultScene
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

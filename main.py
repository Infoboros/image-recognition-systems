from PyQt6.QtWidgets import QApplication

from scenes.cupscene import CupScene

if __name__ == '__main__':
    app = QApplication([])
    screens = app.screens()

    widget = CupScene(
        screens[-1]
    )
    widget.show()
    app.exec()

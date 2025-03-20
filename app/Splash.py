from PyQt6.QtWidgets import QApplication, QMainWindow, QSplashScreen
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap

class SplashScreen(QSplashScreen):
    def __init__(self):
        pixmap = QPixmap("/resourses/folder_icon.png")

        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

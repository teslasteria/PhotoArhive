import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QLocale
from app.main_window import PhotoArchiveApp

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Устанавливаем стандартную локаль
    locale = QLocale.system().name()

    # Установка базового пути для переводов
    if hasattr(sys, '_MEIPASS'):
        # Для pyinstaller
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    window = PhotoArchiveApp()
    window.show()
    app.exec()
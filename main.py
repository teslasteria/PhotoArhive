import sys
from PyQt6.QtWidgets import QApplication
from app.main_window import PhotoArchiveApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PhotoArchiveApp()
    window.show()
    sys.exit(app.exec())
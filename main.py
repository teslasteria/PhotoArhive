import sys
from PyQt6.QtWidgets import QApplication
from app.main_window import PhotoArchiveApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Устанавливаем стиль Fusion до создания основного окна
    app.setStyle('Fusion')
    
    window = PhotoArchiveApp()
    window.show()
    app.exec()
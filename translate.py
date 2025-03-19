import os
from PyQt6.QtCore import QTranslator, QCoreApplication
from PyQt6.QtWidgets import QApplication
import sys

# Создаём приложение
app = QApplication(sys.argv)

# Генерация .ts файлов
languages = ['ru', 'de', 'es', 'fr']
for lang in languages:
    os.system(f'pylupdate6 --verbose app/main_window.py -ts translations/{lang}.ts')
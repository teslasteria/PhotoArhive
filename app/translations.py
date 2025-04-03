import os
from PyQt6.QtCore import QTranslator, QLocale, QLibraryInfo
from PyQt6.QtWidgets import QApplication

class TranslationManager:
    def __init__(self, app):
        self.app = app
        self.app_translator = QTranslator()
        self.qt_translator = QTranslator()
        
    def load_translation(self, language):
        """Загрузка переводов с обработкой ошибок"""
        print(f"Attempting to load translation for: {language}")
        
        # Удаляем предыдущие переводы
        self.app.removeTranslator(self.app_translator)
        self.app.removeTranslator(self.qt_translator)
        
        # Пути к файлам перевода
        base_dir = os.path.dirname(os.path.dirname(__file__))
        translations_path = os.path.join(base_dir, "app", "translations")
        
        # 1. Загружаем системные переводы Qt
        qt_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
        if self.qt_translator.load(f"qtbase_{language}", qt_path):
            self.app.installTranslator(self.qt_translator)
            print(f"Loaded Qt system translation for {language}")
        
        # 2. Загружаем переводы приложения
        qm_file = os.path.join(translations_path, f"photoarchive_{language}.qm")
        
        if not os.path.exists(qm_file):
            print(f"Translation file not found: {qm_file}")
            return False
            
        if self.app_translator.load(qm_file):
            self.app.installTranslator(self.app_translator)
            QLocale.setDefault(QLocale(language))
            print(f"Successfully loaded app translation: {qm_file}")
            return True
        
        print(f"Failed to load translation file: {qm_file}")
        return False
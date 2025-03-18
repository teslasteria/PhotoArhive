import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QProgressBar, QLabel, QMenuBar, QMenu, QHBoxLayout, 
    QApplication, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PIL import Image
from PIL.ExifTags import TAGS
from .themes import dark_stylesheet, light_stylesheet

class PhotoArchiveApp(QWidget):
    def __init__(self):
        super().__init__()

        # Setting up Fusion
        QApplication.setStyle('Fusion')

        self.initUI()

        # default theme
        self.dark_theme = True
        self.setStyleSheet(dark_stylesheet)

    def initUI(self):
        self.setWindowTitle('PhotoArchive')

        # Size and position
        self.setGeometry(100, 100, 1200, 600)  

        # App logo
        self.setWindowIcon(QIcon('resources/app_icon.png'))

        # Menu
        menubar = QMenuBar(self)
        file_menu = menubar.addMenu('File')

        # New Project
        new_project_action = file_menu.addAction('New Project')
        new_project_action.triggered.connect(self.new_project)

        # Open Project
        open_project_action = file_menu.addAction('Open Project')
        open_project_action.triggered.connect(self.open_project)

        # Save Project
        save_project_action = file_menu.addAction('Save Project')
        save_project_action.triggered.connect(self.save_project)

        # Exit
        exit_action = file_menu.addAction('Exit')
        exit_action.triggered.connect(self.close)

        # В методе initUI
        edit_menu = menubar.addMenu('Edit')

        # Undo
        undo_action = edit_menu.addAction('Undo')
        undo_action.triggered.connect(self.undo)

        # Redo
        redo_action = edit_menu.addAction('Redo')
        redo_action.triggered.connect(self.redo)

        # Clear
        clear_action = edit_menu.addAction('Clear')
        clear_action.triggered.connect(self.clear)

        # Preferences
        preferences_action = edit_menu.addAction('Preferences')
        preferences_action.triggered.connect(self.open_preferences)

        # В методе initUI
        preferences_menu = menubar.addMenu('Preferences')

        # Toggle Dark Theme
        theme_action = preferences_menu.addAction('Toggle Dark Theme')
        theme_action.triggered.connect(self.toggle_theme)

        # Language
        language_menu = preferences_menu.addMenu('Language')
        english_action = language_menu.addAction('English')
        english_action.triggered.connect(lambda: self.set_language('English'))
        russian_action = language_menu.addAction('Russian')
        russian_action.triggered.connect(lambda: self.set_language('Russian'))

        # Reset Settings
        reset_action = preferences_menu.addAction('Reset Settings')
        reset_action.triggered.connect(self.reset_settings)

        # Добавление действий в меню Preferences
        theme_action = preferences_menu.addAction('Toggle Dark Theme')
        theme_action.triggered.connect(self.toggle_theme)

        # Основной layout
        main_layout = QVBoxLayout()

        # Добавление меню в layout
        main_layout.setMenuBar(menubar)

        # Контейнер для кнопок выбора директорий
        dir_buttons_layout = QHBoxLayout()
        self.source_dir_btn = QPushButton('Select Source Directory', self)
        self.source_dir_btn.setIcon(QIcon('resources/folder_icon.png'))
        self.source_dir_btn.clicked.connect(self.select_source_directory)
        dir_buttons_layout.addWidget(self.source_dir_btn)

        self.target_dir_btn = QPushButton('Select Target Directory', self)
        self.target_dir_btn.setIcon(QIcon('resources/folder_icon.png'))
        self.target_dir_btn.clicked.connect(self.select_target_directory)
        dir_buttons_layout.addWidget(self.target_dir_btn)

        # Добавление контейнера с кнопками в основной layout
        main_layout.addLayout(dir_buttons_layout)

        # Метки для отображения выбранных директорий
        self.source_dir_label = QLabel('Source Directory: Not selected', self)
        self.target_dir_label = QLabel('Target Directory: Not selected', self)
        main_layout.addWidget(self.source_dir_label)
        main_layout.addWidget(self.target_dir_label)

        # Прогресс-бар
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
                background-color: #f0f0f0;
            }
            QProgressBar::chunk {
                background-color: green;
                width: 10px;
            }
        """)
        main_layout.addWidget(self.progress_bar)

        # Метка статуса
        self.status_label = QLabel('Ready to start', self)
        main_layout.addWidget(self.status_label)

        # Кнопка для начала сортировки
        self.start_btn = QPushButton('Start Sorting', self)
        self.start_btn.setIcon(QIcon('resources/start_icon.png'))
        self.start_btn.clicked.connect(self.start_sorting)
        main_layout.addWidget(self.start_btn)

        # # Кнопка для смены темы
        # self.theme_btn = QPushButton('Toggle Theme', self)
        # self.theme_btn.setIcon(QIcon('resources/theme_icon.png'))
        # self.theme_btn.clicked.connect(self.toggle_theme)
        # main_layout.addWidget(self.theme_btn)

        # Установка основного layout
        self.setLayout(main_layout)

        # Установка отступов и расстояний
        main_layout.setSpacing(15)  # Расстояние между элементами
        main_layout.setContentsMargins(20, 20, 20, 20)  # Отступы от краёв окна

        # Включение кнопок управления окном (свернуть, развернуть, закрыть)
        self.setWindowFlags(Qt.WindowType.Window |
                           Qt.WindowType.WindowMinimizeButtonHint |
                           Qt.WindowType.WindowMaximizeButtonHint |
                           Qt.WindowType.WindowCloseButtonHint)

        self.source_dir = None
        self.target_dir = None

    def select_source_directory(self):
        """Выбор исходной директории"""
        self.source_dir = QFileDialog.getExistingDirectory(self, 'Select Source Directory')
        if self.source_dir:
            self.source_dir_label.setText(f'Source Directory: {self.source_dir}')
        else:
            self.source_dir_label.setText('Source Directory: Not selected')

    def select_target_directory(self):
        """Выбор целевой директории"""
        self.target_dir = QFileDialog.getExistingDirectory(self, 'Select Target Directory')
        if self.target_dir:
            self.target_dir_label.setText(f'Target Directory: {self.target_dir}')
        else:
            self.target_dir_label.setText('Target Directory: Not selected')

    def start_sorting(self):
        """Начало сортировки фотографий"""
        if not self.source_dir or not self.target_dir:
            self.status_label.setText('Please select both source and target directories.')
            return

        self.status_label.setText('Sorting started...')
        self.progress_bar.setValue(0)

        photos = [f for f in os.listdir(self.source_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))]
        total_photos = len(photos)
        processed = 0

        for photo in photos:
            photo_path = os.path.join(self.source_dir, photo)
            try:
                img = Image.open(photo_path)
                exif_data = img._getexif()
                if exif_data:
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        if tag == 'DateTime':
                            date = value.split()[0].replace(':', '-')
                            year, month, day = date.split('-')
                            target_folder = os.path.join(self.target_dir, year, month, day)
                            os.makedirs(target_folder, exist_ok=True)
                            img.close()
                            os.rename(photo_path, os.path.join(target_folder, photo))
                            break
            except Exception as e:
                print(f'Error processing file {photo}: {e}')

            processed += 1
            self.progress_bar.setValue(int((processed / total_photos) * 100))

        self.status_label.setText('Sorting completed!')

    def clear(self):
        """Очистка выбранных директорий"""
        self.source_dir = None
        self.target_dir = None
        self.source_dir_label.setText('Source Directory: Not selected')
        self.target_dir_label.setText('Target Directory: Not selected')
        self.status_label.setText('Ready to start')
        self.progress_bar.setValue(0)

    def toggle_theme(self):
        """Переключение между светлой и тёмной темами"""
        self.dark_theme = not self.dark_theme
        if self.dark_theme:
            self.setStyleSheet(dark_stylesheet)
        else:
            self.setStyleSheet(light_stylesheet)
    
    def new_project(self):
        """Создание нового проекта"""
        self.source_dir = None
        self.target_dir = None
        self.source_dir_label.setText('Source Directory: Not selected')
        self.target_dir_label.setText('Target Directory: Not selected')
        self.status_label.setText('Ready to start')
        self.progress_bar.setValue(0)
        QMessageBox.information(self, 'New Project', 'New project created.')

    def open_project(self):
        """Загрузка проекта"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "Project Files (*.json);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    data = json.load(file)
                    self.source_dir = data.get('source_dir')
                    self.target_dir = data.get('target_dir')
                    self.source_dir_label.setText(f'Source Directory: {self.source_dir}')
                    self.target_dir_label.setText(f'Target Directory: {self.target_dir}')
                    QMessageBox.information(self, 'Open Project', 'Project loaded successfully.')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to load project: {e}')

    def save_project(self):
        """Сохранение проекта"""
        if not self.source_dir or not self.target_dir:
            QMessageBox.warning(self, 'Warning', 'Please select source and target directories first.')
            return

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Project", "", "Project Files (*.json);;All Files (*)", options=options)
        if file_name:
            try:
                data = {
                    'source_dir': self.source_dir,
                    'target_dir': self.target_dir
                }
                with open(file_name, 'w') as file:
                    json.dump(data, file)
                QMessageBox.information(self, 'Save Project', 'Project saved successfully.')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to save project: {e}')

    def undo(self):
        """Отмена последнего действия"""
        # Пример: можно добавить историю действий и отмену
        QMessageBox.information(self, 'Undo', 'Undo last action.')

    def redo(self):
        """Повтор последнего отменённого действия"""
        # Пример: можно добавить историю действий и повтор
        QMessageBox.information(self, 'Redo', 'Redo last undone action.')

    def clear(self):
        """Очистка выбранных директорий"""
        self.source_dir = None
        self.target_dir = None
        self.source_dir_label.setText('Source Directory: Not selected')
        self.target_dir_label.setText('Target Directory: Not selected')
        self.status_label.setText('Ready to start')
        self.progress_bar.setValue(0)

    def open_preferences(self):
        """Открытие окна настроек"""
        # Пример: можно открыть диалоговое окно с настройками
        QMessageBox.information(self, 'Preferences', 'Open preferences dialog.')

    def toggle_theme(self):
        """Переключение между светлой и тёмной темами"""
        self.dark_theme = not self.dark_theme
        if self.dark_theme:
            self.setStyleSheet(dark_stylesheet)
        else:
            self.setStyleSheet(light_stylesheet)

    def set_language(self, language):
        """Установка языка интерфейса"""
        # Пример: можно добавить поддержку нескольких языков
        QMessageBox.information(self, 'Language', f'Language set to {language}.')

    def reset_settings(self):
        """Сброс настроек к значениям по умолчанию"""
        self.dark_theme = False
        self.setStyleSheet(light_stylesheet)
        QMessageBox.information(self, 'Reset Settings', 'Settings reset to default.')
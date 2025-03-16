import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QProgressBar, QLabel, QMenuBar, QMenu, QHBoxLayout,
    QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PIL import Image
from PIL.ExifTags import TAGS
from .themes import dark_stylesheet, light_stylesheet  # Импорт стилей

class PhotoArchiveApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.dark_theme = False  # Флаг для отслеживания текущей темы

    def initUI(self):
        self.setWindowTitle('PhotoArchive')
        self.setGeometry(100, 100, 1200, 600)  # Установка начального размера и позиции

        # Установка стиля Fusion (современный вид)
        QApplication.setStyle('Fusion')

        # Установка иконки приложения
        self.setWindowIcon(QIcon('resources/app_icon.png'))

        # Создание меню
        menubar = QMenuBar(self)
        file_menu = menubar.addMenu('File')
        edit_menu = menubar.addMenu('Edit')
        preferences_menu = menubar.addMenu('Preferences')

        # Добавление действий в меню File
        exit_action = file_menu.addAction('Exit')
        exit_action.triggered.connect(self.close)

        # Добавление действий в меню Edit
        clear_action = edit_menu.addAction('Clear')
        clear_action.triggered.connect(self.clear)

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

        # Кнопка для смены темы
        self.theme_btn = QPushButton('Toggle Theme', self)
        self.theme_btn.setIcon(QIcon('resources/theme_icon.png'))
        self.theme_btn.clicked.connect(self.toggle_theme)
        main_layout.addWidget(self.theme_btn)

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
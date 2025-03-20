import os
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QPushButton, 
    QFileDialog, 
    QProgressBar, 
    QLabel, 
    QMenuBar, 
    QMenu, 
    QHBoxLayout, 
    QApplication, 
    QMessageBox, 
    QCheckBox, 
    QGroupBox,
    QTextEdit,
    QDialog,
    QGridLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PIL import Image
from PIL.ExifTags import TAGS
from .themes import dark_stylesheet, light_stylesheet, progress_bar_style

class FileInfoDialog(QDialog):
    """Окно для отображения информации о файлах"""
    def __init__(self, file_info, parent=None):
        super().__init__(parent)
        self.setWindowTitle("File Information")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setText(file_info)
        layout.addWidget(self.text_edit)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

class PhotoArchiveApp(QWidget):
    def __init__(self):
        super().__init__()

        # Setting up Fusion
        QApplication.setStyle('Fusion')

        self.initUI()

        # default theme
        self.dark_theme = True
        self.setStyleSheet(dark_stylesheet)

        # Режим работы кнопки: False - отбор файлов, True - сортировка
        self.sorting_mode = False

        #  list of selected file formats
        self.selected_formats = []

    def initUI(self):
        self.setWindowTitle('PhotoArchive')

        # Size and position
        self.setGeometry(100, 100, 1200, 600)  

        # App logo
        self.setWindowIcon(QIcon('resources/app_icon.png'))

        # Menu
        menubar = QMenuBar(self)
        file_menu = menubar.addMenu('File')

        # Exit
        exit_action = file_menu.addAction('Exit')
        exit_action.triggered.connect(self.close)

        # Edit section
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

        # Preferences section
        preferences_menu = menubar.addMenu('Preferences')

        # Language
        language_menu = preferences_menu.addMenu('Language')
        english_action = language_menu.addAction('English')
        english_action.triggered.connect(lambda: self.set_language('English'))
        russian_action = language_menu.addAction('Russian')
        russian_action.triggered.connect(lambda: self.set_language('Russian'))

        # Reset Settings
        reset_action = preferences_menu.addAction('Reset Settings')
        reset_action.triggered.connect(self.reset_settings)

        # Toggle theme
        theme_action = preferences_menu.addAction('Toggle Dark Theme')
        theme_action.triggered.connect(self.toggle_theme)

        # main layout
        main_layout = QVBoxLayout()

        # add menu to layout
        main_layout.setMenuBar(menubar)

        # Контейнер для кнопок выбора директорий и меток
        dir_buttons_layout = QVBoxLayout()

        # Кнопка и метка для исходной директории
        source_dir_layout = QHBoxLayout()
        self.source_dir_btn = QPushButton(self.tr('Select Source Directory'), self)
        self.source_dir_btn.setIcon(QIcon('resources/folder_icon.png'))
        self.source_dir_btn.clicked.connect(self.select_source_directory)
        self.source_dir_label = QLabel(self.tr('Source Directory: Not selected'), self)
        self.source_dir_btn.setFixedWidth(200)
        source_dir_layout.addWidget(self.source_dir_btn)
        source_dir_layout.addWidget(self.source_dir_label)
        dir_buttons_layout.addLayout(source_dir_layout)

        # Кнопка и метка для целевой директории
        target_dir_layout = QHBoxLayout()
        self.target_dir_btn = QPushButton(self.tr('Select Target Directory'), self)
        self.target_dir_btn.setIcon(QIcon('resources/folder_icon.png'))
        self.target_dir_btn.clicked.connect(self.select_target_directory)
        self.target_dir_label = QLabel(self.tr('Target Directory: Not selected'), self)
        self.target_dir_btn.setFixedWidth(200)
        target_dir_layout.addWidget(self.target_dir_btn)
        target_dir_layout.addWidget(self.target_dir_label)
        dir_buttons_layout.addLayout(target_dir_layout)

        # Добавление контейнера с кнопками в основной layout
        main_layout.addLayout(dir_buttons_layout)

        checkBox_and_log_output_layout = QHBoxLayout()

        # Group for check boxes
        formats_group = QGroupBox(self.tr('Select Formats to Sort'))
        formats_layout = QGridLayout()

        
        # Чекбоксы для форматов
        self.png_checkbox = QCheckBox('PNG')
        self.jpg_checkbox = QCheckBox('JPG')
        self.jpeg_checkbox = QCheckBox('JPEG')
        self.raw_checkbox = QCheckBox('RAW')
        self.nef_checkbox = QCheckBox('NEF')
        self.cr2_checkbox = QCheckBox('CR2')  # Добавляем новые форматы
        self.dng_checkbox = QCheckBox('DNG')
        self.gif_checkbox = QCheckBox('GIF')
        self.bmp_checkbox = QCheckBox('BMP')
        self.tiff_checkbox = QCheckBox('TIFF')
        self.webp_checkbox = QCheckBox('WEBP')
        self.heic_checkbox = QCheckBox('HEIC/HEIF')
        self.psd_checkbox = QCheckBox('PSD')
        self.svg_checkbox = QCheckBox('SVG')
        self.ico_checkbox = QCheckBox('ICO')
        self.tga_checkbox = QCheckBox('TGA')

        # Устанавливаем чекбоксы по умолчанию
        self.png_checkbox.setChecked(True)
        self.jpg_checkbox.setChecked(True)
        self.jpeg_checkbox.setChecked(True)
        self.raw_checkbox.setChecked(False)
        self.nef_checkbox.setChecked(False)
        self.cr2_checkbox.setChecked(False)  # По умолчанию новые форматы выключены
        self.dng_checkbox.setChecked(False)
        self.gif_checkbox.setChecked(False)
        self.bmp_checkbox.setChecked(False)
        self.tiff_checkbox.setChecked(False)
        self.webp_checkbox.setChecked(False)
        self.heic_checkbox.setChecked(False)
        self.psd_checkbox.setChecked(False)
        self.svg_checkbox.setChecked(False)
        self.ico_checkbox.setChecked(False)
        self.tga_checkbox.setChecked(False)

        # Добавляем чекбоксы в QGridLayout (два столбца)
        formats_layout.addWidget(self.png_checkbox, 0, 0)  # Строка 0, Столбец 0
        formats_layout.addWidget(self.jpg_checkbox, 1, 0)  # Строка 1, Столбец 0
        formats_layout.addWidget(self.jpeg_checkbox, 2, 0)  # Строка 2, Столбец 0
        formats_layout.addWidget(self.raw_checkbox, 3, 0)  # Строка 3, Столбец 0
        formats_layout.addWidget(self.nef_checkbox, 4, 0)  # Строка 4, Столбец 0
        formats_layout.addWidget(self.cr2_checkbox, 5, 0)  # Строка 5, Столбец 0
        formats_layout.addWidget(self.dng_checkbox, 6, 0)  # Строка 6, Столбец 0
        formats_layout.addWidget(self.gif_checkbox, 7, 0)  # Строка 7, Столбец 0

        formats_layout.addWidget(self.bmp_checkbox, 0, 1)  # Строка 0, Столбец 1
        formats_layout.addWidget(self.tiff_checkbox, 1, 1)  # Строка 1, Столбец 1
        formats_layout.addWidget(self.webp_checkbox, 2, 1)  # Строка 2, Столбец 1
        formats_layout.addWidget(self.heic_checkbox, 3, 1)  # Строка 3, Столбец 1
        formats_layout.addWidget(self.psd_checkbox, 4, 1)  # Строка 4, Столбец 1
        formats_layout.addWidget(self.svg_checkbox, 5, 1)  # Строка 5, Столбец 1
        formats_layout.addWidget(self.ico_checkbox, 6, 1)  # Строка 6, Столбец 1
        formats_layout.addWidget(self.tga_checkbox, 7, 1)  # Строка 7, Столбец 1

        formats_group.setFixedWidth(200)
        formats_group.setLayout(formats_layout)
        checkBox_and_log_output_layout.addWidget(formats_group)

        # Добавляем QTextEdit для отображения перемещения файлов
        self.log_text_edit = QTextEdit(self)
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setPlaceholderText("File movement log will appear here...")
        checkBox_and_log_output_layout.addWidget(self.log_text_edit)

        main_layout.addLayout(checkBox_and_log_output_layout)

        # progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet(progress_bar_style)
        main_layout.addWidget(self.progress_bar)

        # Метка статуса
        self.status_label = QLabel('Ready to start', self)
        main_layout.addWidget(self.status_label)

        # Кнопка для начала сортировки
        self.start_btn = QPushButton('Start Sorting', self)
        self.start_btn.setIcon(QIcon('resources/start_icon.png'))
        self.start_btn.clicked.connect(self.start_sorting)
        main_layout.addWidget(self.start_btn)

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

    def get_selected_formats(self):
        """Получение выбранных форматов"""
        selected_formats = []
        if self.png_checkbox.isChecked():
            selected_formats.append('.png')
        if self.jpg_checkbox.isChecked():
            selected_formats.append('.jpg')
        if self.jpeg_checkbox.isChecked():
            selected_formats.append('.jpeg')
        if self.raw_checkbox.isChecked():
            selected_formats.append('.raw')
        if self.nef_checkbox.isChecked():
            selected_formats.append('.nef')
        return selected_formats

    def start_sorting(self):
        """Начало сортировки фотографий"""
        if not self.source_dir or not self.target_dir:
            self.status_label.setText(self.tr('Please select both source and target directories.'))
            return

        if not self.sorting_mode:
            # Режим отбора файлов
            self.status_label.setText(self.tr('Scanning files...'))
            self.progress_bar.setValue(0)

            # Получаем выбранные форматы
            selected_formats = self.get_selected_formats()

            # Фильтруем файлы по выбранным форматам
            self.files_to_sort = [f for f in os.listdir(self.source_dir) if any(f.lower().endswith(ext) for ext in selected_formats)]

            # Подсчёт количества файлов каждого формата
            format_counts = {}
            for ext in selected_formats:
                count = sum(1 for f in self.files_to_sort if f.lower().endswith(ext))
                if count > 0:
                    format_counts[ext] = count

            # Отображение информации о файлах
            file_info = "File Counts:\n"
            for ext, count in format_counts.items():
                file_info += f"{ext}: {count} files\n"

            # Открываем окно с информацией
            info_dialog = FileInfoDialog(file_info, self)
            info_dialog.exec()

            # Переключаем режим кнопки
            self.sorting_mode = True
            self.start_btn.setText("Confirm and Start Sorting")
            self.status_label.setText(self.tr('Files scanned. Press "Confirm and Start Sorting" to begin.'))
        else:
            # Режим сортировки
            self.status_label.setText(self.tr('Sorting started...'))
            self.progress_bar.setValue(0)

            total_photos = len(self.files_to_sort)
            processed = 0

            for photo in self.files_to_sort:
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
                                # Обновляем лог перемещения файлов
                                self.log_text_edit.append(f"Moved: {photo} -> {target_folder}")
                                break
                except Exception as e:
                    print(f'Error processing file {photo}: {e}')

                processed += 1
                self.progress_bar.setValue(int((processed / total_photos) * 100))

            self.status_label.setText(self.tr('Sorting completed!'))
            self.sorting_mode = False
            self.start_btn.setText("Start Sorting")

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

    def set_language(self, language):
        """Установка языка интерфейса"""
        # Пример: можно добавить поддержку нескольких языков
        QMessageBox.information(self, 'Language', f'Language set to {language}.')

    def reset_settings(self):
        """Сброс настроек к значениям по умолчанию"""
        self.dark_theme = False
        self.setStyleSheet(light_stylesheet)
        QMessageBox.information(self, 'Reset Settings', 'Settings reset to default.')
# LIGHT theme
light_stylesheet = """
    QWidget {
        background-color: #ffffff;
        color: #333333;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
    }
    QPushButton {
        background-color: #f0f0f0;
        color: #333333;
        border: 1px solid #cccccc;
        border-radius: 4px;
        padding: 8px 16px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #e0e0e0;
    }
    QPushButton:pressed {
        background-color: #d0d0d0;
    }
    QProgressBar {
        border: 1px solid #cccccc;
        border-radius: 5px;
        text-align: center;
        background-color: #f0f0f0;
    }
    QProgressBar::chunk {
        background-color: #4caf50;
        border-radius: 4px;
    }
    QLabel {
        color: #333333;
        font-size: 14px;
    }
    QMenuBar {
        background-color: #ffffff;
        color: #333333;
        border-bottom: 1px solid #cccccc;
    }
    QMenuBar::item {
        background-color: transparent;
        padding: 8px 16px;
    }
    QMenuBar::item:selected {
        background-color: #e0e0e0;
    }
    QMenu {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #cccccc;
    }
    QMenu::item {
        padding: 8px 16px;
    }
    QMenu::item:selected {
        background-color: #e0e0e0;
    }
    QLineEdit {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #cccccc;
        border-radius: 4px;
        padding: 8px;
    }
    QLineEdit:focus {
        border: 1px solid #4caf50;
    }
"""

# DARK theme
dark_stylesheet = """
    QWidget {
        background-color: #2d2d2d;
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
    }
    QPushButton {
        background-color: #3d3d3d;
        color: #ffffff;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 8px 16px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #4d4d4d;
    }
    QPushButton:pressed {
        background-color: #5d5d5d;
    }
    QProgressBar {
        border: 1px solid grey;
        border-radius: 5px;
        text-align: center;
        background-color: #f0f0f0;
    }
    QProgressBar::chunk {
        background-color: #4caf50;
        border-radius: 4px;
    }
    QLabel {
        color: #ffffff;
        font-size: 14px;
    }
    QMenuBar {
        background-color: #2d2d2d;
        color: #ffffff;
        border-bottom: 1px solid #555555;
    }
    QMenuBar::item {
        background-color: transparent;
        padding: 8px 16px;
    }
    QMenuBar::item:selected {
        background-color: #4d4d4d;
    }
    QMenu {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #555555;
    }
    QMenu::item {
        padding: 8px 16px;
    }
    QMenu::item:selected {
        background-color: #4d4d4d;
    }
    QLineEdit {
        background-color: #3d3d3d;
        color: #ffffff;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 8px;
    }
    QLineEdit:focus {
        border: 1px solid #4caf50;
    }
"""

# PROGRESS BAR style
progress_bar_style = """
    QProgressBar {
        border: 1px solid grey;
        border-radius: 5px;
        text-align: center;
        background-color: #f0f0f0;
    }
    QProgressBar::chunk {
        background-color: #4caf50;
        border-radius: 4px;
    }
""" 
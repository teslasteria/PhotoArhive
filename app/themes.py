dark_stylesheet = """
    QWidget {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    QPushButton {
        background-color: #3d3d3d;
        color: #ffffff;
        border: 1px solid #555;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #555;
    }
    QProgressBar {
        border: 2px solid grey;
        border-radius: 5px;
        text-align: center;
        background-color: #444;
    }
    QProgressBar::chunk {
        background-color: green;
        width: 10px;
    }
    QLabel {
        color: #ffffff;
    }
"""

light_stylesheet = """
    QWidget {
        background-color: #ffffff;
        color: #000000;
    }
    QPushButton {
        background-color: #f0f0f0;
        color: #000000;
        border: 1px solid #ccc;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #ddd;
    }
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
    QLabel {
        color: #000000;
    }
"""
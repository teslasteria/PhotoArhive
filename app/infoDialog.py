from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton


# Info about files those are about to be sorted
class FileInfoDialog(QDialog):
    def __init__(self, file_info, parent=None):
        super().__init__(parent)
        self.setWindowTitle("File Information")
        self.setGeometry(200, 200, 600, 300)

        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setText(file_info)
        layout.addWidget(self.text_edit)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)
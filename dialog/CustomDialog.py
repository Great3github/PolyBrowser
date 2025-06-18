from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox, QDialog, QLabel,QDialogButtonBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
class NewYesNoDialog(QDialog):
    def __init__(self, title, text):
        super().__init__()

        self.setWindowTitle(title)

        QBtn = QDialogButtonBox.No | QDialogButtonBox.Yes

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel(text)
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
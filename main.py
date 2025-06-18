import subprocess
from msg import cmdconfig, msgconfig
import browser_config
from subprocess import DEVNULL, STDOUT
try: subprocess.run(cmdconfig.installcmd, stdout=DEVNULL, stderr=DEVNULL)
except Exception as e: print(msgconfig.ErrorMsg.defaultError)
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox, QDialog, QLabel,QDialogButtonBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys
from dialog import CustomDialog


class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(100, 100, 1000, 600)
        dlg = CustomDialog.NewYesNoDialog(msgconfig.openBrowserConfirmation[0], msgconfig.openBrowserConfirmation[1])
        dlg_out = dlg.exec_()
        if dlg_out == QMessageBox.Yes: pass
        if dlg_out == QMessageBox.No: exit(1)
        # Create browser widget
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(browser_config.startingpage))
        self.showFullScreen()
        # Create navigation bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_home)
        self.url_bar.setDisabled(True)
        self.go_btn = QPushButton(msgconfig.ButtonText.homeButton)
        self.go_btn.clicked.connect(self.navigate_to_home)

        self.back_btn = QPushButton(msgconfig.ButtonText.backButton)
        self.back_btn.clicked.connect(self.browser.back)

        self.forward_btn = QPushButton(msgconfig.ButtonText.forwardButton)
        self.forward_btn.clicked.connect(self.browser.forward)

        self.refresh_btn = QPushButton(msgconfig.ButtonText.refreshButton)
        self.refresh_btn.clicked.connect(self.browser.reload)

        # Layout for navigation bar
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.forward_btn)
        nav_layout.addWidget(self.refresh_btn)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(self.go_btn)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.browser)

        # Main widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Update URL bar when URL changes
        self.browser.urlChanged.connect(self.update_url_bar)

    def navigate_to_home(self):
        
        self.browser.setUrl(QUrl(browser_config.homepage))

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())
        if str(self.browser.url().toString()).startswith(tuple(browser_config.url_blocklist)):
            self.browser.setUrl(QUrl(browser_config.homepage))
            self.showOkdialog(msgconfig.ErrorMsg.siteBlockedError[0], msgconfig.ErrorMsg.siteBlockedError[1])
        
    def showOkDialog(self, title, text):
        dialog = QMessageBox(self)
        dialog.setWindowTitle(str(title))
        dialog.setText(str(text))
        dialog.setStandardButtons(QMessageBox.Ok)

        
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleBrowser()
    window.show()
    sys.exit(app.exec_())

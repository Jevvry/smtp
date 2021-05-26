import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Login(QWidget):
    theSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.login_line = QLineEdit(self)
        self.password = QLineEdit(self)
        self.setWindowTitle('Login')
        self.login_btn = QPushButton("enter", self)
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(300, 350)
        self.login_line.setGeometry(10, 100, 280, 30)
        font = self.login_line.font()
        font.setPointSize(15)
        self.login_line.setFont(font)
        self.login_line.setPlaceholderText("login")

        self.password.setGeometry(10, 150, 280, 30)
        font = self.password.font()
        font.setPointSize(15)
        self.password.setFont(font)
        self.password.setPlaceholderText("password")

        self.login_btn.setGeometry(10, 200, 280, 30)
        font = self.login_btn.font()
        font.setPointSize(15)
        self.login_btn.setStyleSheet('QPushButton {color: gray;}')
        self.login_btn.setFont(font)
        self.login_btn.clicked.connect(self.submit)

    def submit(self):
        self.theSignal.emit(f"{self.login_line.text()}:{self.password.text()}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    sys.exit(app.exec_())

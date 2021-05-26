import sys
from PyQt5.QtWidgets import *
import login_window
import smtp_client
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Main(QWidget):

    def __init__(self):
        super().__init__()

        self.attachments = []
        self.log_window = login_window.Login()
        self.log_window.show()
        self.log_window.theSignal.connect(self.s_login)
        self.login = ""
        self.password = ""

        self.to_line = QLineEdit(self)
        self.from_line = QLineEdit(self)
        self.setWindowTitle('Client')
        self.send_btn = QPushButton("send", self)
        self.attach_btn = QPushButton("attach file", self)
        self.subject_line = QLineEdit(self)
        self.msg = QTextEdit(self)
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(450, 570)
        self.to_line.setGeometry(10, 20, 430, 30)
        font = self.to_line.font()
        font.setPointSize(15)
        self.to_line.setFont(font)
        self.to_line.setPlaceholderText("To")

        self.from_line.setGeometry(10, 70, 430, 30)
        font = self.from_line.font()
        font.setPointSize(15)
        self.from_line.setFont(font)
        self.from_line.setPlaceholderText("From")

        self.subject_line.setGeometry(10, 120, 430, 30)
        font = self.subject_line.font()
        font.setPointSize(15)
        self.subject_line.setFont(font)
        self.subject_line.setPlaceholderText("Subject")

        self.msg.setGeometry(10, 170, 430, 300)
        font = self.msg.font()
        font.setPointSize(15)
        self.msg.setFont(font)

        self.send_btn.setGeometry(10, 480, 430, 30)
        font = self.send_btn.font()
        font.setPointSize(15)
        self.send_btn.setStyleSheet('QPushButton {color: gray;}')
        self.send_btn.setFont(font)
        self.send_btn.clicked.connect(self.send)

        self.attach_btn.setGeometry(10, 520, 430, 30)
        font = self.attach_btn.font()
        font.setPointSize(15)
        self.attach_btn.setStyleSheet('QPushButton {color: gray;}')
        self.attach_btn.setFont(font)
        self.attach_btn.clicked.connect(self.show_dialog)

    def s_login(self, log_pass):
        l_p = log_pass.split(":")
        self.login = l_p[0]
        self.password = l_p[1]
        self.log_window.hide()
        self.show()

    def send(self):
        client = smtp_client.SmtpClient(self.login, self.password, self.subject_line.text(), self.msg.toPlainText(),
                                        self.attachments, self.to_line.text(), self.from_line.text())
        client.send()

    def show_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home',
                                            filter="Images (*.png *.jpg);;Text files (*.txt);;Media (*.mp3)")[0]
        self.attachments.append(fname)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())

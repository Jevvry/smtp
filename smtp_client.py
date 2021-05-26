import socket
from ssl import wrap_socket
from base64 import b64encode


class SmtpClient:
    Address = "smtp.yandex.ru"
    Port = 465
    Timeout = 1

    mime_types = {"png": "image/png", "jpg": "image/png", "mp3": "audio/mpeg"}

    def __init__(self, log, pasw, sbj, text, attachments, receivers,frm):
        self.boundary = "----==--bound.8833.web38o.yandex.ru"
        self.login = log.encode()
        self.passw = pasw.encode()
        self.text = text
        self.receivers = receivers
        self.subject = sbj
        self.attachments = attachments
        self.frm = frm

    def get_attachments(self):
        attachments = ''
        for attachment in self.attachments:
            filename = attachment.strip()

            mime_type = self.mime_types[filename.slpit(".")[-1]]
            with open(filename, 'rb') as f:
                filename = filename.slpit("/")[-1]
                file = b64encode(f.read())
                attachments += (f'Content-Disposition: attachment; filename="{filename}"\n'
                                'Content-Transfer-Encoding: base64\n'
                                f'Content-Type: {mime_type}; name="{filename}"\n\n'
                                ) + file.decode() + f'\n--{self.boundary}'
        return attachments

    def get_msg(self):
        if not all(ord(i) < 128 for i in self.subject):
            self.subject = f'=?utf-8?B?{b64encode(self.subject.encode()).decode()}?='

        if self.text[0] == '.':
            self.text = '.' + self.text
        self.text = self.text.replace("\n.", "\n..")

        login = self.login.decode()
        message = (
            f"From: {self.frm} {login}\n"
            f"To: {self.receivers}\n"
            f"Subject: {self.subject}\n"
            "MIME-Version: 1.0\n"
            f'Content-Type: multipart/mixed; boundary="{self.boundary}"\n\n'
            f"--{self.boundary}\n"
            "Content-Type: text/plain; charset=utf-8\n"
            "Content-Transfer-Encoding: 8bit\n\n"
            f"{self.text}\n"
            f"--{self.boundary}\n"
            f"{self.get_attachments()}--\n."
        )
        return message

    def request(self, sock, cmd, buffer_size=65000):
        rs = sock.recv(buffer_size).decode()
        sock.send(cmd + b'\n')
        return rs

    def send(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock = wrap_socket(sock)
            sock.settimeout(float(self.Timeout))
            sock.connect((self.Address, self.Port))

            print(self.request(sock, b'EHLO test'))

            print(self.request(sock, b'AUTH LOGIN'))
            print(self.request(sock, b64encode(self.login)))
            print(self.request(sock, b64encode(self.passw)))

            print(self.request(sock, b'MAIL FROM: ' + self.login))

            for recipient in self.receivers.split(","):
                print(self.request(sock, b'RCPT TO: ' + recipient.encode()))

            print(self.request(sock, 'DATA'.encode()))

            print(self.request(sock, (self.get_msg() + "\n.").encode()))
            print(sock.recv(65000).decode())

import base64
import os
import socket
import ssl
from getpass import getpass
from pathlib import Path

from mail_creator import MailCreator
from file import File
from server_answer import ServerAnswer
from SMTPException import SMTPException


class Client:
    def __init__(self, login_from: str, to: str, subject: str, is_ssl: bool, do_auth: bool, do_verbose: bool,
                 directory: str, server_port: str):

        self.login_from = login_from
        self.to = to
        self.subject = subject
        self.is_ssl = is_ssl
        self.do_auth = do_auth
        self.do_verbose = do_verbose
        self.dir = Path(directory)
        server_port = server_port.split(':')
        self.server = server_port[0]
        self.port = int(server_port[1])

        if self.do_auth:
            self.password = getpass()

        self.commands = []
        self.set_commands()

    def set_commands(self):
        if self.do_auth:
            self.commands = [f'EHLO {self.login_from.replace("@", ".")}\n', 'auth login\n',
                             f'{base64.b64encode(self.login_from.encode("utf-8")).decode("utf-8")}\n',
                             f'{base64.b64encode(self.password.encode("utf-8")).decode("utf-8")}\n',
                             f'MAIL FROM: <{self.login_from}>\nRCPT TO: <{self.to}>\nDATA\n']
        else:
            self.commands = [f'EHLO {self.login_from.replace("@", ".")}\n',
                             f'MAIL FROM: <{self.login_from}>\nRCPT TO: <{self.to}>\nDATA\n']

    def create_mail(self):
        mail_creator = MailCreator()
        mail_creator.add_header(self.login_from, self.to, self.subject)
        files = self.get_images()
        for i, file in enumerate(files):
            if i == len(files) - 1:
                mail_creator.add_content(file, True)
            else:
                mail_creator.add_content(file, False)

        return mail_creator.get_mail()

    def get_images(self):
        return [File(Path(self.dir / filename)) for filename in os.listdir(self.dir) if
                filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.gif')]

    def recv_msg(self, sock: socket):
        msg = sock.recv(1024).decode('utf-8')
        ans = ServerAnswer(msg)
        if ans.last_code > 499:
            raise Exception(ans.all_msg)

        if self.do_verbose:
            print(f'Server: {msg}')

    def send_msg(self, sock: socket, msg: str):
        if self.do_verbose:
            print(f'You: {msg}')
        sock.send(msg.encode())

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.server, self.port))
            self.recv_msg(sock)
            if self.is_ssl:
                self.send_msg(sock, f'EHLO {self.login_from.replace("@", ".")}\n')
                self.recv_msg(sock)
                self.send_msg(sock, 'starttls\n')
                self.recv_msg(sock)
                sock = ssl.wrap_socket(sock)
            for command in self.commands:
                self.send_msg(sock, command)
                self.recv_msg(sock)
                if 'DATA' in command:
                    sock.send(self.create_mail().encode())
                    self.recv_msg(sock)

        except SMTPException as e:
            print(e)
        finally:
            sock.close()

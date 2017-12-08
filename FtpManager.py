from ftplib import FTP, error_perm
from socket import timeout
from os import listdir, chdir, sep, getcwd
import os

class FtpManager:

    def __init__(self, address, user, password, remote_backup_dir):
        self.address = address
        self.user = user
        self.password = password
        self.remote_dir = remote_backup_dir
        self.connection = None

    def connect(self):
        try:
            try:
                self.connection = FTP(self.address, timeout=5)
            except timeout:
                print("host is down, please check the address")
                exit(code=0)
            self.connection.login(user=self.user, passwd=self.password)
        except error_perm:
            print("access denied, check credentials")
            exit(code=0)

    def upload(self, path):
        files = listdir(path)
        chdir(path)
        for file in files:
            print(getcwd() + sep + file)
            if os.path.isfile(getcwd() + sep + file):
                fh = open(file, 'rb')
                self.connection.storbinary('STOR %s' % file, fh)
                fh.close()
            elif os.path.isdir(getcwd() + sep + file):
                self.connection.mkd(file)
                self.connection.cwd(file)
                self.upload(getcwd() + sep + file)

f = FtpManager("200.10.1.3", "dennis", "1q2w3e4R", None)
f.connect()
f.upload("docker")
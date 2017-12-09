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
                print("Host is down, please check the address")
                exit(code=0)
            self.connection.login(user=self.user, passwd=self.password)
            print("CWD", self.remote_dir)
            self.connection.cwd(self.remote_dir)
        except error_perm:
            print("Access denied, please check credentials")
            exit(code=0)

    def upload(self, path):
        print path
        for name in os.listdir(path):
            localpath = os.path.join(path, name)
            if os.path.isfile(localpath):
                print("STOR", name, localpath)
                self.connection.storbinary('STOR ' + name, open(localpath, 'rb'))
            elif os.path.isdir(localpath):
                print("MKD", name)

                try:
                    self.connection.mkd(name)

                # ignore "directory already exists"
                except error_perm as e:
                    if not e.args[0].startswith('550'):
                        raise

                print("CWD", name)
                self.connection.cwd(name)
                self.upload(localpath)
                print("CWD", "..")
                self.connection.cwd("..")

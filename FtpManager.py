from ftplib import FTP, error_perm
from socket import timeout
from os import listdir, chdir, path.is

class FtpManager:

    def __init__(self, address, user, password, remote_backup_dir):
        self.address = address
        self.user = user
        self.password = password
        self.local_dir = ""
        self.remote_dir = remote_backup_dir
        self.connection = ""

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
        return True

    def upload(self, path):
        self.local_dir = path
        files = listdir(self.local_dir)
        chdir(self.local_dir)
        for file in files:
            if path.isfile(path + r"\{0}".format(file)):
                fh = open(file, 'rb')
                self.connection.storbinary('STOR %s' % file, fh)
                fh.close()
            elif path.isdir(path + r'\{}'.format(file)):
                self.connection.mkd(f)
                self.connection.cwd(f)
                self.upload(path + r'\{}'.format(file))
        self.connection.cwd('..')
        chdir('..')



f = FtpManager("200.10.1.3", "dennis", "1q2w3e4R", None)
f.upload("docker")

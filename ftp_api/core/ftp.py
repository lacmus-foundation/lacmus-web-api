import subprocess

class FTPServer():

    @staticmethod
    def create_user(login:str, password:str):
        encrypted = subprocess.check_output(['openssl','passwd','-1',password],universal_newlines=True)[:-1]
        subprocess.check_call(['useradd',
                               '--password', encrypted,
                               '--shell','/usr/sbin/nologin',
                               '--gid','users',
                               login])

        subprocess.check_call(['mkdir', '/home/%s'%login])
        subprocess.check_call(['chown', '%s:users'%login,'/home/%s'%login])

import subprocess
import os
from commons.config import ROOT_FTP_FOLDER


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

    @staticmethod
    def mkdir_exists_ok(path_name,mode):
        try:
            os.mkdir(path_name,mode=0o750) # root folder can be read and write
        except OSError:
            if not os.path.isdir(path_name):
                raise

    @staticmethod
    def create_project(users:list,id:str,description:str):
        # there could be fails on different steps, so method designed as re-entrant
        # todo - check first users actually exists (requires DB also)
        root_project_path = os.path.join(ROOT_FTP_FOLDER,'project-%s'%id)
        FTPServer.mkdir_exists_ok(root_project_path,0o750)
        subprocess.check_call(['chmod', 'g+w', root_project_path])
        [FTPServer.mkdir_exists_ok(os.path.join(root_project_path,i),0o750)
            for i in ['result','description']]
        group_name = id # todo: short id from DB
        subprocess.check_call(['groupadd','--force',group_name])
        f = open(os.path.join(root_project_path,'description','description.txt'),"wt")
        f.write(description)
        f.close()
        subprocess.check_call(['chgrp', '-R', group_name, root_project_path])
        for user in users:
            subprocess.check_call(['usermod','-a','-G',group_name,user])
            # todo - add admins to all project groups (groups are in db)

        return root_project_path

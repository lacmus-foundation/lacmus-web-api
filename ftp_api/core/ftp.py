import subprocess
import os
from pwd import getpwuid
from commons.config import ROOT_FTP_FOLDER
import logging


class FTPServer():

    @staticmethod
    def create_user(login: str, password: str):
        logging.info("creating user request received for user %s" % login)
        encrypted = subprocess.check_output(['openssl', 'passwd', '-1', password], universal_newlines=True)[:-1]
        try:
            subprocess.check_call(['useradd',
                                   '--password', encrypted,
                                   '--shell', '/usr/sbin/nologin',
                                   '--gid', 'users',
                                   login])
        except subprocess.CalledProcessError as ex:
            if (ex.returncode == 9):
                logging.warning(
                    "User %s already exists on FTP. This shouldn't happen in production, only in debug" % login)
                return
            else:
                logging.error(logging.error("subprocess non-zero return code while creating os user", exc_info=True))
                raise ex
        except Exception as ex:
            logging.error(logging.error("Exception while creating os user", exc_info=True))
            raise ex

        logging.info("user created, creating home dir")
        try:
            subprocess.check_call(['mkdir', '/home/%s' % login])
            subprocess.check_call(['chown', '%s:users' % login, '/home/%s' % login])
        except Exception as ex:
            logging.error(logging.error("Exception while creating home dirs", exc_info=True))
            raise ex

    @staticmethod
    def mkdir_exists_ok(path_name):
        try:
            os.mkdir(path_name, mode=0o750)  # root folder can be read and write
        except OSError:
            if not os.path.isdir(path_name):
                logging.error("exception while creating dir %s" % path_name)
                raise

    @staticmethod
    def get_project_path(id: str):
        return os.path.join(ROOT_FTP_FOLDER, 'project-%s' % id)

    @staticmethod
    def create_project(users: list, id: str, description: str):
        # there could be fails on different steps, so method designed as re-entrant
        # todo - check first users actually exists (requires DB also)
        root_project_path = FTPServer.get_project_path(id)
        logging.info("create project request processing - creating dirs in %s" % root_project_path)
        FTPServer.mkdir_exists_ok(root_project_path)
        subprocess.check_call(['chmod', 'g+w', root_project_path])
        [FTPServer.mkdir_exists_ok(os.path.join(root_project_path, i))
         for i in ['result', 'description', 'error']]
        [FTPServer.mkdir_exists_ok(os.path.join(root_project_path, 'result', i))
         for i in ['empty', 'found']]
        group_name = 'project%s' % id
        logging.info("creating group %s" % group_name)
        subprocess.check_call(['groupadd', '--force', group_name])
        logging.info("writing description")
        f = open(os.path.join(root_project_path, 'description', 'description.txt'), "wt")
        f.write(description)
        f.close()
        logging.info("Assigning permissions")
        subprocess.check_call(['chgrp', '-R', group_name, root_project_path])
        for user in users:
            subprocess.check_call(['usermod', '-a', '-G', group_name, user])
            # todo - add admins to all project groups (groups are in db)

        return root_project_path

    @staticmethod
    def move_file_to_error(path: str, filename: str):
        to_path = os.path.join(path, 'error')
        logging.info("moving from %s to %s " % (os.path.join(path, filename),os.path.join(to_path, filename) ))
        os.rename(os.path.join(path, filename), os.path.join(to_path, filename))

    @staticmethod
    def remove_file(path: str, filename: str):
        logging.info("Removing %s" % (os.path.join(path, filename)))
        os.remove(os.path.join(path, filename))

    @staticmethod
    def get_user_login(path: str, filename: str) -> str:
        return getpwuid(os.stat(os.path.join(path, filename)).st_uid).pw_name

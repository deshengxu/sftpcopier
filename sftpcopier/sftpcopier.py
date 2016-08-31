import sys
import os
import paramiko
import logging
import time
from stat import S_ISDIR
import shutil

sys.path.append(".")
try:
    import util
except:
    from . import util

def get_local_file_list(folder):
    onlyfiles = [f for f in os.listdir(folder)
                 if os.path.isfile(os.path.join(folder, f))]
    return onlyfiles

def get_local_folder_list(folder):
    onlyfolders = [f for f in os.listdir(folder)
                 if not os.path.isfile(os.path.join(folder, f))]
    return onlyfolders

def get_remote_file_list(ftp, folder):
    onlyfiles = []
    for i in ftp.listdir(folder):
        #print(i, ftp.lstat(i))
        full_path = os.path.join(folder, i)
        lstatout = str(ftp.lstat(full_path)).split()[0]
        if 'd' not in lstatout:
            onlyfiles.append(i)
    return onlyfiles

def get_remote_folder_list(ftp, folder):
    onlyfolders = []
    for i in ftp.listdir(folder):
        full_path = os.path.join(folder,i)
        lstatout = str(ftp.lstat(full_path)).split()[0]
        if 'd' in lstatout:
            onlyfolders.append(i)
    return onlyfolders

def ftp_upload(ftp):
    remote_path = r'uditransfer/temp/localoutbox'
    if not remote_path.endswith(r'/'):
        remote_path += r'/'

    local_path = r'D:\ptc\Windchill_10.2\Windchill\temp\filedropfdacommunications\out'
    local_files = get_local_file_list(local_path)
    for local_file in local_files:
        remote_file = remote_path + os.path.basename(local_file)
        ftp.put(os.path.join(local_path,local_file), remote_file)
        os.remove(os.path.join(local_path,local_file))
        logging.info("local file:%s" % local_file)
        logging.info("Remote file:%s" % remote_file)
        logging.info("Upload finished")

def ftp_download(ftp):
    remote_path = r'uditransfer/temp/localinbox'
    if not remote_path.endswith(r'/'):
        remote_path += r'/'

    local_path = r'D:\ptc\Windchill_10.2\Windchill\temp\filedropfdacommunications\in'

    remote_files = get_remote_file_list(ftp, remote_path)
    for remote_file in remote_files:
        local_file = os.path.join(local_path, remote_file)
        remote_file_full = remote_path + remote_file

        ftp.get(remote_file_full, local_file)
        ftp.remove(remote_file_full)
        logging.info(remote_file_full)
        logging.info(local_file)
        logging.info("Download finished")

def process_folders():
    sftpURL = 'gateway-nvirginia2.portal.ptc.io'
    sftpPort = 3697
    sftpUser = 'ppadmin'
    sftpPass = 'rFoY2hPk6?5X'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(sftpURL, username=sftpUser, password=sftpPass, port=sftpPort)

    ftp = ssh.open_sftp()
    ftp_upload(ftp)
    ftp_download(ftp)

    ssh.close()


def main():
    util.initialize_logger(".")
    try:
        while True:
            process_folders()
            logging.info("sleeping...\n\n")
            time.sleep(20)
    except KeyboardInterrupt:
        logging.info("Process stopped!")


if __name__=='__main__':
    main()

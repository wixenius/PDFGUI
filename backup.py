
from FTP.ftpDownAndUpload import downloadFile, uploadFile
from passwords import FILENAME

import time

def backup():
    downloadFile(FILENAME)
    uploadFile(FILENAME, 'parkingBackup', time.strftime('%Y%m%d'))

if __name__ == "__main__":
    backup()
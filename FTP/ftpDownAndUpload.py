from ftplib import FTP
from passwords import FTP_SERVER, FTP_USERNAME, FTP_PASSWORD, FILENAME

def downloadFile(FILENAME):

    try:

        ftp = FTP(FTP_SERVER, FTP_USERNAME, FTP_PASSWORD)     # connect to host, default port

        ftp.cwd('parking')

        ftp.retrbinary('RETR info.json', open(FILENAME, 'wb').write)

        ftp.quit()

        return True

    except:
        return False

def uploadFile(FILENAME):

    try:

        ftp = FTP(FTP_SERVER, FTP_USERNAME, FTP_PASSWORD)     # connect to host, default port

        ftp.cwd('parking')

        file = open(FILENAME, 'rb')                         # file to send
        ftp.storbinary("STOR " + 'info.json', file)            # send the file
        file.close()                                        # close file and FTP

        ftp.quit()

        return True

    except:
        return False


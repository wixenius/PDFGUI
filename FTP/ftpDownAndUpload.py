from ftplib import FTP
from passwords import FTP_DICT

def downloadFile(FILENAME):

    try:

        ftp = FTP(FTP_DICT['SERVER'], FTP_DICT['USERNAME'], FTP_DICT['PASSWORD'])     # connect to host, default port

        ftp.cwd('parking')

        ftp.retrbinary('RETR %s' % FILENAME, open(FILENAME, 'wb').write)

        ftp.quit()

        return True

    except:
        return False

def uploadFile(FILENAME, folder='parking', filenameExtension=''):

    try:

        ftp = FTP(FTP_DICT['SERVER'], FTP_DICT['USERNAME'], FTP_DICT['PASSWORD'])     # connect to host, default port

        ftp.cwd(folder)

        file = open(FILENAME, 'rb')                         # file to send

        if filenameExtension:
            FILENAME = 'info_%s.json' % filenameExtension

        ftp.storbinary("STOR " + '%s' % FILENAME, file)     # send the file
        file.close()                                        # close file and FTP

        ftp.quit()

        return True

    except:
        return False


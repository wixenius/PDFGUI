import json
from FTP.ftpDownAndUpload import uploadFile, downloadFile
from passwords import FILENAME


def listToCommaSeperatedString(list):
    s = ''

    for idx, item in enumerate(list):
        if idx != 0:
            s += ','

        s += str(item)

    return s

def updateFile_PaidUnpaid(apartmentNumber, lPaid, lUnpaid):

    if downloadFile(FILENAME) == False:
        return False

    with open(FILENAME) as data_file:
        data = json.load(data_file)

    if apartmentNumber.upper() in data.keys():
        data[apartmentNumber.upper()]['paid'] = lPaid
        data[apartmentNumber.upper()]['unpaid'] = lUnpaid

        with open(FILENAME, 'w') as outfile:
            json.dump(data, outfile)

        if uploadFile(FILENAME) == False:
            return False

def updateFile_Email(apartmentNumber, lEmail):

    if downloadFile(FILENAME) == False:
        return False

    with open(FILENAME) as data_file:
        data = json.load(data_file)

    if apartmentNumber.upper() in data.keys():
        data[apartmentNumber.upper()]['email'] = lEmail

        with open(FILENAME, 'w') as outfile:
            json.dump(data, outfile)

        if uploadFile(FILENAME) == False:
            return False

    return True

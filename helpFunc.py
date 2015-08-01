import json
from FTP.parseInfo import FILENAME
from FTP.ftpDownAndUpload import uploadFile


def listToCommaSeperatedString(list):
    s = ''

    for idx, item in enumerate(list):
        if idx != 0:
            s += ','

        s += str(item)

    return s

def updateFile_PaidUnpaid(apartmentNumber, lPaid, lUnpaid):

    with open(FILENAME) as data_file:
        data = json.load(data_file)

    if apartmentNumber.upper() in data.keys():
        data[apartmentNumber.upper()]['paid'] = lPaid
        data[apartmentNumber.upper()]['unpaid'] = lUnpaid

        with open(FILENAME, 'w') as outfile:
            json.dump(data, outfile)

        uploadFile(FILENAME)

def updateFile_Email(apartmentNumber, lEmail):

    with open(FILENAME) as data_file:
        data = json.load(data_file)

    if apartmentNumber.upper() in data.keys():
        data[apartmentNumber.upper()]['email'] = lEmail

        with open(FILENAME, 'w') as outfile:
            json.dump(data, outfile)

        uploadFile(FILENAME)

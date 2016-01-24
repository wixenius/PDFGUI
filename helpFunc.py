import json, pprint
from FTP.ftpDownAndUpload import uploadFile, downloadFile
from passwords import FILENAME
from collections import OrderedDict


def listToCommaSeperatedString(list):
    s = ''

    for idx, item in enumerate(list):
        if idx != 0:
            s += ','

        s += str(item)

    return s

def updateFile_PaidUnpaid(apartmentNumber, dPaid_Date, lUnpaid):

    ret = downloadFile(FILENAME)
    while ret == False:
        ret = downloadFile(FILENAME)

    with open(FILENAME) as data_file:
        data = json.load(data_file)

    if apartmentNumber.upper() in data.keys():
        data[apartmentNumber.upper()]['paid'] = dPaid_Date
        data[apartmentNumber.upper()]['unpaid'] = lUnpaid

        with open(FILENAME, 'w') as outfile:
            pprint.pprint(data, outfile)

        replaceCitationInFile()

        ret = uploadFile(FILENAME)
        while ret == False:
            ret = uploadFile(FILENAME)

def updateFile_Email(apartmentNumber, lEmail):

    ret = downloadFile(FILENAME)
    while ret == False:
        ret = downloadFile(FILENAME)

    with open(FILENAME) as data_file:
        data = json.load(data_file)

    if apartmentNumber.upper() in data.keys():
        data[apartmentNumber.upper()]['email'] = lEmail

        with open(FILENAME, 'w') as outfile:
            pprint.pprint(data, outfile)

        replaceCitationInFile()

        ret = uploadFile(FILENAME)
        while ret == False:
            ret = uploadFile(FILENAME)

def replaceCitationInFile():
    f = open(FILENAME,'r')
    filedata = f.read()
    f.close()

    newdata = filedata.replace("'",'"')

    f = open(FILENAME,'w')
    f.write(newdata)
    f.close()
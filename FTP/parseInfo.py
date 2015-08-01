import json

from passwords import FILENAME
from helpFunc import listToCommaSeperatedString


def parseInfo(apartmentNumber):

    with open(FILENAME) as data_file:
        data = json.load(data_file)

    if apartmentNumber.upper() in data.keys():
        return data[apartmentNumber.upper()]
    else:
        return False

def returnCSVEmail():
    with open(FILENAME) as data_file:
        data = json.load(data_file)

    lEmail = []

    for key in data.keys():
        lEmail.extend(data[key]['email'])

    return listToCommaSeperatedString(lEmail)

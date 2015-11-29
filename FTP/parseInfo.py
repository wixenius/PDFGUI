import json

from helpFunc import listToCommaSeperatedString
from passwords import FILENAME


def returnData():
    with open(FILENAME) as data_file:
        data = json.load(data_file)

    return data


def parseInfo(apartmentNumber):

    with open(FILENAME) as data_file:
        data = json.load(data_file)

    if apartmentNumber.upper() in data.keys():
        return data[apartmentNumber.upper()]
    else:
        return False


def returnCSVEmail(specificHouse = None):
    with open(FILENAME) as data_file:
        data = json.load(data_file)

    lEmail = []

    for key in data.keys():
        if specificHouse:
            if not key.startswith(specificHouse):
                continue

        lEmail.extend(data[key]['email'])

    return listToCommaSeperatedString(lEmail)

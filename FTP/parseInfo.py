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

def returnCSVEmail(specificHouse = None):
    with open(FILENAME) as data_file:
        data = json.load(data_file)

    lEmail = []

    for key in data.keys():
        if specificHouse:
            if not key.startswith(specificHouse):
                continue

        print (key)
        lEmail.extend(data[key]['email'])


    return listToCommaSeperatedString(lEmail)

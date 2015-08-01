import json

from passwords import FILENAME


def parseInfo(apartmentNumber):

    with open(FILENAME) as data_file:
        data = json.load(data_file)

    if apartmentNumber.upper() in data.keys():
        return data[apartmentNumber.upper()]
    else:
        return False

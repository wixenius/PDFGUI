import logging

class Logger:

    def __init__(self):
        logging.basicConfig(filename='example.log', level=logging.DEBUG, format='%(levelname)s %(asctime)s : %(message)s')

    def log(self, stringToLog):
        logging.error(stringToLog)

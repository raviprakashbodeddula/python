import configparser
import logging, logging.config
import sys
import os
import datetime
import random

class Base:
    i = 10

    def __init__(self):
        self.filename = os.path.basename(__file__)
        self.filename_no_ext = os.path.splitext(self.filename)[0]
        self.ini_filename = self.filename_no_ext + '.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.ini_filename)
        logging.config.fileConfig(self.ini_filename)
        self.logger = logging.getLogger('')
        self.logger.info('jdgjsgjdggdskf')

b=Base()
b.logger.debug("knkngfdkfngkfng")

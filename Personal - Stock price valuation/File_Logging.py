# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 11:56:00 2020

@author: Jesse
"""

import logging
import sys
import datetime
import logging.config
import logging.handlers

class FileLogging:
    """
    Standard logger object that creates three logging files:
        1. current_info_logging.log
            Contains all information of the previous time a script was running.
        2. info_logging.log
            Contains all information of complete history of the execution of the script.
        3. error_logging.log
            Contains all information of complete history of the errors and critical errors that occured in the script.
            Delete manually after occurrence of the errors is fixed.
    The file also outputs to std.output using limited formatting.
   
    Logging levels are as following, according to https://docs.python.org/2/library/logging.html:    
    CRITICAL : 50
    ERROR: 40
    WARNING: 30
    INFO: 20
    DEBUG: 10
    NOTSET: 0
    """    
    def __init__(self,logger_name = 'root',directory='',stream_on = False):
        if directory.isalpha():
            sys.stdout.write('CRITICAL ERROR in FileLogging - the given directory is not a directory but a name!')
            sys.exit()
       
        #Creation time of the logger
        self.starting_datetime = datetime.datetime.now()

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s;%(name)s;%(levelname)s;%(message)s", "%Y-%m-%d %H:%M:%S")
        limited_formatter = logging.Formatter("%(message)s")
        logging.config.dictConfig({'version': 1, 'disable_existing_loggers': False})
       # self.logger.handlers = []
        if len(self.logger.handlers) == 0:
            try:      
                #Outputs messages above debug to standard output with limited formatting.
                if stream_on == True:
                    consoleHandler = logging.StreamHandler()    
                    consoleHandler.setLevel(logging.DEBUG)
                    consoleHandler.setFormatter(limited_formatter)
                    self.logger.addHandler(consoleHandler)
                   
                #Outputs messages above debug to a file, writing to a new file using complete formatting
                current_info_handler = logging.FileHandler('{}current_info_logging.log'.format(directory), mode='w')
                current_info_handler.setLevel(logging.DEBUG)
                current_info_handler.setFormatter(formatter)
               
                #Outputs messages above debug to a file, appending a previous file using complete formatting
                info_handler = logging.FileHandler('{}info_logging.log'.format(directory))
                info_handler.setLevel(logging.INFO)
                info_handler.setFormatter(formatter)
               
                #Outputs messages above error to a file, appending a previous file using complete formatting
                error_handler = logging.FileHandler('{}error_logging.log'.format(directory))
                error_handler.setLevel(logging.ERROR)
                error_handler.setFormatter(formatter)
               
                self.logger.addHandler(current_info_handler)
                self.logger.addHandler(info_handler)
                self.logger.addHandler(error_handler)
           
            except FileNotFoundError:
                del self.logger
                sys.stdout.write('CRITICAL ERROR - Creation of file logging object aborted! Folder {} does not exist, create such a directory!'.format(directory))
                sys.exit()
       
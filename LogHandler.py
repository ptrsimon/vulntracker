#!/usr/bin/python3
#
# LogHandler.py - write console or file logs
#

import Config
import datetime
from abc import ABC, abstractmethod

class LogHandler(ABC):
    loglevels = {
        0: "DEBUG",
        1: "INFO",
        2: "WARNING",
        3: "ERROR"
    }

    @abstractmethod
    def Write(self, msg, level):
        pass

class ConsoleLogHandler(LogHandler):
    def Write(self, msg, level):
        if level >= Config.AppConfig.loglevel:
            print("[{0}] {1} {2}".format(datetime.datetime.now(), self.loglevels[level], msg))

class FileLogHandler(LogHandler):
    def __init__(self, path):
        self.path = path

    def Write(self, msg, level):
        if level >= Config.AppConfig.loglevel:
            with open(self.path, 'a') as fh:
                fh.write("[{0}] {1} {2}\n".format(datetime.datetime.now(), self.loglevels[level], msg))

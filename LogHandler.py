#!/usr/bin/python3
#
# LogHandler.py - write console or file logs
#

import Config
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
            print("[{0}] {1}".format(self.loglevels[level], msg))

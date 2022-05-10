#!/usr/bin/python3
#
# AffectedVersion.py - describe a software version range
#

class AffectedVersion:
    def __init__(self, end_version=0, start_version=0, end_version_excluding=True, start_version_excluding=True):
        self.end_version = end_version
        self.end_version_excluding = end_version_excluding
        self.start_version = start_version
        self.start_version_excluding = start_version_excluding

    def __str__(self):

        printstr = ""
        if not self.start_version_excluding:
            printstr += "["
        else:
            printstr += "]"
        printstr += str(self.start_version)
        printstr += "-"
        printstr += str(self.end_version)
        if not self.start_version_excluding:
            printstr += "]"
        else:
            printstr += "["

        return printstr

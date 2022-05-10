#!/usr/bin/python3
#
# InventoryItem.py - describe a single inventory entry
#

class InventoryItem:
    def __init__(self, cpestring, severity, human_name):
        self.cpestring = cpestring
        self.severity = severity
        self.human_name = human_name

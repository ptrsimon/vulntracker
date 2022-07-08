#!/usr/bin/python3
#
# InventoryItem.py - describe a single inventory entry
#

class InventoryItem:
    def __init__(self, human_name):
        self.human_name = human_name

class CPEInventoryItem(InventoryItem):
    def __init__(self, cpestring, severity, human_name):
        self.cpestring = cpestring
        self.severity = severity
        super(CPEInventoryItem, self).__init__(human_name)

class KeywordInventoryItem(InventoryItem):
    def __init__(self, keyword, human_name):
        self.keyword = keyword
        super(KeywordInventoryItem, self).__init__(human_name)
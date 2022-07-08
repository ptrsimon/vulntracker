#!/usr/bin/python3
#
# InventoryHandler.py - parse and return inventory file (interesting software is defined here)
#

from InventoryItem import CPEInventoryItem, KeywordInventoryItem
import yaml

class InventoryHandler:
    def __init__(self, path):
        self.path = path

    def GetAllItems(self):
        items = []
        with open(self.path, 'r') as fh:
            for i in yaml.load(fh, Loader=yaml.FullLoader):
                if "severities" in i and "cpestring" in i:
                    for j in i["severities"]:
                        items.append(CPEInventoryItem(i["cpestring"], j, i["human_name"]))
                elif "keyword" in i:
                    items.append(KeywordInventoryItem(i["keyword"], i["human_name"]))
            return items

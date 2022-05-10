#!/usr/bin/python3
#
# InventoryHandler.py - parse and return inventory file (interesting software is defined here)
#

from InventoryItem import InventoryItem
import yaml

class InventoryHandler:
    def __init__(self, path):
        self.path = path

    def GetAllItems(self):
        items = []
        with open(self.path, 'r') as fh:
            for i in yaml.load(fh, Loader=yaml.FullLoader):
                for j in i["severities"]:
                    items.append(InventoryItem(i["cpestring"], j, i["human_name"]))
            return items

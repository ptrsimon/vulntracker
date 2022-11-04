#!/usr/bin/python3
#
# ApiHandler.py - handle requests to NVD
#
import sys
import time
import requests
import json

import LogHandler
from InventoryItem import CPEInventoryItem, KeywordInventoryItem, InventoryItem


class ApiHandler:
    def __init__(self, apikey, loghandler: LogHandler):
        self.apikey = apikey
        self.lh = loghandler

    def DaysAgoToTimestamp(self, days):
        epoch = time.time() - days * 86400
        return time.strftime("%Y-%m-%d", time.localtime(epoch)) + "T00:00:00:000 UTC+01:00"

    def GetVulnerabilitiesByCPE(self, cpestring, severity, newer_than_days):
        self.lh.Write("Fetching " + severity + " vulnerabilities for " + cpestring, 0)
        if newer_than_days != 0:
            r = requests.get('https://services.nvd.nist.gov/rest/json/cves/1.0/',
                             params={
                                 'apiKey': self.apikey,
                                 'resultsPerPage': "2000",
                                 'cpeMatchString': cpestring,
                                 'pubStartDate': self.DaysAgoToTimestamp(newer_than_days),
                                 'pubEndDate': self.DaysAgoToTimestamp(0),
                                 'cvssV3Severity': severity
                             },
                             timeout=60)
        else:
            r = requests.get('https://services.nvd.nist.gov/rest/json/cves/1.0/',
                             params={
                                 'apiKey': self.apikey,
                                 'resultsPerPage': "2000",
                                 'cpeMatchString': cpestring,
                                 'cvssV3Severity': severity
                             },
                             timeout=60)
        if r.status_code != 200:
            self.lh.Write("Failed to fetch vulnerabilities for " + cpestring + ": status="
                          + str(r.status_code) + " respurl=" + r.url, 3)
            sys.exit(1)
        return json.loads(r.text)

    def GetVulnerabilitiesByKeyword(self, keyword, newer_than_days):
        self.lh.Write("Fetching vulnerabilities for keyword " + keyword, 0)
        if newer_than_days != 0:
            r = requests.get('https://services.nvd.nist.gov/rest/json/cves/1.0/',
                             params={
                                 'apiKey': self.apikey,
                                 'resultsPerPage': "2000",
                                 'keyword': keyword,
                                 'pubStartDate': self.DaysAgoToTimestamp(newer_than_days),
                                 'pubEndDate': self.DaysAgoToTimestamp(0),
                             },
                             timeout=60)
        else:
            r = requests.get('https://services.nvd.nist.gov/rest/json/cves/1.0/',
                             params={
                                 'apiKey': self.apikey,
                                 'resultsPerPage': "2000",
                                 'keyword': keyword
                             },
                             timeout=60)
        if r.status_code != 200:
            self.lh.Write("Failed to fetch vulnerabilities for keyword " + keyword + ": status="
                          + str(r.status_code) + " respurl=" + r.url, 3)
            sys.exit(1)
        return json.loads(r.text)

    def GetVulnerabilities(self, item, newer_than_days=0):
        if isinstance(item, CPEInventoryItem):
            return self.GetVulnerabilitiesByCPE(item.cpestring, item.severity, newer_than_days)
        elif isinstance(item, KeywordInventoryItem):
            return self.GetVulnerabilitiesByKeyword(item.keyword, newer_than_days)
        else:
            self.lh.Write("Unsupported inventory item type: " + str(type(item)) + ", exit", 3)
            sys.exit(1)

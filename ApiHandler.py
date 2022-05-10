#!/usr/bin/python3
#
# ApiHandler.py - handle requests to NVD
#
import sys
import time
import requests
import json
import LogHandler

class ApiHandler:
    def __init__(self, apikey, loghandler: LogHandler):
        self.apikey = apikey
        self.lh = loghandler

    def DaysAgoToTimestamp(self, days):
        epoch = time.time() - days * 86400
        return time.strftime("%Y-%m-%d", time.localtime(epoch)) + "T00:00:00:000 UTC+01:00"

    def GetVulnerabilities(self, cpestring, severity, newer_than_days=0):
        self.lh.Write("Fetching " + severity + " vulnerabilities for " + cpestring, 0)
        if newer_than_days != 0:
            r = requests.get('https://services.nvd.nist.gov/rest/json/cves/1.0/',
                             params={
                                 'apiKey': self.apikey,
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
                                 'cpeMatchString': cpestring,
                                 'cvssV3Severity': severity
                             },
                             timeout=60)
        if r.status_code != 200:
            self.lh.Write("Failed to fetch vulnerabilities for " + cpestring + ": status code " + str(r.status_code), 3)
            sys.exit(1)
        return json.loads(r.text)

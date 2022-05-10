#!/usr/bin/python3
#
# AlertHandler.py - send out alerts
#

import Vulnerability
import AlertStateHandler
import LogHandler
import requests
import sys
from abc import ABC, abstractmethod

class AlertHandler(ABC):
    def __init__(self, loghandler: LogHandler):
        self.lh = loghandler
        self.ahs = None

    @abstractmethod
    def Send(self, vulnerability: Vulnerability):
        self.AddToState(vulnerability.cveid)

    def RegisterAlertStateHandler(self, ash: AlertStateHandler):
        self.ahs = ash

    def AddToState(self, cveid):
        if self.ahs is not None:
            self.ahs.AddAlert(cveid)

    def InState(self, cveid):
        if self.ahs is not None:
            return self.ahs.HasAlert(cveid)
        else:
            return False

class Elastic2nagiosAlertHandler(AlertHandler):
    def __init__(self, elastic2nagios_url, loghandler: LogHandler, apikey=None):
        self.elastic2nagios_url = elastic2nagios_url
        self.apikey = apikey
        super().__init__(loghandler)

    def Send(self, vulnerability: Vulnerability):
        if self.InState(vulnerability.cveid):
            self.lh.Write(vulnerability.cveid + " already in state database, skipping", 0)
            return

        self.lh.Write("Sending alert for " + vulnerability.cveid, 0)

        payload = {
            "plugin_output": vulnerability.cveid + " in " + vulnerability.human_name,
            "service": "CVE",
            "status": "WARNING",
            "hostname": "none"
        }
        headers = {}
        if self.apikey is not None:
            headers['apikey'] = self.apikey

        r = requests.post(self.elastic2nagios_url + "/create", data=payload, headers=headers)
        if r.status_code != 200:
            self.lh.Write("Failed to send alert to elastic2nagios: status code" + str(r.status_code))
            sys.exit(1)

        self.AddToState(vulnerability.cveid)

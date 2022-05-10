#!/usr/bin/python3
#
# AlertStateHandler.py - keeps track of CVEs where an alert was already sent out
#

import LogHandler
import json
import sys


class AlertStateHandler:
    def __init__(self, statefile, loghandler: LogHandler):
        self.statefile = statefile
        self.lh = loghandler

    def AddAlert(self, cveid):
        try:
            with open(self.statefile, 'r') as fh:
                state = json.load(fh)
        except Exception:
            state = []

        if cveid not in state:
            state.append(cveid)

        with open(self.statefile, 'w') as fh:
            json.dump(state, fh)

    def HasAlert(self, cveid):
        state = []
        try:
            with open(self.statefile, 'r') as fh:
                state = json.load(fh)
        except Exception as e:
            self.lh.Write("Failed to open state database: " + str(e) + ". Assuming empty state.", 0)

        return cveid in state

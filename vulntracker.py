#!/usr/bin/python3
#
# vulntracker.py - utility to fetch CVEs and send an alert if something interesting is found
#

from ApiHandler import ApiHandler
from AlertHandler import Elastic2nagiosAlertHandler
from AlertStateHandler import AlertStateHandler
from InventoryHandler import InventoryHandler
from InventoryItem import CPEInventoryItem, KeywordInventoryItem
from Vulnerability import Vulnerability
from LogHandler import ConsoleLogHandler
from LogHandler import FileLogHandler
import Config
import argparse
import time
import sys
import signal


def sigint_handler(sig, frame):
    print('Received SIGINT, exit')
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(
        description="Utility to fetch CVEs and send an alert if something interesting is found")
    parser.add_argument('-a', action='store_true',
                        help="Fetch all CVEs regardless of their published date (default is CVEs newer than 30 days)")
    args = parser.parse_args()

    signal.signal(signal.SIGINT, sigint_handler)

    try:
        lh = FileLogHandler(Config.FileLoggerConfig.path)
    except (NameError, AttributeError):
        lh = ConsoleLogHandler()

    ah = ApiHandler(Config.NvdApiConfig.apikey, lh)
    ih = InventoryHandler("inventory.yml")
    alh = Elastic2nagiosAlertHandler(Config.Elastic2nagiosConfig.url, lh, Config.Elastic2nagiosConfig.apikey)

    try:
        ash = AlertStateHandler(Config.AlertStateConfig.path, lh)
        alh.RegisterAlertStateHandler(ash)
    except NameError:
        pass

    inv = ih.GetAllItems()
    vulns = []

    for i in inv:
        if args.a:
            resp = ah.GetVulnerabilities(i)["result"]["CVE_Items"]
        else:
            resp = ah.GetVulnerabilities(i, Config.NvdApiConfig.daysnewer)["result"]["CVE_Items"]
        for j in resp:
            if isinstance(i, CPEInventoryItem):
                vuln = Vulnerability(j["cve"]["CVE_data_meta"]["ID"],
                                     i.cpestring, i.severity,
                                     j["cve"]["description"]["description_data"][0]["value"], i.human_name)
                for k in j["configurations"]["nodes"]:
                    vuln.ParseAffectedVersions(k["cpe_match"])
            elif isinstance(i, KeywordInventoryItem):
                vuln = Vulnerability(j["cve"]["CVE_data_meta"]["ID"],
                                     "unknown", "unknown",
                                     j["cve"]["description"]["description_data"][0]["value"], i.human_name)
            else:
                lh.Write("Unsupported inventory item type: " + str(type(i)) + ", exit", 3)
                sys.exit(1)
            vulns.append(vuln)
        time.sleep(1)

    for i in vulns:
        alh.Send(i)
        time.sleep(1)

    return 0


if __name__ == '__main__':
    main()

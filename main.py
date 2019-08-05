#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import sys
import requests
import configparser
import datetime
import socket
import time
from emoji import emojize

conf = {
    'bottoken': None
}
# read configuration
config_fn = "conf.ini"

config = configparser.ConfigParser()

config.read(config_fn)

conf = config['TELEGRAM']
network = "offline"
message = conf['message']
message = message.replace("\\n",'\n')
message = message.replace("\\r",'\r')
print(message)
looptime = int(conf['looptime'])
maxtries = int(conf['maxtries'])
currtry = 0

def telegram(message):
    """
    Bot Token and Chat ID Must be set at the configuration file 
    """
    botToken = conf['bottoken']
    chatid = conf['chatid']
    telegramurl = ("https://api.telegram.org/bot{0}/sendMessage").format(botToken)
    params = {"chat_id": chatid, "parse_mode": "HTML", "text": message}
    req = requests.post(telegramurl, params)

def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex.message)
        return False

# While there is no network keeps checking every 3 seconds
while True:
    currtry += 1
    if internet() == True:
        network = "online"
        break
    else:
        network = "offline"
        time.sleep(3)
    if currtry >= maxtries:
        break

if network == "online":
    telegram(emojize(message, use_aliases=True))
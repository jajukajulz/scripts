# Description: Script for rebooting and getting stats from a TPLINK router

#https://github.com/F5OEO/tp-connected
#
# Rain uses 1800MHz and 2600MHz but DOES NOT do Carrier aggregation.
# Some routers will auto connect to 1800MHz only - even though the router does support 2600MHZ. You will need a script to force it to 2600MHZ on the rain network.
# 1800MHz is generally slower on the download, but faster on the upload and has better ping/latency.
# 2600MHz is generally faster on the download, but slower on the upload and has more sporadic ping/latency.

#TL-MR6400
#With Rain you can select Band 3 (1800MHz) and Depending on your router model Band 38 (2600MHz) TDD OR Band 40 (2500-2600MHz) TDD. Check your router specs and select the band accordingly. Band 38 = 2600MHz and Band 41 = 2500MHz they are exactly the same band but some routers handle is differently.
#Network Type:
#4G: FDD-LTE Cat4 (800/900/1800/2100/2600MHz),
#TDD-LTE (1900/2300/2500/2600MHz)
#3G: DC-HSPA+/HSPA+/HSPA/UMTS (900/2100MHz)

#rain currently runs on the B3 1800MHz and B38 2600MHz bands qualifying as LTE. Your router/mobile phone needs to support one of these
#Rain 4G ONLY:
#1800 MHz FDD (Most devices support this band aka ‘Band 3’); &
#2600 MHz TDD (Some devices support this band aka ‘Band 38’)

#Rain FDD-LTE:800MHz(Band20)、900MHz(Band8)、1800MHz(Band3)、2100MHz(Band1)、2600MHz(Band7)
#Rain TDD-LTE: 2600MHz(Band38)

#Login to router -> Wireless -> Wireless settings -> Channel and Channel Width
#For 2.4GHz, channels 1, 6 and 11 are generally best, but any channel can be used. Also, change the channel width to 20MHz. 

import urllib2
from requests import get
from base64 import b64encode
from urllib.parse import quote

def getRouterUrl():
    return 'http://192.168.1.1' #Ip to TP-Link router

def SetupRouterConnection():

   #TP-Link router username and password
   username = '<CHANGE_ME>'
   password = '<CHANGE_ME>'

   p = urllib2.HTTPPasswordMgrWithDefaultRealm()

   p.add_password(None, getRouterUrl(), username, password)

   handler = urllib2.HTTPBasicAuthHandler(p)
   opener = urllib2.build_opener(handler)
   urllib2.install_opener(opener)
   return True

def addMacToWiFiBlock( mac,  desc):
   url = getRouterUrl()+'/userRpm/WlanMacFilterRpm.htm?Mac='+mac+'&Desc='+desc+'&Type=1&entryEnabled=1&Changed=0&selIndex=0&Page=1&vapIdx=1&Save=Save'
   page = urllib2.urlopen(url).read()
   return True

def getClientList():
    url = getRouterUrl()+'/userRpm/AssignedIpAddrListRpm.htm?Refresh=Refresh' #Clients
    page = urllib2.urlopen(url).read()
    devices = []

    #Parse out device list
    page = page.split("new Array(", 1)
    page = page[1].split('0,0 );', 1)
    page = page[0].replace('"',"").replace(' ',"")
    data = page.split("\n")

    for index in range(len(data)):
        if(index != 0):
            devices.append( data[index].split(",") )

    return devices

def getStatistics():
    url = getRouterUrl()+'/userRpm/SystemStatisticRpm.htm?itnerval=10&Num_per_page=100' #stats
    page = urllib2.urlopen(url).read()
    stats = []

    #Parse out statistic data
    page =  page.split("new Array(", 1)
    page = page[1].split('0,0 );', 1)
    page = page[0].replace('"',"").replace(' ',"")
    data = page.split("\n")

    for index in range(len(data)):
        if(index != 0):
            stats.append(  data[index].split(",") )
        #    if (len(sd) > 5):
        #        database_statistics.addStatisticData(sd[1],sd[2],sd[3],sd[4],sd[5],sd[6],sd[7],sd[8],sd[9])

    return stats

#SetupRouterConnection()
#addMacToWiFiBlock('00-00-00-00-00-11', 'test')
#getClientList()
#getStatistics()






def reboot():
    # constants
    tplink = '192.168.0.1'
    user = 'admin'
    password = 'admin'
    url_template = 'http://{}/userRpm/SysRebootRpm.htm?Reboot=Reboot'

    auth_bytes = bytes(user+':'+password, 'utf-8')
    auth_b64_bytes = b64encode(auth_bytes)
    auth_b64_str = str(auth_b64_bytes, 'utf-8')

    auth_str = quote('Basic {}'.format(auth_b64_str))

    auth = {
    'Referer': 'http://'+tplink+'/', 
    'Authorization': auth_str,
    }

    reboot_url = url_template.format(tplink)

    r = get(reboot_url, headers=auth)


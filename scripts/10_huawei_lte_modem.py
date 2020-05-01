# Description: Script for changing network band on a Huawei router


#https://github.com/Salamek/huawei-lte-api
#$ pip install huawei-lte-api
# Relay received SMS into your email https://github.com/chenwei791129/Huawei-LTE-Router-SMS-to-E-mail-Sender

# Rain uses 1800MHz and 2600MHz but DOES NOT do Carrier aggregation.
# B525 router will auto connect to 1800MHz only - even though the router does support 2600MHZ. You will need a script to force it to 2600MHZ on the rain network.
# 1800MHz is generally slower on the download, but faster on the upload and has better ping/latency.
#  2600MHz is generally faster on the download, but slower on the upload and has more sporadic ping/latency.

#With Rain you can select Band 3 (1800MHz) and Depending on your router model Band 38 (2600MHz) TDD OR Band 40 (2500-2600MHz) TDD. Check your router specs and select the band accordingly. Band 38 = 2600MHz and Band 41 = 2500MHz they are exactly the same band but some routers handle is differently.

from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
from huawei_lte_api.Connection import Connection

# connection = Connection('http://192.168.8.1/') For limited access, I have valid credentials no need for limited access
# connection = AuthorizedConnection('http://admin:MY_SUPER_TRUPER_PASSWORD@192.168.8.1/', login_on_demand=True) # If you wish to login on demand (when call requires authorization), pass login_on_demand=True

# 192.168.1.1
connection = AuthorizedConnection('http://admin:admin1@192.168.8.1/')

client = Client(connection) # This just simplifies access to separate API groups, you can use device = Device(connection) if you want
print(client.device.signal())  # Can be accessed without authorization
print(client.device.information())  # Needs valid authorization, will throw exception if invalid credentials are passed in URL


#<response>
#<NetworkMode>00</NetworkMode>
#<NetworkBand>3FFFFFFF</NetworkBand>
#<LTEBand>7FFFFFFFFFFFFFFF</LTEBand>
#</response>


dump(client.net.net_mode_list)

# /api/net/net-mode-list 
#<response>
#  <AccessList>
#    <Access>00</Access>
#    <Access>01</Access>
#    <Access>02</Access>
#    <Access>03</Access>
#  </AccessList>
#  <BandList>
#    <Band>
#      <Name>GSM900/GSM1800/WCDMA BCVIII/WCDMA BCI</Name>
#      <Value>2000000400380</Value>
#    </Band>
#  </BandList>
#  <LTEBandList>
#    <LTEBand>
#      <Name>LTE BC1/LTE BC3/LTE BC40/LTE BC41</Name>
#      <Value>18000000005</Value>
#    </LTEBand>
#    <LTEBand>
#      <Name>All bands</Name>
#      <Value>7ffffffffffffff</Value>
#    </LTEBand>
#  </LTEBandList>
#</response>



lteband = 10000000000 #default 7FFFFFFFFFFFFFFF


print(lteband)
networkband = "3FFFFFFF"
networkmode = "03"
client.net.set_net_mode(lteband, networkband, networkmode)


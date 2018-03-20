#!/usr/bin/python3

#import logging
#logging.basicConfig(level=logging.DEBUG)

from infoblox_client import connector
#from infoblox_client.connector import Connector
#from infoblox_client.exceptions import InfobloxException

#try:
#    from infoblox_client.connector import Connector
#    from infoblox_client.exceptions import InfobloxException
#    HAS_INFOBLOX_CLIENT = True
#except Import Error:
#    HAS_INFOBLOX_CLIENT = False

# WAPI 2.2.2 minimum requirement - NIOS 7.2

nios_provider_spec = {
    'host': dict(),
    'username': dict(),
    'password': dict(no_log=True),
    'ssl_verify': dict(type='bool', default=False),
    'silent_ssl_warnings': dict(type='bool', default=True),
    'http_request_timeout': dict(type='int', default=10),
    'http_pool_connections': dict(type='int', default=10),
    'http_pool_maxsize': dict(type='int', default=10),
    'max_retries': dict(type='int', default=3),
    'wapi_version': dict(default='2.7.1'),
    'max_results': dict(type='int', default=1000)
}

host = "10.60.27.4"
username = "admin"
password = "infoblox"
wapi_version = "2.7.1"

membername = "testpreprov1.blairlab"
memberip = "10.60.27.21"
membernetmask = "255.255.255.0"
membergateway = "10.60.27.1"

opts = {'host': host, 'username': username, 'password': password, 'wapi_version': wapi_version, 'ssl_verify': False, 'silent_ssl_warnings': True}

conn = connector.Connector(opts)

#networks = conn.get_object('network')
#print(networks)

createpayload = {"host_name": membername,  "vip_setting": {"_struct":"setting:network","address": memberip, "gateway": membergateway, "subnet_mask": membernetmask}, "platform": "VNIOS"}

newmember = conn.create_object('member', createpayload)

print(newmember)

updatepayload = {"host_name": membername,  "vip_setting": {"_struct":"setting:network","address": memberip, "gateway": membergateway, "subnet_mask": membernetmask}, "pre_provisioning": {"_struct": "preprovision", "hardware_info": [{"_struct": "preprovisionhardware", "hwmodel": "IB-VM-820", "hwtype": "IB-VNIOS"}], "licenses": ["dhcp", "dns", "enterprise", "vnios"]}}

preprov = conn.update_object(newmember, updatepayload)

print(preprov)

#funccall = newmember + "?_function=create_token"

gettoken = conn.call_func("create_token", newmember, "")

print(gettoken["pnode_tokens"][0]["token"])

deletemember = conn.delete_object(newmember)

print(deletemember)

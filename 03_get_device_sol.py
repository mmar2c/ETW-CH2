"""
Based on: lab1-1-get-host.py
04_get_device_sol
This script prints out all network devices that are connected to APIC-EM network devices in a tabular list format.
"""

import requests
import json
import sys
from tabulate import *
from apic_em_functions_sol import *

post_url = 'https://sandboxapicem.cisco.com/api/v1/network-device'

# Setup API request headers.
ticket = get_ticket()
headers = {'content-type' : 'application/json','X-Auth-Token': ticket}

device_list=[]
try:
    resp = requests.get(post_url,headers=headers,params='',verify = False)
    response_json = resp.json() # Get the json-encoded content from response
    print ('Status of GET /device request: ',resp.status_code)  # This is the http request status
except:
    print ('Something wrong with GET /host request!')
    sys.exit()
    # Now create a list of host summary info
i=0
for item in response_json['response']:
    i+=1
    device_list.append([i,item['type'],item['managementIpAddress']])
    
print (tabulate(device_list,headers=['Number','Type','IP'],tablefmt='rst'))


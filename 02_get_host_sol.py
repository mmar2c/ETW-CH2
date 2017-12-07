"""
Based on: lab1-1-get-host.py
02_get_host_sol
This script prints out all hosts that are connected to APIC-EM network devices in a tabular list format.
"""
'''
02_get_host.py
gets an inventory of hosts from \host endpoint
October, 2017
'''

import requests
import json
from tabulate import *
from apic_em_functions_sol import *

post_url = 'https://sandboxapicem.cisco.com/api/v1/host'

# All APIC-EM REST API request and response content type is JSON.
ticket = get_ticket()
headers = {'content-type':'application/json','X-Auth-Token':ticket}

try:
    resp = requests.get(post_url,headers=headers,params="",verify = False)
    response_json = resp.json() # Get the json-encoded content from response
    print ('Status of /host request: ',str(resp.status_code))  # This is the http request status
except:
    print ('Something is wrong with GET /host request!')
    sys.exit()

# Now create a list of host info to be held in host_list

host_list=[]
i=0
for item in response_json['response']:
    i+=1
    host_list.append([i,item['hostType'],item['hostIp']])

print (tabulate(host_list,headers=['Number','Type','IP'],tablefmt='rst'))

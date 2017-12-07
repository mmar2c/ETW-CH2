"""
This script retrieves an authentication token from APIC-EM and prints out it's value
It is standalone, there is no dependency.
MBenson clean edit 10/5
"""
import requests # Import JSON encoder and decoder module
import json     # requests module used to send REST requests to API
import sys
from tabulate import *

def get_ticket():
    requests.packages.urllib3.disable_warnings() # Disable SSH warnings
    
    # TICKET API URL
    post_url = 'https://sandboxapicem.cisco.com/api/v1/ticket'

    # All APIC-EM REST API request and response content type is JSON.
    headers = {'content-type': 'application/json'}

    # JSON input body content
    body_json = {
        'username': 'devnetuser',
        'password': 'Cisco123!'
    }

    # Make request and get response - "resp" is the response of this request
    resp = requests.post(post_url, json.dumps(body_json), headers=headers,verify=False)
    
    # Create ojbect to contain the request status
    status = resp.status_code #status code property of resp object

    # Create ojbect to contain the converted json-formatted response
    response_json = resp.json()

    #parse data for service ticket
    serviceTicket = response_json['response']['serviceTicket']
    return serviceTicket

def get_host():
    post_url = 'https://sandboxapicem.cisco.com/api/v1/host'

    # All APIC-EM REST API request and response content type is JSON.
    ticket = get_ticket()
    headers = {'content-type' : 'application/json','X-Auth-Token': ticket}

    try:
        resp = requests.get(post_url,headers=headers,params='',verify = False)
        response_json = resp.json() # Get the json-encoded content from response
        print ("Status of /host request: ",str(resp.status_code))  # This is the http request status
    except:
        print ('Something is wrong with GET /host request!')
        sys.exit()
    # Now create a list of host info to be held in host_list
    
    host_list=[]
    i=0
    for item in response_json['response']:
        i+=1
        host_list.append([i,item['hostType'],item['hostIp']])
    #print host_list
    print (tabulate(host_list,headers=['Number','Type','IP'],tablefmt='rst'))  

def get_device():
    
    post_url = 'https://sandboxapicem.cisco.com/api/v1/network-device'

    # Setup API request headers.
    ticket = get_ticket()
    headers = {"content-type" : "application/json","X-Auth-Token": ticket}

    device_list=[]
    try:
        resp = requests.get(post_url,headers=headers,params='',verify = False)
        response_json = resp.json() # Get the json-encoded content from response
        print ('Status of GET /device request: ',resp.status_code)  # This is the http request status
    except:
        print ('Something wrong with GET /device request!')
        sys.exit()
    # Now create a list of host summary info
    i=0
    for item in response_json['response']:
        i+=1
        device_list.append([i,item['type'],item['managementIpAddress']])
        
    print (tabulate(device_list,headers=['Number','Type','IP'],tablefmt='rst'))

  
    



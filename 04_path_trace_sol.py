"""
04_path_trace_sol.py
Path Trace Solution
APIC-EM Workshop
October 15, 2017
"""
#==================================================
# Section 1. Setup the environment and variables required to interact with the APIC-EM
#===================================================
import requests
import json
import time
import sys
from apic_em_functions_sol import *
from tabulate import *

requests.packages.urllib3.disable_warnings() #disables certificate security warning

#++++++++++++++++++++++++++++++++++++++++
# Path Trace API URL for flow_analysis endpoint
post_url = "https://sandboxapicem.cisco.com/api/v1/flow-analysis"

# Get service ticket number using imported function
ticket = get_ticket()

# Create headers for requests to the API
headers = {
			"content-type" : "application/json",
			"X-Auth-Token": ticket
			}
#++++++++++++++++++++++++++++++++++++++++++
			
#============================
# Section 2. Display list of devices and IPs by calling get_host() and get_devices()
#============================

#++++++++++++++++++++++++++++++++++++++++++
print('List of hosts on the network: ')
get_host()
print('List of devices on the network: ')
get_device()
#++++++++++++++++++++++++++++++++++++++++++

print('\n\n') #prints two blank lines to format output

# ============================
# Section 3. Get the source and destination IP addresses for the Path Trace
# ============================

while True:
	#++++++++++++++++++++++++++++++++++++++++++
	s_ip = input('Please enter the source IP address for the path trace: ')
	d_ip = input('Please enter the destinaion IP address for the path trace: ')
	#++++++++++++++++++++++++++++++++++++++++++
	#Various error traps should be completed here - POSSIBLE CHALLENGE
	if s_ip != '' or d_ip != '':
		#this creates a python dictionary that will be dumped as a 
		path_data = {
					"sourceIP": s_ip, 
					"destIP": d_ip
					}
		print('Source IP address is: ' + path_data['sourceIP']) #stud: optional challenge
		print('Destination IP address is: ' + path_data['destIP']) #stud: optional challenge
		break #Exit loop if values supplied
	else:
		print("\n\nYOU MUST ENTER IP ADDRESSES TO CONTINUE.\nUSE CTRL-C TO QUIT\n")
		continue #Return to beginning of loop and repeat

#============================
# Section 4. Initiate the Path Trace and get the flowAnalysisId
#============================

#++++++++++++++++++++++++++++++++++++		
# Post request to initiate Path Trace
path = json.dumps(path_data) #variable to hold the path_data
resp = requests.post(post_url,path,headers=headers,verify=False)

# Inspect the return, get the Flow Analysis ID, put it into a variable
resp_json = resp.json()
flowAnalysisId = resp_json["response"]["flowAnalysisId"]
print('FLOW ANALYSIS ID: ' + flowAnalysisId)
#++++++++++++++++++++++++++++++++++++

#============================
# Section 5. Check status of Path Trace request, output results when COMPLETED
#============================

status = ""

#Add Flow Analysis ID to the endpoint URL in order to check the status of this specific path trace
#++++++++++++++++++++++++++++++++++++
check_url = post_url + "/" + flowAnalysisId
#++++++++++++++++++++++++++++++++++++

checks = 0 #variable to increment within the while loop. Will trigger exit from loop after x iterations

while status != 'COMPLETED':
	checks += 1
	r = requests.get(check_url,headers=headers,params="",verify = False)
	response_json = r.json()
	#++++++++++++++++++++++++++++++++++++
	status = response_json["response"]["request"]["status"]
	#++++++++++++++++++++++++++++++++++++
	
	#wait one second before trying again
	time.sleep(1)
	if checks == 15: #number of iterations before exit of loop; change depending on conditions
		print("Number of status checks exceeds limit. Possible problem with Path Trace.")
		#break
		sys.exit()
	elif status == 'FAILED':
		print('Problem with Path Trace')
		#break
		sys.exit()
	print('REQUEST STATUS: ' + status)
	

#============================
# Section 6. Display results
#============================

#+++++++++++Add Values+++++++++++++++
# Create required variables
path_source = response_json['response']['request']['sourceIP'] 	#the source address for the trace, printed below
path_dest = response_json['response']['request']['destIP'] 	#the destination address for the trace, printed below
networkElementsInfo = response_json['response']['networkElementsInfo'] 	#variable holding a list of all the network element dictionaries
#++++++++++++++++++++++++++++++++++++

all_devices = [] # create a list variable to store the hosts and devices
device_no = 1  #this variable is an ordinal number for each device, incremented in the loop

#Iterate through returned Path Trace JSON and populate list of path information
for networkElement in networkElementsInfo:
    # test if the devices DOES NOT have a "name", absence of "name" identifies an end host
    if not 'name' in networkElement:  #assigns values to the variables for the hosts
       name = 'Unamed Host'
       ip = networkElement['ip']
       egressInterfaceName = 'UNKNOWN'
       ingressInterfaceName = 'UNKNOWN'
       device = [device_no,name,ip,ingressInterfaceName,egressInterfaceName]
    # if there is the "name" key, then it is an intermediary device
    else: #assigns values to the variables for the intermediary devices
       name = networkElement['name']
       ip = networkElement['ip']   
       if 'egressInterface' in networkElement: #not all intermediary devices have ingress and egress interfaces
           egressInterfaceName = networkElement['egressInterface']['physicalInterface']['name']
       else:
           egressInterfaceName = 'UNKNOWN'
           
       if 'ingressInterface' in networkElement:
           ingressInterfaceName = networkElement['ingressInterface']['physicalInterface']['name']
       else:
           ingressInterfaceName = 'UNKNOWN'       
       device = [device_no,name,ip,ingressInterfaceName,egressInterfaceName] #create the list of info to be displayed
    all_devices.append(device) #add this list of info for the device as a new line in this variable
    device_no += 1  #increments the ordinal variable for the device in the list

print('Path trace: \nSource: ' + path_source + '\nDestination: ' + path_dest) #print the source and destination IPs for the trace
print('List of devices on path:')
print (tabulate(all_devices,headers=['Item','Name','IP','Ingress Int','Egress Int'],tablefmt="rst")) #print the table of devices in the path trace

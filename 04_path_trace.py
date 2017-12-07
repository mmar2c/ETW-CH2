"""
Path Trace Student Work File
APIC-EM Workshop
October 15, 2017
"""
#==================================================
# Section 1. Setup the environment and variables required to interact with the APIC-EM
#===================================================
#+++++++++++Add Values+++++++++++++++
#import functions


#disable SSL certificate warnings


#++++++++++++++++++++++++++++++++++++


#+++++++++++Add Values+++++++++++++++
# Path Trace API URL for flow_analysis endpoint
post_url =    #URL of API endpoint
# Get service ticket number using imported function
ticket =      # Add your function name that gets service ticket
# Create headers for requests to the API
headers =     # Create dictionary containing headers for the request
#++++++++++++++++++++++++++++++++++++

#============================
# Section 2. Display list of devices and IPs by calling get_host() and get_devices()
#============================

#+++++++++++Add Values+++++++++++++++
#display message identifying what is to be printed on the next line

# Add your function name that displays hosts

# Display message identifying what is to be printed

# Add your function name that displays network devices

#++++++++++++++++++++++++++++++++++++

print('\n\n') #prints two blank lines to format output

# ============================
# Section 3. Get the source and destination IP addresses for the Path Trace
# ============================

while True:
	#+++++++++++Add Values+++++++++++++++
	s_ip =  # Request user input for source IP address
	d_ip =  # Request user input for destination IP address
	#++++++++++++++++++++++++++++++++++++
	#Various error traps should be completed here - POSSIBLE CHALLENGE

	if s_ip != '' or d_ip != '':
		#this creates a python dictionary that will be converted to a JSON object and posted
		path_data = {
					"sourceIP": s_ip, 
					"destIP": d_ip
					}
		#Optional: Add statements that display the source and destination IP addresses that will be used. And asks user to verify. Loop if not verified by user.
		
		
		break  #Exit loop if values supplied
	else:
		print("\n\nYOU MUST ENTER IP ADDRESSES TO CONTINUE.\nUSE CTRL-C TO QUIT\n")
		continue  #Return to beginning of loop and repeat

#============================
# Section 4. Initiate the Path Trace and get the flowAnalysisId
#============================

#+++++++++++Add Values+++++++++++++++	
# Post request to initiate Path Trace
path =  #Convert the path_data dictionary to JSON and assign it to this variable
resp =  #Make the request. Construct the post request to the API

# Inspect the return, get the Flow Analysis ID, put it into a variable
resp_json = resp.json()
flowAnalysisId =  # Assign the value of the flowAnalysisID key of resp_json.
#+++++++++++++++++++++++++++++++++++++

print('FLOW ANALYSIS ID: ' + flowAnalysisId)

#============================
# Section 5. Check status of Path Trace request, output results when COMPLETED
#============================


#initialize variable to hold the status of the path trace
status = ""

#+++++++++++Add Values+++++++++++++++
#Add Flow Analysis ID to the endpoint URL in order to check the status of this specific path trace
check_url =  #Append the flowAnalyisId to the flow analysis end point URL that was created in Section 1
#++++++++++++++++++++++++++++++++++++

checks = 0 #variable to increment within the while loop. Will trigger exit from loop after x iterations

while status != 'COMPLETED':
	checks += 1
	r = requests.get(check_url,headers=headers,params="",verify = False)
	response_json = r.json()
	#+++++++++++Add Values+++++++++++++++
	status =   # Assign the value of the status of the path trace request from response_json
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
	print('REQUEST STATUS: ' + status) #Print the status as the loop runs
	

#============================
# Section 6. Display results
#============================

# Create required variables
#+++++++++++Add Values+++++++++++++++
path_source =  #Assign the source address for the trace from response_json
path_dest =    #Assign the destination address for the trace from response_json
networkElementsInfo =  #Assign the list of all network element dictionaries from response_json
#+++++++++++++++++++++++++++++++++++++

all_devices = [] 	# A list variable to store the hosts and devices
device_no = 1 #this variable is an ordinal number for each device, incremented in the loop

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

print('Path trace: \n Source: ' + path_source + '\n\tDestination: ' + path_dest) #print the source and destination IPs for the trace
print('List of devices on path:')
print (tabulate(all_devices,headers=['Item','Name','IP','Ingress Int','Egress Int'],tablefmt="rst")) #print the table of devices in the path trace

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

intra_hutch_main.py

Purpose: Create a JSON file for ATEF to sanity-check if 
static PVs truly stay static. This main program will 
compare the value of PVs under all IOCs of a hutch multiple
times to filter out the dynamic PVs, keeping the static PVs 
and their values.

by: Rizheng Jiang 01/04/2024

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

import subprocess
import config
from datetime import datetime
import json
import os


# Gather user inputs for comparision and sifting
print("Hutch code list: \n\nCXI_FS5: 5  \nMEC_FS6: 6  \nMFX_FS4.5: 45  \nNEH_FS11: 11 \nNEH_FS14: 14  \nXCS_FS4: 4\n")
hutch_code = input("Enter hutch code: ")
hutch_dict = {
"5" : "CXI_FS5", 
"6" : "MEC_FS6",  
"45" : "MFX_FS4.5",  
"11" : "NEH_FS11", 
"14" : "NEH_FS14",  
"4" : "XCS_FS4"}

hutch = hutch_dict[hutch_code]
folder= os.getcwd() + "/" + hutch + "/"
ioc_path = folder + hutch + '_IOC.txt'

subprocess.run(["mkdir", "-p", folder + "temp/"])
pv_lists_path = folder + "temp/" + "pv_lists/"

subprocess.run(["mkdir", "-p", pv_lists_path])

total_iterations = int(input("Enter total iterations of random sampling: "))
interval = float(input("Enter max interval of each iteration in seconds: "))




# Run through all the IOCs of a hutch and configure the JSON file.
with open(ioc_path, 'r') as readtxt:
    ioc_list = [line.strip() for line in readtxt.readlines()]
    print("Estimated wait time: " + str(int(len(ioc_list) * total_iterations * (interval/2) / 60 + 2)) + " minutes.")
    for ioc in ioc_list:
        #print("Getting .pvlist file from " + ioc)
        subprocess.run(["cp", "/cds/data/iocData/"+ ioc +"/iocInfo/IOC.pvlist", pv_lists_path + ioc +"_IOC.pvlist"])
        config.run_config_json(
        hutch, 
        ioc, 
        ioc_list.index(ioc), 
        (ioc_list.index(ioc)+1)/len(ioc_list), 
        folder, 
        pv_lists_path + ioc +"_IOC.pvlist", 
        pv_lists_path + "new_" + ioc +"_IOC.pvlist", 
        total_iterations, interval
        )




#Getting date infomation
now = datetime.now()
date = now.strftime("%Y%m%d")
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")


#Add metadata and cleanup       
with open(folder + date + hutch + ".json", 'r') as openfile:
    # Reading from json file
    config_template = json.load(openfile)   

#Adding hutch name in JSON    
if config_template["root"]["name"] != hutch:
    config_template["root"]["name"] = hutch
    
#Adding timestamp in JSON
config_template["root"]["description"] = date_time

del config_template["root"]["configs"][0]
with open(folder + date + hutch + ".json", "w") as outfile:
    json.dump(config_template, outfile, indent=2)


print("date and time:",date_time)  
print("Done")


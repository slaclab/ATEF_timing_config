'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
intra_hutch_main.py

Purpose: Create a JSON file for ATEF to check static PVs. 
This main program compares the value of PVs multiple
times to filter out the dynamic PVs, keeping the static PVs 
and their values.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import subprocess
import config
from datetime import datetime
import json
import os
import argparse
from argparse import RawTextHelpFormatter

# Gather user input: hutch code, total iter, interval
parser = argparse.ArgumentParser(description='intra hutch usage:', formatter_class=RawTextHelpFormatter)
parser.add_argument("hutch_code", help="Enter the code of the hutch you want to check \n\nHutch code list: \nCXI_FS5: 5  \nMEC_FS6: 6  \nMFX_FS4.5: 45  \nNEH_FS11: 11 \nNEH_FS14: 14  \nXCS_FS4: 4\n\n", type=str)
parser.add_argument("total_iterations", help="Enter total iterations of random sampling (Default: 5)\n", nargs='?', const=1, type=int, default=5)
parser.add_argument("interval", help="Enter max interval of each iteration in seconds (Default: 5) \n", nargs='?', const=1, type=float, default=5)

args = parser.parse_args()

# date and time 
now = datetime.now()
date = now.strftime("%Y%m%d")
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

# Hutch list
hutch_dict = {
"5" : "CXI_FS5", 
"6" : "MEC_FS6",  
"45" : "MFX_FS4.5",  
"11" : "NEH_FS11", 
"14" : "NEH_FS14",  
"4" : "XCS_FS4",
"test" : "test_hutch"}

hutch = hutch_dict[args.hutch_code]
folder= os.getcwd() + "/" + hutch + "/"
ioc_path = folder + hutch + '_IOC.txt'

# temp dir for the pvlists 
subprocess.run(["mkdir", "-p", folder + "temp/"])
pv_lists_path = folder + "temp/" + "pv_lists/"
subprocess.run(["mkdir", "-p", pv_lists_path])

# Iterate through IOC list of a hutch and configure the JSON file.
with open(ioc_path, 'r') as hutch_iocs:
    ioc_list = [line.strip() for line in hutch_iocs.readlines()]
    # approx wait time 
    wait_time = int(len(ioc_list) * args.total_iterations * (args.interval/2) / 60 + 2)
    print("Estimated wait time: " + str(wait_time) + " minutes.")
    # json creation
    for ioc in ioc_list:
        # get list of pvs for each ioc
        subprocess.run(["cp", "/cds/data/iocData/"+ ioc +"/iocInfo/IOC.pvlist", pv_lists_path + ioc +"_IOC.pvlist"])
        # function for json config
        config.run_config_json(
        hutch, 
        ioc, 
        ioc_list.index(ioc), 
        (ioc_list.index(ioc)+1)/len(ioc_list), 
        folder, 
        pv_lists_path + ioc +"_IOC.pvlist", 
        pv_lists_path + "new_" + ioc +"_IOC.pvlist", 
        args.total_iterations, args.interval
        )

# Add metadata and cleanup       
with open(folder + date + hutch + ".json", 'r') as openfile:
    config_template = json.load(openfile)   

if config_template["root"]["name"] != hutch:
    config_template["root"]["name"] = hutch
config_template["root"]["description"] = date_time

del config_template["root"]["configs"][0]
with open(folder + date + hutch + ".json", "w") as outfile:
    json.dump(config_template, outfile, indent=2)

print("date and time:",date_time)  
print("Done")
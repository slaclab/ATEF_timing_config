'''''''''''''''''''''''''''''''''''''''''''''''''''

This package contains all the functions needed for the 
intra_hutch and inter_hutch comparisions. Use it by
"import config".

by: Rizheng Jiang 01/04/2024

'''''''''''''''''''''''''''''''''''''''''''''''''''


import json
import pandas as pd
import copy
from epics import caget, caput, cainfo
import time
import random
import subprocess
from tqdm import tqdm

#Get PV values once
def get_PV_values(No: int, pvlist: str, PV: dict):
    df = pd.read_csv(pvlist, header=None)
    
    names = []
    values = []
    pytype = []
    
    for i in df[0]:
        a = caget(i) 
        if isinstance(a, (float, int, str)):
            names.append(i)
            values.append(a)
            pytype.append(type(a))

    dictionary = {'PV_name': names, 'values': values, 'py_data_type': pytype}

    var_name = 'PV' + str(No)
    PV[var_name] = dictionary


#Compare two PV values dictionaries and filter out the dynamic values
def find_static(list1: int, list2: int, PV: dict, pvlist_new: str, folder: str, ioc: str):
    if list1 == 0:
        df1 = pd.DataFrame(PV['PV0'])
    else:
        df1 = pd.DataFrame(PV['static_PV_value'])

    df2 = pd.DataFrame(PV['PV1'])

    if df1.shape == df2.shape:
        static_PV_value = df1[df1["values"] == df2["values"]]
        PV['static_PV_value'] = pd.DataFrame(static_PV_value).reset_index(drop=True)
        static_PV_value.to_csv(folder + "temp/" + ioc + '_static_PV_value.csv', index=False)
        
    new_pvlist = static_PV_value['PV_name']
    new_pvlist.to_csv(pvlist_new, header=False, index=False)

    
#Configure the JSON file for one IOC using a PV dictionary
def configure(hutch: str, ioc: str, iocindex: int, progress: float, PV: dict, folder: str):
    # Opening JSON file
    with open('SR620_test.json', 'r') as openfile:
        # Reading from json file
        default_json_object = json.load(openfile)
    if iocindex == 0:
        with open('SR620_test.json', 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
    else:
        with open(folder + hutch + '.json', 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
    
    
    json_object["root"]["configs"].append(json_object["root"]["configs"][0])
    json_object["root"]["configs"][iocindex+1]["PVConfiguration"]["name"] = ioc
    
    PVs = default_json_object["root"]["configs"][0]["PVConfiguration"]["by_pv"]

    df = pd.DataFrame(PV['static_PV_value'])
    PVdictionary = {}

    for i in range(len(df["values"])):
        # Create a deep copy of the template for each iteration
        template = copy.deepcopy(PVs["IOC:LAS:LHN:SR620:04:SR_i_am_alive"])
        template[0]["Equals"]["value"] = df["values"][i]
        PVname = df["PV_name"][i]
        template[0]["Equals"]["name"] = PVname
        PVdictionary[PVname] = template

    json_object["root"]["configs"][iocindex+1]["PVConfiguration"]["by_pv"] = PVdictionary
    
    with open(folder + hutch + ".json", "w") as outfile:
        json.dump(json_object, outfile, indent=2)


#Configure all IOCs in a loop.
def run_config_json(hutch: str, ioc: str, iocindex: int, progress: float, folder: str, pvlist_default: str, pvlist_new: str, total_iterations: int, interval: float):
    PV0 = {} 
    # Create a tqdm progress bar with a total number of iterations
    for i in tqdm(range(total_iterations), desc = ioc):
        
        if i == 0:
            #print("Reading and recording the first list of PV values...")
            get_PV_values(i, pvlist_default, PV0)
            #print("First list of PV values recorded.")
            
        elif i == 1:
            #print("Wait for the PVs to fluctuate...")
            time.sleep(random.uniform(0.1, interval))
            
            get_PV_values(i, pvlist_default, PV0)
            #print("Next list of PV values recorded.")
    
            #print("Extracting the static PVs...")
            find_static(i-1,i, PV0, pvlist_new, folder, ioc)
            #print("Static PVs further narrowed.")
        
        else:
            #print("Wait for the PVs to fluctuate...")
            time.sleep(random.uniform(0.1, interval))
        
            get_PV_values(1, pvlist_new, PV0)
            #print("Next list of PV values recorded.")
    
            #print("Extracting the static PVs...")
            find_static(i-1,i, PV0, pvlist_new, folder, ioc)
            #print("Static PVs further narrowed.")
            


    
    #print("Configuring "+ ioc +" in JSON configuration file...")
    configure(hutch, ioc, iocindex, progress, PV0, folder)


    
        
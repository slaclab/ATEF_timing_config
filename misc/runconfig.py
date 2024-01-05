import config
import time
import random

def run_config_json(hutch: str, ioc: str, iocindex: int, progress: float, folder: str, pvlist_default: str, pvlist_new: str):
    PV0 = {}
    for i in range(0,3):
    
        if i == 0:
            #print("Reading and recording the first list of PV values...")
            config.get_PV_values(i, pvlist_default, PV0)
            #print("First list of PV values recorded.")
            
        elif i == 1:
            #print("Wait for the PVs to fluctuate...")
            time.sleep(random.uniform(0.1, 10.0))
            
            config.get_PV_values(1, pvlist_default, PV0)
            #print("Next list of PV values recorded.")
    
            #print("Extracting the static PVs...")
            config.find_static(i-1,i, PV0, pvlist_new, folder, ioc)
            #print("Static PVs further narrowed.")
        
        else:
            #print("Wait for the PVs to fluctuate...")
            time.sleep(random.uniform(0.1, 10.0))
        
            config.get_PV_values(1, pvlist_new, PV0)
            #print("Next list of PV values recorded.")
    
            #print("Extracting the static PVs...")
            config.find_static(i-1,i, PV0, pvlist_new, folder, ioc)
            #print("Static PVs further narrowed.")
    
    print("Configuring "+ ioc +" in JSON configuration file...")
    config.configure(hutch, ioc, iocindex, progress, PV0, folder)
    print("Done.")
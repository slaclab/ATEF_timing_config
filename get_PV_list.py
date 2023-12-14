import subprocess
import config


#print("Hutch name list: CXI_FS5  MEC_FS6  MFX_FS4.5  NEH_FS11  NEH_FS14  XCS_FS4")
#hutch = input("Enter hutch name: ")
hutch = "NEH_FS14"
folder= "/cds/home/r/rj1/atef/timing_config/"+ hutch + "/"
ioc_path = folder + hutch + '_IOC.txt'
pv_lists_path = folder + "pv_lists/"

subprocess.run(["mkdir", "-p", pv_lists_path])

with open(ioc_path, 'r') as readtxt:
    ioc_list = [line.strip() for line in readtxt.readlines()]
    # Read the file line by line
    for ioc in ioc_list:
        #print("Getting .pvlist file from " + ioc)
        subprocess.run(["cp", "/cds/data/iocData/"+ ioc +"/iocInfo/IOC.pvlist", pv_lists_path + ioc +"_IOC.pvlist"])
        print("Begin configuring " + ioc + " Progress: " + str((ioc_list.index(ioc))/len(ioc_list)*10000//1/100) + "%")
        config.run_config_json(hutch, ioc, ioc_list.index(ioc), (ioc_list.index(ioc)+1)/len(ioc_list), folder, pv_lists_path + ioc +"_IOC.pvlist", pv_lists_path + "new_" + ioc +"_IOC.pvlist")
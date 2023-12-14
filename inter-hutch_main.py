import json
import subprocess


print("Hutch code list: \n\nCXI_FS5: 5  \nMFX_FS4.5: 45  \nNEH_FS11: 11 \nNEH_FS14: 14  \nXCS_FS4: 4\n")

print("Recommend pairing FS11 with FS14, MFX with CXI or XCS")

hutch_dict = {"5" : "CXI_FS5",  "45" : "MFX_FS4.5",  "11" : "NEH_FS11", "14" : "NEH_FS14",  "4" : "XCS_FS4"}

hutch_code1 = input("Enter hutch 1 code: ")
hutch1 = hutch_dict[hutch_code1]

hutch_code2 = input("Enter hutch 2 code: ")
hutch2 = hutch_dict[hutch_code2]

hutch_key_dict = {"5" : ["CXI", "FS5"],  "45" : ["MFX", "FS45"],  "11" : ["NEH", "FS11"], "14" : ["NEH", "FS14"],  "4" : ["XCS", "FS4"]}

number_interhutch = subprocess.check_output("find interhutch -mindepth 1 -type d | wc -l", shell=True, stderr=subprocess.STDOUT, text=True)
number_interhutch = number_interhutch.strip()


subprocess.run(["mkdir", "-p", "interhutch/" + number_interhutch  + "_" + hutch1 + "_" + hutch2])



with open(hutch1 + "/" + hutch1 + ".json", 'r') as openfile1:
    config1 = json.load(openfile1)
    
with open(hutch2 + "/" + hutch2 + ".json", 'r') as openfile2:
    config2 = json.load(openfile2)

with open(hutch1 + "/" + hutch1 + ".json", 'r') as openfile1:
    config3 = json.load(openfile1)
    
with open('SR620_test.json', 'r') as openfile:
    template = json.load(openfile)
    
pv_pv_template = template["root"]["configs"][0]["PVConfiguration"]["by_pv"]["LAS:FS14:CNT:TI:B:GetTrigThreshold"]

if len(config1["root"]["configs"]) == len(config1["root"]["configs"]):
    print(len(config1["root"]["configs"]))
    ioc_list_strip_dict = []
    
    for i in range(len(config1["root"]["configs"])):
        print(i)
        pv_strip_dict = {}
        print(config1["root"]["configs"][i]["PVConfiguration"]["name"])
        print("Hutch 1")
        for pv1 in config1["root"]["configs"][i]["PVConfiguration"]["by_pv"].keys():
            pv1_stripped = pv1
            for hutch_id in hutch_key_dict[hutch_code1]:
                pv1_stripped = pv1_stripped.replace(hutch_id, "")
                #print(pv1_stripped)
            pv_strip_dict[pv1_stripped] = pv1
        
        ioc_list_strip_dict.append(pv_strip_dict)
        #print(pv_strip_dict)
        
        print(config2["root"]["configs"][i]["PVConfiguration"]["name"])
        print("Hutch 2")
        for pv2 in config2["root"]["configs"][i]["PVConfiguration"]["by_pv"].keys():
            pv2_stripped = pv2
            for hutch_id in hutch_key_dict[hutch_code2]:
                pv2_stripped = pv2_stripped.replace(hutch_id, "")
            #print(pv2_stripped)
            
            if pv2_stripped in ioc_list_strip_dict[i].keys():
                #print(ioc_list_strip_dict[i][pv2_stripped] + " matches with " + pv2)
                pv_pv_template[0]["Equals"]["name"] = ioc_list_strip_dict[i][pv2_stripped] + " & " + pv2
                pv_pv_template[0]["Equals"]["value_dynamic"]["EpicsValue"]["pvname"] = pv2
                config3["root"]["configs"][i]["PVConfiguration"]["by_pv"][ioc_list_strip_dict[i][pv2_stripped]] = pv_pv_template
        print("-----------------------------------------------------------------------")
            
else:
    print("Two hutches not comparable.")
    
with open("interhutch/" + number_interhutch  + "_" + hutch1 + "_" + hutch2 + "/" + hutch1 + "_" + hutch2 + "_comparison" + ".json", "w") as outfile:
        json.dump(config3, outfile, indent=2)
        
print("Configuration complete.")
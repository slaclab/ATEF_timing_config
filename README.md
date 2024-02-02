https://confluence.slac.stanford.edu/pages/viewpage.action?pageId=396375975

**Overview**

The goal of integrating ATEF into our checkout procedure is to check that no static PVs get modified under the radar. 
However, it is unrealistic to manually configure PV comparisons on a large scale in ATEF.
To mass process and configure the PV comparisons in ATEF, we have developed this tool to:
1) Recognize and extract the static PVs across different IOCs and establish a baseline table for default values.
2) Automatically construct the configuration file for tens of thousands of PVs in ATEF checkout.
Language: Python



**Data Flowchart**

https://slac-my.sharepoint.com/:u:/r/personal/rj1_slac_stanford_edu/Documents/Drawing.vsdx?d=w0e642654c14148669a2ced1fa0f1426d&csf=1&web=1&e=lR6VyX



**Summary**

This readme will show you the steps to generate a config file for a hutch and then how to run that config file to see which PVs have changed from the config file. To begin, make sure that you have access to the SLAC Linux network and the required permissions.

The main function and output is the generation of a .json configuration file. The .json files contain PVs relevant to the hutch or the devices/IOCs and their static values that are to be checked by ATEF. The script that generates the .json essentially samples the PVs for a specified number of iterations for a specified amount of time. At the end of the sampling, the PVs that have not changed are saved to the .json file thus capturing the "static PVs" during the script sampling iterations.

The .json files that are generated can then be natively run through atef to give an indication of which of the PVs have changed from when the config file was generated.



**Steps**

1. Sourcing the latest atef module
Enter the following command to access atef in your environment:

```
source /reg/g/pcds/engineering_tools/latest-released/scripts/pcds_conda
```

2. Generating the .json config file
The config file is a .json file that contains the PVs specific to the hutch. 
To generate the file, run the following command:

```
python intra_hutch_main.py [-h] hutch_code [total_iterations] [interval]
```

- Enter the hutch_code corresponding to the hutch.
- Enter the total number of iterations.
   - This value refers to the number of iterations that the PVs are sampled.
   - We have been using 5 as a value that yields sufficient config file results. (default:5)
- Enter the max interval for each iteration.
   - This value refers to the maximum amount of time where the PV is sampled. (default:5). The unit for this value is in seconds.

Run the following line to get the help info
```
python intra_hutch_main.py -h
```

![image](https://github.com/slaclab/ATEF_timing_config/assets/141056563/1779cff7-0967-472d-a8f2-ec8c6e1145c1)

Following the prompts, a time estimation on the generation of the config file will be displayed along with a progress bar.
An example run on MFX4.5:

![image](https://github.com/slaclab/ATEF_timing_config/assets/141056563/2f8464a0-f133-410b-9702-533310a33e38)


4. Running a config file through ATEF
To run the config file through atef, use the following command replacing "/cds/home/r/rj1/atef/timing_config/MFX_FS4.5/20240201MFX_FS4.5.json" with the desired .json file: 

```
python -m atef --log DEBUG check /cds/home/r/rj1/atef/timing_config/MFX_FS4.5/20240201MFX_FS4.5.json
```

5. Interpreting the Output
The output will show a subset of PVs which have a current value that is different from that which was captured in the config file. 
Screenshot of the output:

![image](https://github.com/slaclab/ATEF_timing_config/assets/141056563/ac832bf2-0a04-4cd0-be39-6e66b26c085a)

How to interpret the results:

  1. Hutch name
  2. IOC name
  3. PV name and the value recorded **last time** (after "equal to")
  4. PV name and the value recorded **this time** (after "value of")


The output tells you the discrepancy of the specific PVs within an IOC of a hutch between a previous ATEF run (when the config file was generated) and now.






















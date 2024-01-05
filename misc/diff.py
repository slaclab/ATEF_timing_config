with open('/cds/home/r/rj1/atef/timing_config/NEH_FS11/pv_lists/new_ioc-las-lhn-sr620-01_IOC.pvlist', 'r') as file1, open('/cds/home/r/rj1/atef/timing_config/NEH_FS14/pv_lists/new_ioc-las-lhn-sr620-04_IOC.pvlist', 'r') as file2:
    diff = set(file1).difference(file2)

with open('difference.txt', 'w') as output_file:
    for line in diff:
        output_file.write(line)
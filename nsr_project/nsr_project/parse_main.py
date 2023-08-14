"""
=================================================
National Security Research Institute (NSR) 
Commissioned Research Project, Ajou University

Function     : parse_main.py
Prototype    : 
Author       : Jongtae Lee (Ajou University)
Revision     : v1.1   2023.07.10 New
Modified     : 2023.08.14 By whdxo830
=================================================
"""

import header
from header import parse_data

path = "./config file"
file_lst = header.os.listdir(path)
order = ['conf', 'interface', 'arp', 'route']
file_lst.sort(key=lambda x: (int(x.split('_')[0][1:]), order.index(x.split('_')[1].split('.')[0])))
for file in file_lst:
    filepath = path + '/' + file
    
    # router-based parsing (need to add device separation code in the future)
    match = header.re.search(r'_(\w+).xml', file)
    if match:
        if match.group(1) == 'arp':
            print(filepath)
            header.parse_xml_arp(filepath)
        if match.group(1) == 'conf':
            print(filepath)
            header.parse_xml_conf(filepath)
        if match.group(1) == 'route':
            print(filepath)
            header.parse_xml_route(filepath)
        if match.group(1) == 'interface':
            print(filepath)
            header.parse_xml_interface(filepath)

print()
print('================================[PPrint Result]================================')            
print()
header.pprint.pprint(header.parse_data)

# convert json format, always reset and new write (view: https://jsonlint.com/)
with open("./result json/parsing_data.json", 'w') as f:
    header.json.dump(parse_data, f)
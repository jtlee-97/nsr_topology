"""
=================================================
National Security Research Institute (NSR) 
Network topology automation analysis algorithm 
development project, Ajou University

Function     : analysis_data.py
Prototype    : parse and analysis module test
Author       : Huiyeon Jang (Ajou University)
Revision     : v1.1   2023.07.20 New
Modified     : 2023.08.14 By whdxo830
=================================================
"""
import header 

with open("./result json/parsing_data.json", 'r') as f: # read parsing_data.json
    json_data=header.json.load(f)

def analysis_data():
    routers=list(json_data.keys())

    interface_data={}
    topology_data={}

    for r in routers: # key: ip address , value : router, port *issue: subnet mask?
        ports=list(json_data[r]['interface'].keys())
        for p in ports:
            if "unit" in json_data[r]['interface'][p]:
               ip= json_data[r]['interface'][p]["unit"]["interface IP"].split('/')[0]
               interface_data[ip]={}
               interface_data[ip]['router']=r
               interface_data[ip]['port']=p
           
    #print(interface_data)

    for r in routers: # find connection depend on ARP inrformation
        topology_data[r]={}
        topology_data[r]['Connectivity']=[]
        ports=list(json_data[r]['interface'].keys())
        for p in ports:
            if "logical interface" in json_data[r]['interface'][p]:
                lk=json_data[r]['interface'][p]['logical interface'].keys()
                for l in lk:
                    if "arp" in json_data[r]['interface'][p]['logical interface'][l].keys():
                        arp=json_data[r]['interface'][p]['logical interface'][l]['arp']
                        if arp['ip-address'] in interface_data:
                                ip=arp['ip-address']
                                if r != interface_data[ip]['router']:
                                    #print(r,interface_data[ip]['router'])
                                    topology_data[r]['Connectivity'].append({'Device':interface_data[ip]['router'], "Interface":interface_data[ip]['port'],"Network":ip})
                                
    print('================================[Analysis Test START]================================')            
    header.pprint.pprint(topology_data)
    print('================================[Analysis Test END]================================')            

    with open("./result json/topology_data.json", 'w') as make_file:
        header.json.dump(topology_data,make_file,indent='\t')
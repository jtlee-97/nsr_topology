"""
=================================================
National Security Research Institute (NSR) 
Network topology automation analysis algorithm 
development project, Ajou University

Function     : parse_xml_conf
             : move_logical
Prototype    : configuration parse (Step 1)
Version      : Python 3.9.13
Author       : J.T.Lee, H.Y.Jang (Ajou Univ.)
Revision     : v2.0   (from 2023. 07. 10)
Modified     : 2023. 08. 31
=================================================
"""
import header
import os

current_working_directory = os.getcwd()
current_script_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_script_directory, ".."))
config_file_path = os.path.join(parent_directory, "config_file")

def parse_xml_conf(xml_file):
    tree = header.ET.parse(xml_file)
    root = tree.getroot()
    
    # get "host-name" (device name)
    hostname = root.find('configuration/system/host-name').text
    header.parsing_data[hostname] = {}
    header.parsing_data[hostname]['interfaces'] = {}
    
    # interface setting
    interfaces=root.findall('configuration/interfaces/interface/name')
    if interfaces is not None:
        for interface in interfaces:
            interface_name=interface.text
            header.parsing_data[hostname]['interfaces'][interface_name]={}

    # logical system
    lg_system_lst=root.findall('configuration/logical-systems')
    
    if len(lg_system_lst)!=0 :
        header.parsing_data[hostname]['logical-systems']=[]
        for lg_system in lg_system_lst:
            lg_name=lg_system.find('name').text
            header.parsing_data[hostname]['logical-systems'].append(lg_name)
            header.parsing_data[lg_name]={}
            header.parsing_data[lg_name]['logical-system']='*'

            lg_itf=lg_system.findall('interfaces/interface/name')
            if lg_itf is not None:
                header.parsing_data[lg_name]['interfaces']={}
                for itf in lg_itf:
                    itf_name=itf.text
                    header.parsing_data[lg_name]['interfaces'][itf_name]={}
                    

    # nat parsing
    services=root.find('configuration/services')
    
    if services is not None:

        header.parsing_data[hostname]['service']={}

        sets=services.findall('service-set')

        if sets is not None:
            for set in sets:
                set_name=set.find('name').text
                nat_rule_name=set.find('nat-rules/name').text
                if nat_rule_name is not None:
                    header.parsing_data[hostname]['service']['nat']={}
                    header.parsing_data[hostname]['service']['nat'][set_name]={}
            
        nat=services.find('nat')

        if nat is not None:
            rules=nat.findall('rule')
            if rules is not None:
                for rule in rules:
                    rule_name=rule.find('name').text

                    if nat_rule_name==rule_name:
                        header.parsing_data[hostname]['service']['nat'][set_name][nat_rule_name]={}
                        match_direction=rule.find('match-direction').text
                        header.parsing_data[hostname]['service']['nat'][set_name][nat_rule_name]['match-direction']=match_direction

                        terms=rule.findall('term')
                        if terms is not None:
                            for term in terms:
                                term_name=term.find('name').text
                                header.parsing_data[hostname]['service']['nat'][set_name][nat_rule_name][term_name]={}
                                from_=term.find('from/source-address/name').text
                                header.parsing_data[hostname]['service']['nat'][set_name][nat_rule_name][term_name]['from']=from_
                                then_=term.find('then/translated/source-prefix').text
                                header.parsing_data[hostname]['service']['nat'][set_name][nat_rule_name][term_name]['then']=then_

                    
    # protocol parsing

    protocols=root.find('configuration/protocols')
    if protocols is not None:
        header.parsing_data[hostname]['protocol']={}
        protocol_interfaces=protocols.findall('ospf/area/interface/name')
        if protocol_interfaces is not None:
            for protocol_intf in protocol_interfaces:
                header.parsing_data[hostname]['protocol'][protocol_intf.text]={}

"""
=================================================
National Security Research Institute (NSR) 
Network topology automation analysis algorithm 
development project, Ajou University

Function     : parse_xml_arp
             : add_arp_info
Prototype    : configuration parse (Step 1)
Version      : Python 3.9.13
Author       : J.T.Lee, H.Y.Jang (Ajou Univ.)
Revision     : v2.0   (from 2023. 07. 11)
Modified     : 2023. 08. 31
=================================================
"""
import header

def parse_xml_arp(xml_file):

    tree = header.ET.parse(xml_file)
    root = tree.getroot()

    # Check the device name
    match = header.re.search(r'R\d', xml_file)
    hostname = match.group()

    # namespace (xml file)
    namespace_element = root[0]
    namespace = namespace_element.tag.split('}')[0][1:]
    namespace = {'arp':namespace}

    arp_tables=root.findall('.//arp:arp-table-entry',namespace)

    for arp_table in arp_tables:
        arp_intf_name = arp_table.find('arp:interface-name',namespace).text
        
        if 'logical-systems' in header.parsing_data[hostname]:
            for py_intf in header.parsing_data[hostname]['interfaces']:
                for ly_intf in header.parsing_data[hostname]['interfaces'][py_intf]['logical-interfaces']:
                    if  ly_intf == arp_intf_name:
                        ip = arp_table.find('arp:ip-address',namespace).text
                        mac = arp_table.find('arp:mac-address',namespace).text
                        add_arp_info(hostname, py_intf, ly_intf, ip, mac)
                    
            for lg_sys in header.parsing_data[hostname]['logical-systems']:
                for py_intf in header.parsing_data[lg_sys]['interfaces']:
                    for ly_intf in header.parsing_data[lg_sys]['interfaces'][py_intf]['logical-interfaces']:
                        if  ly_intf == arp_intf_name:
                            ip = arp_table.find('arp:ip-address',namespace).text
                            mac = arp_table.find('arp:mac-address',namespace).text
                            add_arp_info(lg_sys, py_intf, ly_intf, ip, mac)
                    
        else:
            for py_intf in header.parsing_data[hostname]['interfaces']:
                for ly_intf in header.parsing_data[hostname]['interfaces'][py_intf]['logical-interfaces']:
                    if  ly_intf == arp_intf_name:
                        ip = arp_table.find('arp:ip-address',namespace).text
                        mac = arp_table.find('arp:mac-address',namespace).text
                        add_arp_info(hostname, py_intf, ly_intf, ip, mac)


def add_arp_info(hostname, intf_name, ly_intf, ip, mac):
    if 'arp_table' not in header.parsing_data[hostname]['interfaces'][intf_name]['logical-interfaces'][ly_intf]:
        #header.parsing_data[hostname]['interfaces'][intf_name]['logical-interfaces'][ly_intf]['arp_table'] = {}
        header.parsing_data[hostname]['interfaces'][intf_name]['logical-interfaces'][ly_intf]['arp_table'] = []
        
        #header.parsing_data[hostname]['interfaces'][intf_name]['logical-interfaces'][ly_intf]['arp_table']['ip-address'] = ip
        #header.parsing_data[hostname]['interfaces'][intf_name]['logical-interfaces'][ly_intf]['arp_table']['mac-address'] = mac
        header.parsing_data[hostname]['interfaces'][intf_name]['logical-interfaces'][ly_intf]['arp_table'].append({'ip-address': ip, 'mac-address': mac})

    else:
        #header.parsing_data[hostname]['interfaces'][intf_name]['logical-interfaces'][ly_intf]['arp_table']['ip-address'] = ip
        #header.parsing_data[hostname]['interfaces'][intf_name]['logical-interfaces'][ly_intf]['arp_table']['mac-address'] = mac
        header.parsing_data[hostname]['interfaces'][intf_name]['logical-interfaces'][ly_intf]['arp_table'].append({'ip-address': ip, 'mac-address': mac})

    # [To be modified] Currently, we store information about the arp table as a list and it is classified by index in the actual json

# Before Code (mid term' 0831)
'''
def parse_xml_arp(xml_file):
    tree = header.ET.parse(xml_file)
    root = tree.getroot()
    
    # Check the belonging device
    match = header.re.search(r'R\d', xml_file)
    hostname = match.group()

    # (issues, 2023.07.12) : dynamic namespace
    # There is a namespace problem other than the config file and needs to be resolved (currently static mapping)
    # namespaces = {'arp': 'http://xml.juniper.net/junos/14.1R1/junos-arp'}
    
    # namespace issue complete (08.31)
    namespace_element = root[0]
    namespaces = namespace_element.tag.split('}')[0][1:]
    namespaces = {'arp':namespaces}

    arp_tables = root.findall('.//arp:arp-table-entry', namespaces)
    
    for arp_table in arp_tables:
        interface_name = arp_table.find('arp:interface-name', namespaces).text
        
        re_intf_name = header.re.sub(r"\.\d+$","",interface_name)
        
        if re_intf_name in header.parsing_data[hostname]['interface']:
            if interface_name in header.parsing_data[hostname]['interface'][re_intf_name]['logical interface']:
                header.parsing_data[hostname]['interface'][re_intf_name]['logical interface'][interface_name]['arp'] = {}
                mac_address = arp_table.find('arp:mac-address', namespaces)
                if mac_address is not None:
                    header.parsing_data[hostname]['interface'][re_intf_name]['logical interface'][interface_name]['arp']['mac-address'] = mac_address.text
                ip_address = arp_table.find('arp:ip-address', namespaces)
                if ip_address is not None:
                    header.parsing_data[hostname]['interface'][re_intf_name]['logical interface'][interface_name]['arp']['ip-address'] = ip_address.text
            elif interface_name not in header.parsing_data[hostname]['interface'][re_intf_name]['logical interface']:
                header.parsing_data[hostname]['interface'][re_intf_name]['logical interface'][interface_name] = {}
                header.parsing_data[hostname]['interface'][re_intf_name]['logical interface'][interface_name]['arp'] = {}
                mac_address = arp_table.find('arp:mac-address', namespaces)
                if mac_address is not None:
                    header.parsing_data[hostname]['interface'][re_intf_name]['logical interface'][interface_name]['arp']['mac-address'] = mac_address.text
                ip_address = arp_table.find('arp:ip-address', namespaces)
                if ip_address is not None:
                    header.parsing_data[hostname]['interface'][re_intf_name]['logical interface'][interface_name]['arp']['ip-address'] = ip_address.text
        
        # total arp count add
        #header.parsing_data[hostname]['arp_entry_count'] = root.findall('.//arp:arp-entry-count',namespaces).text
        
 '''
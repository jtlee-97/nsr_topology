"""
=================================================
National Security Research Institute (NSR) 
Commissioned Research Project, Ajou University

Function     : parse_xml_arp.py
Prototype    : parse_xml_arp
Author       : Jongtae Lee (Ajou University)
Revision     : v1.1   2023.07.11 New
Modified     : 2023.07.12 By whdxo830
=================================================
"""
import header

def parse_xml_arp(xml_file):
    tree = header.ET.parse(xml_file)
    root = tree.getroot()
    
    # Check the belonging device
    match = header.re.search(r'R\d', xml_file)
    hostname = match.group()

    # (issues, 2023.07.12) : dynamic namespace
    # There is a namespace problem other than the config file and needs to be resolved (currently static mapping)
    namespaces = {'arp': 'http://xml.juniper.net/junos/14.1R1/junos-arp'}

    arp_tables = root.findall('.//arp:arp-table-entry', namespaces)
    
    for arp_table in arp_tables:
        interface_name = arp_table.find('arp:interface-name', namespaces).text
        
        re_intf_name = header.re.sub(r"\.\d+$","",interface_name)
        
        if re_intf_name in header.parse_data[hostname]['interface']:
            if interface_name in header.parse_data[hostname]['interface'][re_intf_name]['logical interface']:
                header.parse_data[hostname]['interface'][re_intf_name]['logical interface'][interface_name]['arp'] = {}
                mac_address = arp_table.find('arp:mac-address', namespaces)
                if mac_address is not None:
                    header.parse_data[hostname]['interface'][re_intf_name]['logical interface'][interface_name]['arp']['mac-address'] = mac_address.text
                ip_address = arp_table.find('arp:ip-address', namespaces)
                if ip_address is not None:
                    header.parse_data[hostname]['interface'][re_intf_name]['logical interface'][interface_name]['arp']['ip-address'] = ip_address.text
            elif interface_name not in header.parse_data[hostname]['interface'][re_intf_name]['logical interface']:
                header.parse_data[hostname]['interface'][re_intf_name]['logical interface'][interface_name] = {}
                header.parse_data[hostname]['interface'][re_intf_name]['logical interface'][interface_name]['arp'] = {}
                mac_address = arp_table.find('arp:mac-address', namespaces)
                if mac_address is not None:
                    header.parse_data[hostname]['interface'][re_intf_name]['logical interface'][interface_name]['arp']['mac-address'] = mac_address.text
                ip_address = arp_table.find('arp:ip-address', namespaces)
                if ip_address is not None:
                    header.parse_data[hostname]['interface'][re_intf_name]['logical interface'][interface_name]['arp']['ip-address'] = ip_address.text
        
        # total arp count add
        #header.parse_data[hostname]['arp_entry_count'] = root.findall('.//arp:arp-entry-count',namespaces).text
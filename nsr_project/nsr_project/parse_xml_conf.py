"""
=================================================
National Security Research Institute (NSR) 
Commissioned Research Project, Ajou University

Function     : parse_xml_conf.py
Prototype    : parse_xml_conf
Author       : Jongtae Lee (Ajou University)
Revision     : v1.4   2023.07.10 New
Modified     : 2023.07.17 By whdxo830
=================================================
"""
import header

def parse_xml_conf(xml_file):
    tree = header.ET.parse(xml_file)
    root = tree.getroot()
    
    # get "host-name" (device name)
    hostname = root.find('configuration/system/host-name').text
    # make Key "hostname" in dictionary
    header.parse_data[hostname] = {}
    header.parse_data[hostname]['interface'] = {}
    
    # XML Structure Traversal, Keyward: "interfaces"
    interfaces = root.findall('configuration/interfaces/interface')
    for interface in interfaces:
        interface_name = interface.find('name').text
        re_intf_name = header.re.sub(r"\.\d+$","",interface_name)

        # create key "interface_name" in dictionary
        header.parse_data[hostname]['interface'][re_intf_name] = {}

        # save "description" value
        description = interface.find('description')
        if description is not None:
            header.parse_data[hostname]['interface'][interface_name]['description'] = description.text

        # save "speed" value
        speed = interface.find('speed')
        if speed is not None:
            header.parse_data[hostname]['interface'][interface_name]['speed'] = speed.text

        # find root in unit structure
        unit = interface.find('unit')
        address = unit.find('family').find('inet').find('address')
        
        # create sub key "unit" in dictionary
        header.parse_data[hostname]['interface'][interface_name]['unit'] = {}

        unit_name = unit.find('name')
        intf_ip = address.find('name')
        if unit_name is not None:
            header.parse_data[hostname]['interface'][interface_name]['unit']['uname'] = unit_name.text
        if intf_ip is not None:
            header.parse_data[hostname]['interface'][interface_name]['unit']['interface IP'] = intf_ip.text
        
        # [TBD] unit > family > inet > filter            

     # [SKIP] XML Structure Traversal, Keyward: "routing-option"
     # That data can come from "route.xml"

     # XML Structure Traversal, Keyward: "protocol"
    ospf_area = root.findall('configuration/protocols/ospf/area/interface')
    for interface in ospf_area:
        ospf_intf_name = interface.find('name').text
        # Assign only as decimal point according to current xml data
        ospf_re_intf_name = header.re.sub(r"\.\d+$","",ospf_intf_name)
        interface_dict = header.parse_data[hostname]['interface'][ospf_re_intf_name]
        interface_dict['logical interface'] = {}
        interface_dict['logical interface'][ospf_intf_name] = {}

        # matching interface name and add to dictionary
        if ospf_re_intf_name in header.parse_data[hostname]:
            interface_dict = header.parse_data[hostname][ospf_re_intf_name]
            # bfd-liveness-detection {"bfd": "on/off"}
            bfd_liveness_detection = interface.find('bfd-liveness-detection')
            ############# revision ############# 
            if ospf_intf_name in interface_dict['logical interface']:
                if bfd_liveness_detection is not None:
                    minimum_interval = bfd_liveness_detection.find('minimum-interval').text
                    interface_dict['logical interface'][ospf_intf_name]['ospf'] = {}
                    interface_dict['logical interface'][ospf_intf_name]['ospf']['bfd'] = 'on'
                    interface_dict['logical interface'][ospf_intf_name]['ospf']['minimum-interval'] = minimum_interval
            else:
                interface_dict['logical interface'][ospf_intf_name] = {}
                if bfd_liveness_detection is not None:
                    minimum_interval = bfd_liveness_detection.find('minimum-interval').text
                    interface_dict['logical interface'][ospf_intf_name]['ospf'] = {}
                    interface_dict['logical interface'][ospf_intf_name]['ospf']['bfd'] = 'on'
                    interface_dict['logical interface'][ospf_intf_name]['ospf']['minimum-interval'] = minimum_interval
        
    
    # [SKIP] XML Structure Traversal, Keyward: "firewall"
    # That data is from the 2nd year task

    # [To Do] XML Structure Traversal, Keyward: "routing-instances" and "logical-system"
"""
=================================================
National Security Research Institute (NSR) 
Network topology automation analysis algorithm 
development project, Ajou University

Function     : parse_xml_interface
Prototype    : configuration parse (Step 1)
Version      : Python 3.9.13
Author       : J.T.Lee, H.Y.Jang (Ajou Univ.)
Revision     : v2.0   (from 2023. 07. 12)
Modified     : 2023. 08. 31
=================================================
"""
import header
import os

current_working_directory = os.getcwd()
current_script_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_script_directory, ".."))
config_file_path = os.path.join(parent_directory, "config_file")

def parse_xml_interface(xml_file):
    tree = header.ET.parse(xml_file)
    root = tree.getroot()

    # Check the belonging device
    # match = header.re.search(r'R\d', xml_file)
    # hostname = match.group(1)
    file_name=os.path.basename(xml_file)
    hostname=file_name.split('_')[0]
    # namespace (xml file)
    namespace_element = root[0]
    namespace = namespace_element.tag.split('}')[0][1:]
    namespace = {'interface':namespace}
   
    # Physical Interface
    intf_py_tables = root.findall('.//interface:physical-interface', namespace)
    for intf_py_table in intf_py_tables:
        # If the pysical interface name is in parsing_data, perform operations by fetching the pysical interface name stored inside parsing_data
        intf_py_name = intf_py_table.find('interface:name',namespace).text
        if intf_py_name in header.parsing_data[hostname]['interfaces']:
            # Logical Interface
            lg_interfaces = intf_py_table.findall('interface:logical-interface',namespace)

            if 'logical-interfaces' not in header.parsing_data[hostname]['interfaces'][intf_py_name]:
                if lg_interfaces is not None:
                    header.parsing_data[hostname]['interfaces'][intf_py_name]['logical-interfaces'] = {}
                    for logical_intf in lg_interfaces: 
                        lg_intf_name = logical_intf.find('interface:name',namespace).text
                        header.parsing_data[hostname]['interfaces'][intf_py_name]['logical-interfaces'][lg_intf_name] = {}

                        address_family = logical_intf.findall('interface:address-family',namespace)
                        if len(address_family) != 0:
                            header.parsing_data[hostname]['interfaces'][intf_py_name]['logical-interfaces'][lg_intf_name]['address-family'] = {}
                            for fam in address_family:
                                fam_name = fam.find('interface:address-family-name',namespace).text
                                header.parsing_data[hostname]['interfaces'][intf_py_name]['logical-interfaces'][lg_intf_name]['address-family'][fam_name] = {}
                                interface_address = fam.find('interface:interface-address',namespace)
                                if interface_address is not None:
                                    ifa_local = interface_address.find('interface:ifa-local',namespace).text
                                    header.parsing_data[hostname]['interfaces'][intf_py_name]['logical-interfaces'][lg_intf_name]['address-family'][fam_name]['ifa-local'] = ifa_local
            else:
                if lg_interfaces is not None:
                    for logical_intf in lg_interfaces: 
                        lg_intf_name = logical_intf.find('interface:name',namespace).text

                        if lg_intf_name not in header.parsing_data[hostname]['interfaces'][intf_py_name]['logical-interfaces']:
                            header.parsing_data[hostname]['interfaces'][intf_py_name]['logical-interfaces'][lg_intf_name] = {}
                            address_family = logical_intf.findall('interface:address-family',namespace)
                            if len(address_family) != 0:
                                header.parsing_data[hostname]['interfaces'][intf_py_name]['logical-interfaces'][lg_intf_name]['address-family'] = {}
                                for fam in address_family:
                                    fam_name = fam.find('interface:address-family-name',namespace).text
                                    header.parsing_data[hostname]['interfaces'][intf_py_name]['logical-interfaces'][lg_intf_name]['address-family'][fam_name] = {}
                                    interface_address = fam.find('interface:interface-address',namespace)
                                    if interface_address is not None:
                                        ifa_local = interface_address.find('interface:ifa-local',namespace).text
                                        header.parsing_data[hostname]['interfaces'][intf_py_name]['logical-interfaces'][lg_intf_name]['address-family'][fam_name]['ifa-local'] = ifa_local

                        else:
                            address_family = logical_intf.findall('interface:address-family',namespace)
                            if len(address_family) != 0:
                                header.parsing_data[hostname]['interfaces'][intf_py_name]['logical-interfaces'][lg_intf_name]['address-family'] = {}
                                for fam in address_family:
                                    fam_name = fam.find('interface:address-family-name',namespace).text
                                    header.parsing_data[hostname]['interfaces'][intf_py_name]['logical-interfaces'][lg_intf_name]['address-family'][fam_name] = {}
                                    interface_address = fam.find('interface:interface-address',namespace)
                                    if interface_address is not None:
                                        ifa_local = interface_address.find('interface:ifa-local',namespace).text
                                        header.parsing_data[hostname]['interfaces'][intf_py_name]['logical-interfaces'][lg_intf_name]['address-family'][fam_name]['ifa-local'] = ifa_local
                
        # If the pysical interface name is not in parsing_data, create new pysical interface name and continue
        else: 
            if 'logical-systems' in header.parsing_data[hostname]:
                for lg_syst in header.parsing_data[hostname]['logical-systems']:
                    if intf_py_name in header.parsing_data[lg_syst]['interfaces']:
                        # Logical Interface
                        lg_interfaces = intf_py_table.findall('interface:logical-interface',namespace)
                        if lg_interfaces is not None:
                            header.parsing_data[lg_syst]['interfaces'][intf_py_name]['logical-interfaces'] = {}
                            for logical_intf in lg_interfaces:
                                lg_intf_name = logical_intf.find('interface:name',namespace).text
                                header.parsing_data[lg_syst]['interfaces'][intf_py_name]['logical-interfaces'][lg_intf_name] = {}

                                address_family = logical_intf.findall('interface:address-family',namespace)
                                if len(address_family) != 0:
                                    header.parsing_data[lg_syst]['interfaces'][intf_py_name]['logical-interfaces'][lg_intf_name]['address-family'] = {}
                                    for fam in address_family:
                                        fam_name = fam.find('interface:address-family-name',namespace).text
                                        header.parsing_data[lg_syst]['interfaces'][intf_py_name]['logical-interfaces'][lg_intf_name]['address-family'][fam_name] = {}
                                        interface_address = fam.find('interface:interface-address',namespace)
                                        if interface_address is not None:
                                            interface_local = interface_address.find('interface:ifa-local',namespace).text
                                            header.parsing_data[lg_syst]['interfaces'][intf_py_name]['logical-interfaces'][lg_intf_name]['address-family'][fam_name]['ifa-local'] = interface_local

# nat parsing

    if 'nat' in header.parsing_data[hostname]:
        interfaces=root.find('')


# Before Code (mid term' 0831)
"""
def parse_xml_interface(xml_file):
    tree = header.ET.parse(xml_file)
    root = tree.getroot()
    
    # Check the belonging device
    match = header.re.search(r'R\d', xml_file)
    hostname = match.group()

    # namespace issues (2023.07.12)
    # There is a namespace problem other than the config file and needs to be resolved (currently static mapping)
    namespaces = {'interface': 'http://xml.juniper.net/junos/14.1R1/junos-interface'}

    intf_py_tables = root.findall('.//interface:physical-interface', namespaces)
    for intf_py_table in intf_py_tables:
        intf_py_name = intf_py_table.find('interface:name', namespaces).text

        # create key "interface_name" in dictionary
        if intf_py_name not in header.parsing_data[hostname]['interface']:
            header.parsing_data[hostname]['interface'][intf_py_name] = {}

        # create sub key "status" in dictionary
        header.parsing_data[hostname]['interface'][intf_py_name]['status'] = {}

        # save "admin-status" value -- or "down"
        description_py = intf_py_table.find('interface:description', namespaces)
        if description_py is not None:
            header.parsing_data[hostname]['interface'][intf_py_name]['status']['description'] = description_py.text

        # save "admin-status" value -- or "down"
        admin_status_py = intf_py_table.find('interface:admin-status', namespaces)
        if admin_status_py is not None:
            header.parsing_data[hostname]['interface'][intf_py_name]['status']['admininistration'] = admin_status_py.text
            
        # save "oper-status" value -- or "down" / "testing"
        oper_status_py = intf_py_table.find('interface:oper-status', namespaces)
        if oper_status_py is not None:
            header.parsing_data[hostname]['interface'][intf_py_name]['status']['operational'] = oper_status_py.text


        intf_lg_tables = intf_py_table.findall('.//interface:logical-interface', namespaces)
        for intf_lg_table in intf_lg_tables:
            intf_lg_name = intf_lg_table.find('interface:name', namespaces)
            
            if 'logical interface' not in header.parsing_data[hostname]['interface'][intf_py_name]:
                header.parsing_data[hostname]['interface'][intf_py_name]['logical interface'] = {}
            
            if intf_lg_name is not None:
                intf_lg_name = intf_lg_name.text

                # create key "interface_name" in dictionary
                if intf_lg_name not in header.parsing_data[hostname]['interface'][intf_py_name]['logical interface']:
                    header.parsing_data[hostname]['interface'][intf_py_name]['logical interface'][intf_lg_name] = {}

                # save "admin-status" value -- or "down" in logical
                admin_status_lg = intf_lg_table.find('interface:admin-status', namespaces)
                if admin_status_lg is not None and admin_status_lg.text == 'up':
                    header.parsing_data[hostname]['interface'][intf_py_name]['logical interface'][intf_lg_name]['admininistration'] = admin_status_lg.text
                
                # save "oper-status" value -- or "down" / "testing" in logical
                oper_status_lg = intf_lg_table.find('interface:oper-status', namespaces)
                if oper_status_lg is not None and oper_status_lg.text == 'up':
                    header.parsing_data[hostname]['interface'][intf_py_name]['logical interface'][intf_lg_name]['operational'] = oper_status_lg.text

            # (issue, 2023.07.12) : Whether to distinguish "address-family-name"
            add_fam_names = intf_lg_table.findall('.//interface:address-family-name', namespaces)
            header.parsing_data[hostname]['interface'][intf_py_name]['logical interface'][intf_lg_name]['address family name'] = []
            for add_fam_name in add_fam_names:
                if add_fam_name is not None:
                    header.parsing_data[hostname]['interface'][intf_py_name]['logical interface'][intf_lg_name]['address family name'].append(add_fam_name.text)
"""
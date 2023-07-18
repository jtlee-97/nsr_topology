"""
=================================================
National Security Research Institute (NSR) 
Commissioned Research Project, Ajou University

Function     : parse_xml_interface.py
Prototype    : parse_xml_interface
Author       : Jongtae Lee (Ajou University)
Revision     : v1.3   2023.07.12 New
Modified     : 2023.07.17 By whdxo830
=================================================
"""
import header

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
        if intf_py_name not in header.parse_data[hostname]['interface']:
            header.parse_data[hostname]['interface'][intf_py_name] = {}

        # create sub key "status" in dictionary
        header.parse_data[hostname]['interface'][intf_py_name]['status'] = {}

        # save "admin-status" value -- or "down"
        description_py = intf_py_table.find('interface:description', namespaces)
        if description_py is not None:
            header.parse_data[hostname]['interface'][intf_py_name]['status']['description'] = description_py.text

        # save "admin-status" value -- or "down"
        admin_status_py = intf_py_table.find('interface:admin-status', namespaces)
        if admin_status_py is not None:
            header.parse_data[hostname]['interface'][intf_py_name]['status']['admininistration'] = admin_status_py.text
            
        # save "oper-status" value -- or "down" / "testing"
        oper_status_py = intf_py_table.find('interface:oper-status', namespaces)
        if oper_status_py is not None:
            header.parse_data[hostname]['interface'][intf_py_name]['status']['operational'] = oper_status_py.text


        intf_lg_tables = intf_py_table.findall('.//interface:logical-interface', namespaces)
        for intf_lg_table in intf_lg_tables:
            intf_lg_name = intf_lg_table.find('interface:name', namespaces)
            
            if 'logical interface' not in header.parse_data[hostname]['interface'][intf_py_name]:
                header.parse_data[hostname]['interface'][intf_py_name]['logical interface'] = {}
            
            if intf_lg_name is not None:
                intf_lg_name = intf_lg_name.text

                # create key "interface_name" in dictionary
                if intf_lg_name not in header.parse_data[hostname]['interface'][intf_py_name]['logical interface']:
                    header.parse_data[hostname]['interface'][intf_py_name]['logical interface'][intf_lg_name] = {}

                # save "admin-status" value -- or "down" in logical
                admin_status_lg = intf_lg_table.find('interface:admin-status', namespaces)
                if admin_status_lg is not None and admin_status_lg.text == 'up':
                    header.parse_data[hostname]['interface'][intf_py_name]['logical interface'][intf_lg_name]['admininistration'] = admin_status_lg.text
                
                # save "oper-status" value -- or "down" / "testing" in logical
                oper_status_lg = intf_lg_table.find('interface:oper-status', namespaces)
                if oper_status_lg is not None and oper_status_lg.text == 'up':
                    header.parse_data[hostname]['interface'][intf_py_name]['logical interface'][intf_lg_name]['operational'] = oper_status_lg.text

            # (issue, 2023.07.12) : Whether to distinguish "address-family-name"
            add_fam_names = intf_lg_table.findall('.//interface:address-family-name', namespaces)
            header.parse_data[hostname]['interface'][intf_py_name]['logical interface'][intf_lg_name]['address family name'] = []
            for add_fam_name in add_fam_names:
                if add_fam_name is not None:
                    header.parse_data[hostname]['interface'][intf_py_name]['logical interface'][intf_lg_name]['address family name'].append(add_fam_name.text)

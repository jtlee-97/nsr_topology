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
    
    # Basic interface layer construction steps
    interfaces = root.findall('configuration/interfaces/interface/name')
    if interfaces is not None:
        for interface in interfaces:
            interface_name = interface.text
            header.parsing_data[hostname]['interfaces'][interface_name] = {}
    
    # Logical-system existence check and classification steps
    logical_syss = root.findall('configuration/logical-systems')
    logical_sys_list = []
    if not logical_syss: 
        pass
    else:
        header.parsing_data[hostname]['logical-systems'] = []
        for logical_sys in logical_syss:
            lg_name = logical_sys.find('name').text
            header.parsing_data[hostname]['logical-systems'].append(lg_name)
            header.parsing_data[lg_name] = {}
            header.parsing_data[lg_name]['logical-system'] = '*'
            logical_sys_list.append(lg_name)

            l_interface=logical_sys.findall('interfaces/interface/name')
            if l_interface is not None:
                header.parsing_data[lg_name]['interfaces'] = {}
                for i in l_interface:
                    l_intf_name = i.text
                    header.parsing_data[lg_name]['interfaces'][l_intf_name] = {}

    # nat parsing
    services=root.find('configuration/services')
    if services is not None:
        service_set_name=services.find('service-set/name').text
        nat_rules_name=services.find('service-set/nat-rules/name').text

        if service_set_name is not None:
            header.parsing_data[hostname]['nat']={}
            header.parsing_data[hostname]['nat'][service_set_name]={}
            if nat_rules_name is not None:
                header.parsing_data[hostname]['nat'][service_set_name][nat_rules_name]={}

        nat=services.find('nat')
        if nat is not None:
            rule_name=nat.find('rule/name').text
            if rule_name is not None:
                if rule_name==nat_rules_name:
                    match_direction=nat.find('rule/match-direction').text
                    if match_direction is not None:
                        header.parsing_data[hostname]['nat'][service_set_name][nat_rules_name]['match-direction']=match_direction
            
                terms=nat.findall('rule/term')
                if terms is not None:
                    for term in terms:
                        term=term.find('name').text
                        header.parsing_data[hostname]['nat'][service_set_name][nat_rules_name][term]={}
                        
                        
                      


            
                


            

    # make logical systems folder and Move file steps
    if not logical_sys_list: 
        pass
    else:
        new_lg_path = "./logical_systems"
        if not header.os.path.exists(new_lg_path):
            header.os.mkdir(new_lg_path)
            move_logical(logical_sys_list) 
        else:
            move_logical(logical_sys_list)

# Move [logical-system file] to [logical-system folder]
def move_logical(lg_sys_list): 
    path = config_file_path
    dsc = os.path.join(parent_directory, "logical_systems")
    file_list = header.os.listdir(path)
    for lg in lg_sys_list:
        for file in file_list:
            lg_file = header.re.search(lg, file)
            if lg_file is not None:
                src = path + '/' + file
                # �̵����� ���� ����� ���� ������ ����
                #header.shutil.move(src, dsc)
                header.shutil.copy(src, dsc)


# Before Code (mid term' 0831)
'''
    # XML Structure Traversal, Keyward: "interfaces"
    interfaces = root.findall('configuration/interfaces/interface')
    for interface in interfaces:
        interface_name = interface.find('name').text
        re_intf_name = header.re.sub(r"\.\d+$","",interface_name)

        # create key "interface_name" in dictionary
        header.parsing_data[hostname]['interface'][re_intf_name] = {}

        # save "description" value
        description = interface.find('description')
        if description is not None:
            header.parsing_data[hostname]['interface'][interface_name]['description'] = description.text

        # save "speed" value
        speed = interface.find('speed')
        if speed is not None:
            header.parsing_data[hostname]['interface'][interface_name]['speed'] = speed.text

        # find root in unit structure
        unit = interface.find('unit')
        address = unit.find('family').find('inet').find('address')
        
        # create sub key "unit" in dictionary
        header.parsing_data[hostname]['interface'][interface_name]['unit'] = {}

        unit_name = unit.find('name')
        intf_ip = address.find('name')
        if unit_name is not None:
            header.parsing_data[hostname]['interface'][interface_name]['unit']['uname'] = unit_name.text
        if intf_ip is not None:
            header.parsing_data[hostname]['interface'][interface_name]['unit']['interface IP'] = intf_ip.text
        
        # [TBD] unit > family > inet > filter            

     # [SKIP] XML Structure Traversal, Keyward: "routing-option"
     # That data can come from "route.xml"

     # XML Structure Traversal, Keyward: "protocol"
    ospf_area = root.findall('configuration/protocols/ospf/area/interface')
    for interface in ospf_area:
        ospf_intf_name = interface.find('name').text
        # Assign only as decimal point according to current xml data
        ospf_re_intf_name = header.re.sub(r"\.\d+$","",ospf_intf_name)
        interface_dict = header.parsing_data[hostname]['interface'][ospf_re_intf_name]
        interface_dict['logical interface'] = {}
        interface_dict['logical interface'][ospf_intf_name] = {}

        # matching interface name and add to dictionary
        if ospf_re_intf_name in header.parsing_data[hostname]:
            interface_dict = header.parsing_data[hostname][ospf_re_intf_name]
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
'''
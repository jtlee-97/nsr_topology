"""
=================================================
National Security Research Institute (NSR) 
Network topology automation analysis algorithm 
development project, Ajou University

Function     : parse_xml_route
Prototype    : configuration parse (Step 1)
Version      : Python 3.9.13
Author       : J.T.Lee, H.Y.Jang (Ajou Univ.)
Revision     : v1.4   (from 2023. 07. 17)
Modified     : 2023. 07. 20
=================================================
"""
import header
import os

current_working_directory = os.getcwd()
current_script_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_script_directory, ".."))
config_file_path = os.path.join(parent_directory, "config_file")

def parse_xml_route(xml_file):
    tree = header.ET.parse(xml_file)
    root = tree.getroot()
    
    # Check the belonging device
    match = header.re.search(r'R\d', xml_file)
    hostname = match.group()

    # namespace (xml file) 
    namespace_element = root[0]
    namespace = namespace_element.tag.split('}')[0][1:]
    namespace = {'routing':namespace}
    
    header.parsing_data[hostname]['routing table'] = {}
    header.parsing_data[hostname]['routing table']['destination'] = {}

    route_tables = root.findall('.//routing:route-table', namespace)
    for route_table in route_tables:
        table_name = route_table.find('routing:table-name', namespace).text
        if table_name is not None:
            header.parsing_data[hostname]['routing table']['table-name'] = table_name

        destination_count = route_table.find('routing:destination-count', namespace).text
        if destination_count is not None:
            header.parsing_data[hostname]['routing table']['destination-count'] = destination_count

        total_route_count = route_table.find('routing:total-route-count', namespace).text
        if total_route_count is not None:
            header.parsing_data[hostname]['routing table']['total-route-count'] = total_route_count

        active_route_count = route_table.find('routing:active-route-count', namespace).text
        if active_route_count is not None:
            header.parsing_data[hostname]['routing table']['active-route-count'] = active_route_count

        holddown_route_count = route_table.find('routing:holddown-route-count', namespace).text
        if holddown_route_count is not None:
            header.parsing_data[hostname]['routing table']['holddown-route-count'] = holddown_route_count

        hidden_route_count = route_table.find('routing:hidden-route-count', namespace).text
        if hidden_route_count is not None:
            header.parsing_data[hostname]['routing table']['hidden-route-count'] = hidden_route_count

        route_entries = route_table.findall('routing:rt', namespace)
        for route_entry in route_entries:
            rt_destination = route_entry.find('routing:rt-destination', namespace).text
            if rt_destination is not None:
                header.parsing_data[hostname]['routing table']['destination'][rt_destination] = {}

            rt_entry = route_entry.find('routing:rt-entry', namespace)
            if rt_entry is not None:
                active_tag = rt_entry.find('routing:active-tag', namespace).text
                if active_tag is not None:
                    header.parsing_data[hostname]['routing table']['destination'][rt_destination]['active-tag'] = active_tag

                protocol_name = rt_entry.find('routing:protocol-name', namespace).text
                if protocol_name is not None:
                    header.parsing_data[hostname]['routing table']['destination'][rt_destination]['protocol-name'] = protocol_name

                preference = rt_entry.find('routing:preference', namespace).text
                if preference is not None:
                    header.parsing_data[hostname]['routing table']['destination'][rt_destination]['preference'] = preference

                age = rt_entry.find('routing:age', namespace).text
                if age is not None:
                    header.parsing_data[hostname]['routing table']['destination'][rt_destination]['age'] = age

                nh_entries = rt_entry.findall('routing:nh', namespace)
                for nh_entry in nh_entries:
                    nh_to = nh_entry.find('routing:to', namespace)
                    nh_via = nh_entry.find('routing:via', namespace)
                    if nh_to is not None and nh_via is not None:
                        if 'next-hop' not in header.parsing_data[hostname]['routing table']['destination'][rt_destination]:
                            header.parsing_data[hostname]['routing table']['destination'][rt_destination]['next-hop'] = []
                        
                        next_hop = {
                            'to': nh_to.text,
                            'via': nh_via.text
                        }
                        header.parsing_data[hostname]['routing table']['destination'][rt_destination]['next-hop'].append(next_hop)

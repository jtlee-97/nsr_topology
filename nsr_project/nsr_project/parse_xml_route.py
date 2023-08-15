"""
=================================================
National Security Research Institute (NSR) 
Network topology automation analysis algorithm 
development project, Ajou University

Function     : parse_xml_route.py
Prototype    : route parse
Author       : Jongtae Lee (Ajou University)
Revision     : v1.2   2023.07.17 New
Modified     : 2023.07.18 By whdxo830
=================================================
"""
import header

def parse_xml_route(xml_file):
    tree = header.ET.parse(xml_file)
    root = tree.getroot()
    
    # Check the belonging device
    match = header.re.search(r'R\d', xml_file)
    hostname = match.group()

    # namespace issues (2023.07.12)
    # There is a namespace problem other than the config file and needs to be resolved (currently static mapping)
    namespaces = {'routing': 'http://xml.juniper.net/junos/14.1R1/junos-routing'}
    
    header.parse_data[hostname]['routing table'] = {}
    header.parse_data[hostname]['routing table']['destination'] = {}

    route_tables = root.findall('.//routing:route-table', namespaces)
    for route_table in route_tables:
        table_name = route_table.find('routing:table-name', namespaces).text
        if table_name is not None:
            header.parse_data[hostname]['routing table']['table-name'] = table_name

        destination_count = route_table.find('routing:destination-count', namespaces).text
        if destination_count is not None:
            header.parse_data[hostname]['routing table']['destination-count'] = destination_count

        total_route_count = route_table.find('routing:total-route-count', namespaces).text
        if total_route_count is not None:
            header.parse_data[hostname]['routing table']['total-route-count'] = total_route_count

        active_route_count = route_table.find('routing:active-route-count', namespaces).text
        if active_route_count is not None:
            header.parse_data[hostname]['routing table']['active-route-count'] = active_route_count

        holddown_route_count = route_table.find('routing:holddown-route-count', namespaces).text
        if holddown_route_count is not None:
            header.parse_data[hostname]['routing table']['holddown-route-count'] = holddown_route_count

        hidden_route_count = route_table.find('routing:hidden-route-count', namespaces).text
        if hidden_route_count is not None:
            header.parse_data[hostname]['routing table']['hidden-route-count'] = hidden_route_count

        route_entries = route_table.findall('routing:rt', namespaces)
        for route_entry in route_entries:
            rt_destination = route_entry.find('routing:rt-destination', namespaces).text
            if rt_destination is not None:
                header.parse_data[hostname]['routing table']['destination'][rt_destination] = {}

            rt_entry = route_entry.find('routing:rt-entry', namespaces)
            if rt_entry is not None:
                active_tag = rt_entry.find('routing:active-tag', namespaces).text
                if active_tag is not None:
                    header.parse_data[hostname]['routing table']['destination'][rt_destination]['active-tag'] = active_tag

                protocol_name = rt_entry.find('routing:protocol-name', namespaces).text
                if protocol_name is not None:
                    header.parse_data[hostname]['routing table']['destination'][rt_destination]['protocol-name'] = protocol_name

                preference = rt_entry.find('routing:preference', namespaces).text
                if preference is not None:
                    header.parse_data[hostname]['routing table']['destination'][rt_destination]['preference'] = preference

                age = rt_entry.find('routing:age', namespaces).text
                if age is not None:
                    header.parse_data[hostname]['routing table']['destination'][rt_destination]['age'] = age

                nh_entries = rt_entry.findall('routing:nh', namespaces)
                for nh_entry in nh_entries:
                    nh_to = nh_entry.find('routing:to', namespaces)
                    nh_via = nh_entry.find('routing:via', namespaces)
                    if nh_to is not None and nh_via is not None:
                        if 'next-hop' not in header.parse_data[hostname]['routing table']['destination'][rt_destination]:
                            header.parse_data[hostname]['routing table']['destination'][rt_destination]['next-hop'] = []
                        
                        next_hop = {
                            'to': nh_to.text,
                            'via': nh_via.text
                        }
                        header.parse_data[hostname]['routing table']['destination'][rt_destination]['next-hop'].append(next_hop)

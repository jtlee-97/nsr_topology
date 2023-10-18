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
import ipaddress

def analysis_data(): #분석 진행하는 메인 함수 

    with open("./result_json/parsing_data.json", 'r') as f: # read parsing_data.json
        parsing_data=header.json.load(f)

    topology_data={} # 네트워크 토폴로지 연결정보 

    # 2차 파싱
    router_ip_data=parsing_router_ip(parsing_data)
    arp_data=parsing_arp(parsing_data)
    route_data=parsing_route(parsing_data)
    network_data=parsing_network(router_ip_data)
    

    # ARP 테이블 기반 연결성 분석
    routers=arp_data.keys()
    for r in routers:
        topology_data[r]={}
        topology_data[r]['Connectivity']={}
        topology_data[r]['Connectivity']['Terminal']={}
        topology_data[r]['Connectivity']['Router']={}

        for port in arp_data[r].keys():
            arp_ip=arp_data[r][port].keys()
            for ip in arp_ip:
                arp_mac=arp_data[r][port][ip]['mac-address']
                if ip_find(ip,router_ip_data)==False:
                    topology_data[r]['Connectivity']['Terminal'][ip]={}
                    topology_data[r]['Connectivity']['Terminal'][ip]['mac-address']=arp_mac
                    topology_data[r]['Connectivity']['Terminal'][ip]['via']=port


                else:
                    c_router,c_port,c_ip=ip_find(ip,router_ip_data)
                    topology_data[r]['Connectivity']['Router'][c_router]={}
                    topology_data[r]['Connectivity']['Router'][c_router]['ip']=c_ip
                    topology_data[r]['Connectivity']['Router'][c_router]['mac-address']=arp_mac
                    topology_data[r]['Connectivity']['Router'][c_router]['port']=c_port
                    topology_data[r]['Connectivity']['Router'][c_router]['via']=port

    # Route 테이블 기반 접근성 분석
    #접근성 확인, static 추가, route 우선순위 확인 
    route_routers=route_data.keys()
    for r in route_routers:
        topology_data[r]['Accessible']={}
        dest_list=route_data[r].keys()
        for dest in dest_list:
            protocol_type=route_data[r][dest]['protocol-name']
            dest_network=find_network(dest)
            if protocol_type=='Direct':
                topology_data[r]['Accessible'][dest_network]={}
                topology_data[r]['Accessible'][dest_network]['via']=r
            elif protocol_type=='OSPF':
                if 'next-hop' in route_data[r][dest]:
                    next_hop_lst=route_data[r][dest]['next-hop']
                    for next_hop in next_hop_lst:
                        next_ip=next_hop['to']
                        a_router,a_port,a_ip=ip_find(next_ip,router_ip_data)
                        topology_data[r]['Accessible'][dest_network]={}
                        topology_data[r]['Accessible'][dest_network]['via']=a_router
                    
            elif protocol_type=='Static':
                if 'next-hop' in route_data[r][dest]:
                    next_hop_lst=route_data[r][dest]['next-hop']
                    for next_hop in next_hop_lst:
                        if 'service' in next_hop.keys():
                            service=next_hop['service']
                        else:
                            next_ip=next_hop['to']
                            if ip_find(next_ip,router_ip_data)==False:
                                via_port=next_hop['via']
                                topology_data[r]['Accessible'][dest_network]={}
                                topology_data[r]['Accessible'][dest_network]['via']=via_port
                            else:
                                a_router,a_port,a_ip=ip_find(next_ip,router_ip_data)
                                topology_data[r]['Accessible'][dest_network]={}
                                topology_data[r]['Accessible'][dest_network]['via']=a_router
                            

                


    with open("./result_json/router_ip_data.json", 'w') as make_file:
        header.json.dump(router_ip_data,make_file,indent=4)
    
    with open("./result_json/arp_data.json", 'w') as make_file:
        header.json.dump(arp_data,make_file,indent=4)

    with open("./result_json/topology_data.json", 'w') as make_file:
        header.json.dump(topology_data,make_file,indent=4)

    with open("./result_json/route_data.json", 'w') as make_file:
        header.json.dump(route_data,make_file,indent=4)
    
    with open("./result_json/network_data.json", 'w') as make_file:
        header.json.dump(network_data,make_file,indent=4)


def parsing_router_ip(parsing_data):

    router_ip_data={}

    routers=parsing_data.keys()

    for router in routers:
        router_ip_data[router]={}
        for intf in parsing_data[router]['interfaces']:
            for lo_intf in parsing_data[router]['interfaces'][intf]['logical-interfaces']:
                if 'address-family' in parsing_data[router]['interfaces'][intf]['logical-interfaces'][lo_intf]:
                    address_name=parsing_data[router]['interfaces'][intf]['logical-interfaces'][lo_intf]['address-family'].keys()
                    for name in address_name:
                        if 'ifa-local' in parsing_data[router]['interfaces'][intf]['logical-interfaces'][lo_intf]['address-family'][name]:
                            ip_address=parsing_data[router]['interfaces'][intf]['logical-interfaces'][lo_intf]['address-family'][name]['ifa-local']
                            router_ip_data[router][ip_address]={}
                            router_ip_data[router][ip_address]['port']=lo_intf

    return router_ip_data


def parsing_arp(parsing_data):

    arp_data={}

    routers=parsing_data.keys()

    for r in routers:
        arp_data[r]={}
        for intf in parsing_data[r]['interfaces']:
            if 'logical-interfaces' in parsing_data[r]['interfaces'][intf]:
                for lo_intf in parsing_data[r]['interfaces'][intf]['logical-interfaces']:
                    if 'arp_table' in parsing_data[r]['interfaces'][intf]['logical-interfaces'][lo_intf]:
                        arp_data[r][lo_intf]={}
                        for arp in parsing_data[r]['interfaces'][intf]['logical-interfaces'][lo_intf]['arp_table']:
                            arp_ip=arp['ip-address']
                            arp_mac=arp['mac-address']
                            arp_data[r][lo_intf][arp_ip]={}
                            arp_data[r][lo_intf][arp_ip]['mac-address']=arp_mac



    return arp_data


def ip_find(arp_ip,router_ip_data):

    routers=router_ip_data.keys()

    for r in routers:
        for ip in router_ip_data[r].keys():
            if '/' not in arp_ip:
                ip_=ip.split('/')[0]
                if arp_ip==ip_:
                    port=router_ip_data[r][ip]['port']
                    return r,port,ip
            else:
                if arp_ip==ip:
                    port=router_ip_data[r][ip]['port']
                    return r,port,ip
       
 
    return False

def parsing_route(parsing_data):

    route_data={}

    routers=parsing_data.keys()

    for r in routers:
        if 'routing table' in parsing_data[r]: 
            route_data[r]=parsing_data[r]['routing table']['destination']
            
     
    return route_data


#     ip_data={} # 각 라우터의 ip주소에 따른 포트 정보 가지고 있다. 
#     network_data={} # 전체 네트워크의 네트워크 주소 구성정보
#     routing_data={} # 네트워크 라우터의  라우팅 정보
#     arp_data={}
#     ip_data=ip_match(json_data,ip_data) #ip_data에서 각 라우터 ip주소에 따른 포트 정보 매치시켜주는 함수 
#     # header.pprint.pprint(ip_data)
    
#     network_data=router_network(ip_data)
#     routing_data=parsing_routing_inf(json_data)
#     arp_data=parsing_arp_inf(json_data)

#     arp_router=arp_data.keys()

#     for router in arp_router:
#         header.topology_data[router]={}
#         header.topology_data[router]["Connectivity"]={}
#         header.topology_data[router]["Connectivity"]["Router"]={}
#         header.topology_data[router]["Connectivity"]["Terminal"]={}

#         for port in arp_data[router].keys():
#             for arp_ip in arp_data[router][port].keys():
#                     if ip_find(arp_ip,ip_data) !=False:
#                         c_router,c_port=ip_find(arp_ip,ip_data)
#                         header.topology_data[router]['Connectivity']['Router'][c_router]={}
#                         header.topology_data[router]['Connectivity']['Router'][c_router]['Interface']=c_port
#                         header.topology_data[router]['Connectivity']['Router'][c_router]['ip-address']=arp_ip
#                         header.topology_data[router]['Connectivity']['Router'][c_router]['mac-address']=arp_data[router][port][arp_ip]['mac-address']
#                         header.topology_data[router]['Connectivity']['Router'][c_router]['via']=port
#                     else:
#                         if 'nat' in arp_data[router][port][arp_ip].keys():
#                             header.topology_data[router]["Connectivity"]["Terminal"][arp_ip]={}
#                             header.topology_data[router]["Connectivity"]["Terminal"][arp_ip]['mac-address']=arp_data[router][port][arp_ip]['mac-address']
#                             header.topology_data[router]["Connectivity"]["Terminal"][arp_ip]['via']=port
#                         else:
#                             header.topology_data[router]["Connectivity"]["Terminal"][arp_ip]={}
#                             header.topology_data[router]["Connectivity"]["Terminal"][arp_ip]['mac-address']=arp_data[router][port][arp_ip]['mac-address']
#                             header.topology_data[router]["Connectivity"]["Terminal"][arp_ip]['via']=port
                    

#     # routers=json_data.keys()

#     # for router in routers:
        
#     #     header.topology_data[router]={}
#     #     header.topology_data[router]["Connectivity"]={}
#     #     header.topology_data[router]["Connectivity"]["Router"]={}
#     #     header.topology_data[router]["Connectivity"]["Terminal"]={}
#     #     header.topology_data[router]['Accesible']={}

#     #     # ARP 기반  연결성 분석


#     #     # for intf in json_data[router]['interfaces']:
#     #     #     if 'logical-interfaces' in json_data[router]['interfaces'][intf]:
#     #     #         for lo_intf in json_data[router]['interfaces'][intf]['logical-interfaces']:
#     #     #             if 'arp_table' in json_data[router]['interfaces'][intf]['logical-interfaces'][lo_intf]:
#     #     #                 for arp in json_data[router]['interfaces'][intf]['logical-interfaces'][lo_intf]['arp_table']:
#     #     #                     arp_ip=arp['ip-address']
#     #     #                     arp_mac=arp['mac-address']
#     #     #                     if ip_find(arp_ip,ip_data) !=False:
#     #     #                         c_router,c_port=ip_find(arp_ip,ip_data)
#     #     #                         header.topology_data[router]['Connectivity']['Router'][c_router]={}
#     #     #                         header.topology_data[router]['Connectivity']['Router'][c_router]['Interface']=c_port
#     #     #                         header.topology_data[router]['Connectivity']['Router'][c_router]['ip-address']=arp_ip
#     #     #                         header.topology_data[router]['Connectivity']['Router'][c_router]['mac-address']=arp_mac
#     #     #                         header.topology_data[router]['Connectivity']['Router'][c_router]['via']=lo_intf
#     #     #                     else:
#     #     #                          header.topology_data[router]["Connectivity"]["Terminal"][arp_ip]={}
#     #     #                          header.topology_data[router]["Connectivity"]["Terminal"][arp_ip]['mac-address']=arp_mac
#     #     #                          header.topology_data[router]["Connectivity"]["Terminal"][arp_ip]['via']=lo_intf


#     # 접근성 분석

#     routers=json_data.keys()

#     for router in routers:
        
#         if 'routing table' in json_data[router]: #라우팅 테이블이 있으면 접근성 분석
#             header.topology_data[router]['Accesible']={}
#             dest_list=routing_data[router].keys()
#             for dest in dest_list:
#                 protocol_type=routing_data[router][dest]['protocol-name']
#                 dest_network=find_network(dest)
#                 if protocol_type=='Direct':
#                     header.topology_data[router]['Accesible'][dest_network]={}
#                     header.topology_data[router]['Accesible'][dest_network]['via']=router
#                 elif protocol_type=='OSPF':
#                     if 'next-hop' in routing_data[router][dest]:
#                         next_hop_lst=routing_data[router][dest]['next-hop']
#                         for next_hop in next_hop_lst:
#                             next_ip=next_hop['to']
#                             for r in routers:
#                                 ip_lst=ip_data[r].keys()
#                                 for ip in ip_lst:
#                                     ip_sp=ip.split('/')[0]
#                                     if next_ip == ip_sp:
#                                         header.topology_data[router]['Accesible'][dest_network]={}
#                                         header.topology_data[router]['Accesible'][dest_network]['via']=r
                                        

def find_network(ip_address): # ip주소에서 서브넷에 따른 네트워크 부분 알아내는 함수

    network=ipaddress.IPv4Network(ip_address,strict=False)
    network_address=str(network.network_address)

    return network_address
    
def parsing_network(router_ip_data):

    network_data={}

    routers=router_ip_data.keys()

    for r in routers:
        ip_lst=router_ip_data[r].keys()
        for ip in ip_lst:
            if '/' in ip:
                network_part=find_network(ip)
                network_data[network_part]={}
                network_data[network_part][r]={}
    
    networks=network_data.keys()

    for router in routers:
        ip_lst=router_ip_data[router].keys()
        for ip in ip_lst:
            if '/' in ip:
                ip_network=find_network(ip)
                for network in networks:
                    if network==ip_network:
                        network_data[network][router]={}
                        port=router_ip_data[router][ip]["port"]
                        network_data[network][router][port]=ip

    

    return network_data




# def router_network(router_ip_port): # 각 라우터의 각 포트가 가지고 있는 네트워크 뽑음

#     network_data={}

#     routers=router_ip_port.keys()

#     for router in routers:
#         ip_lst=router_ip_port[router].keys()
#         for ip in ip_lst:
#             if '/' in ip : #ipv4 주소인 경우 
#                 network_part=find_network(ip)
#                 network_data[network_part]={}    
            

#     networks=network_data.keys()

#     for router in routers:
#         ip_lst=router_ip_port[router].keys()
#         for ip in ip_lst:
#             if '/' in ip:
#                 ip_network=find_network(ip)
#                 for network in networks:
#                     if network==ip_network:
#                         network_data[network][router]={}
#                         port=router_ip_port[router][ip]["port"]
#                         network_data[network][router][port]=ip

        
#     # header.pprint.pprint(network_data)
    
#     return network_data
        


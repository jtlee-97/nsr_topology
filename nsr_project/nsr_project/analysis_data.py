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
        json_data=header.json.load(f)

    ip_data={} # 각 라우터의 ip주소에 따른 포트 정보 가지고 있다. 
    network_data={} # 전체 네트워크의 네트워크 주소 구성정보
    routing_data={} # 네트워크 라우터의  라우팅 정보
    ip_data=ip_match(json_data,ip_data) #ip_data에서 각 라우터 ip주소에 따른 포트 정보 매치시켜주는 함수 
    # header.pprint.pprint(ip_data)
    

    routers=json_data.keys()

    for router in routers:
        
        header.topology_data[router]={}
        header.topology_data[router]["Connectivity"]={}
        header.topology_data[router]["Connectivity"]["Router"]={}
        header.topology_data[router]["Connectivity"]["Terminal"]={}
        header.topology_data[router]['Accesible']={}

        network_data=router_network(ip_data)

        routing_data=parsing_routing_inf(json_data)
        
        # 연결성 분석

        for intf in json_data[router]['interfaces']:
            if 'logical-interfaces' in json_data[router]['interfaces'][intf]:
                for lo_intf in json_data[router]['interfaces'][intf]['logical-interfaces']:
                    if 'arp_table' in json_data[router]['interfaces'][intf]['logical-interfaces'][lo_intf]:
                        for arp in json_data[router]['interfaces'][intf]['logical-interfaces'][lo_intf]['arp_table']:
                            arp_ip=arp['ip-address']
                            arp_mac=arp['mac-address']
                            if ip_find(arp_ip,ip_data) !=False:
                                c_router,c_port=ip_find(arp_ip,ip_data)
                                header.topology_data[router]['Connectivity']['Router'][c_router]={}
                                header.topology_data[router]['Connectivity']['Router'][c_router]['Interface']=c_port
                                header.topology_data[router]['Connectivity']['Router'][c_router]['ip-address']=arp_ip
                                header.topology_data[router]['Connectivity']['Router'][c_router]['mac-address']=arp_mac
                                header.topology_data[router]['Connectivity']['Router'][c_router]['via']=lo_intf
                            else:
                                 header.topology_data[router]["Connectivity"]["Terminal"][arp_ip]={}
                                 header.topology_data[router]["Connectivity"]["Terminal"][arp_ip]['mac-address']=arp_mac
                                 header.topology_data[router]["Connectivity"]["Terminal"][arp_ip]['via']=lo_intf


        # 접근성 분석
        
        if 'routing table' in json_data[router]: #라우팅 테이블이 있으면 접근성 분석
            dest_list=routing_data[router].keys()
            for dest in dest_list:
                protocol_type=routing_data[router][dest]['protocol-name']
                dest_network=find_network(dest)
                if protocol_type=='Direct':
                    header.topology_data[router]['Accesible'][dest_network]={}
                    header.topology_data[router]['Accesible'][dest_network]['via']=router
                elif protocol_type=='OSPF':
                    if 'next-hop' in routing_data[router][dest]:
                        next_hop_lst=routing_data[router][dest]['next-hop']
                        for next_hop in next_hop_lst:
                            next_ip=next_hop['to']
                            for r in routers:
                                ip_lst=ip_data[r].keys()
                                for ip in ip_lst:
                                    ip_sp=ip.split('/')[0]
                                    if next_ip == ip_sp:
                                        header.topology_data[router]['Accesible'][dest_network]={}
                                        header.topology_data[router]['Accesible'][dest_network]['via']=r
                                        
                                
                            
                            
                        



                    
                    


    with open("./result_json/topology_data.json", 'w') as make_file:
        header.json.dump(header.topology_data,make_file,indent=4)

    with open("./result_json/router_ip_port.json", 'w') as make_file:
        header.json.dump(ip_data,make_file,indent=4)

    with open("./result_json/network_data.json", 'w') as make_file:
        header.json.dump(network_data,make_file,indent=4)

    with open("./result_json/routing_data.json", 'w') as make_file:
        header.json.dump(routing_data,make_file,indent=4)


def ip_match(json_data,ip_data):

    routers=json_data.keys()

    for router in routers:
        ip_data[router]={}
        for intf in json_data[router]['interfaces']:
            for lo_intf in json_data[router]['interfaces'][intf]['logical-interfaces']:
                if 'address-family' in json_data[router]['interfaces'][intf]['logical-interfaces'][lo_intf]:
                    address_name=json_data[router]['interfaces'][intf]['logical-interfaces'][lo_intf]['address-family'].keys()
                    for name in address_name:
                        if 'ifa-local' in json_data[router]['interfaces'][intf]['logical-interfaces'][lo_intf]['address-family'][name]:
                            ip_address=json_data[router]['interfaces'][intf]['logical-interfaces'][lo_intf]['address-family'][name]['ifa-local']
                            ip_data[router][ip_address]={}
                            ip_data[router][ip_address]['port']=lo_intf



    return ip_data

def ip_find(ip_address,ip_data):
    
    routers=ip_data.keys()
    for router in routers:
        for data_ip in ip_data[router]:
            sp_data_ip=data_ip.split('/')[0]
            if ip_address==sp_data_ip:
                port=ip_data[router][data_ip]['port']
                return router, port
            
    return False


def find_network(ip_address): # ip주소에서 서브넷에 따른 네트워크 부분 알아내는 함수

    network=ipaddress.IPv4Network(ip_address,strict=False)
    network_address=str(network.network_address)

    return network_address
    

def router_network(router_ip_port): # 각 라우터의 각 포트가 가지고 있는 네트워크 뽑음

    network_data={}

    routers=router_ip_port.keys()

    for router in routers:
        ip_lst=router_ip_port[router].keys()
        for ip in ip_lst:
            if '/' in ip : #ipv4 주소인 경우 
                network_part=find_network(ip)
                network_data[network_part]={}    
            

    networks=network_data.keys()

    for router in routers:
        ip_lst=router_ip_port[router].keys()
        for ip in ip_lst:
            if '/' in ip:
                ip_network=find_network(ip)
                for network in networks:
                    if network==ip_network:
                        network_data[network][router]={}
                        port=router_ip_port[router][ip]["port"]
                        network_data[network][router][port]=ip

        
    # header.pprint.pprint(network_data)
    
    return network_data
        

  
def parsing_routing_inf(parsing_result): # 각 라우터의 라우팅 테이블 정보 파싱하는 함수 

    routing_data={}

    routers=parsing_result.keys()

    for router in routers:
        if 'routing table' in parsing_result[router]: #라우팅 테이블이 있으면 파싱시작 - 현재 논리적 시스템 라우팅 테이블 포함 안됨.. 추가 필요.
            routing_data[router]=parsing_result[router]['routing table']['destination']
            
    return routing_data
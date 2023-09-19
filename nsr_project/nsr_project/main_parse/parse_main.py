"""
=================================================
National Security Research Institute (NSR) 
Network topology automation analysis algorithm 
development project, Ajou University

Function     : parse_main.py
Prototype    : Separation of files and functions
Author       : Jongtae Lee (Ajou University)
Revision     : v1.1   2023.07.10 New
Modified     : 2023.08.14 By whdxo830
=================================================
"""

import header
import os

current_working_directory = os.getcwd()
print(current_working_directory)

def parse_main():
    path = './config_file'
    file_lst = header.os.listdir(path)
    order = ['conf', 'interface', 'arp', 'route']
    #file_lst.sort(key=lambda x: (int(x.split('_')[0][1:]), order.index(x.split('_')[1].split('.')[0])))
    file_lst.sort(key=lambda x: order.index(x.split('_')[1].split('.')[0]))
    
    for file in file_lst:
        filepath = path + '/' + file
    
        # router-based parsing (need to add device separation code in the future)
        match = header.re.search(r'_(\w+).xml', file)
        if match:
            if match.group(1) == 'arp':
                # print(filepath)
                header.parse_xml_arp(filepath)
            if match.group(1) == 'conf':
                # print(filepath)
                header.parse_xml_conf(filepath)
            if match.group(1) == 'route':
                # print(filepath)
                header.parse_xml_route(filepath)
            if match.group(1) == 'interface':
                # print(filepath)
                header.parse_xml_interface(filepath)

    # convert json format, always reset and new write (view: https://jsonlint.com/)
    result_path = '../result_json/parsing_data.json'
    with open(result_path, 'w') as f:
        header.json.dump(header.parsing_data, f, indent=4)
    

    # current_datetime = datetime.datetime.now()
    # formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    # result_directory = 'g:\\내 드라이브\\[1] Ajou University\\[프로젝트]\\[1] 네트워크 토폴로지 분석 자동화 연구\\연구\\(00) Main Code (rev_0814)\\nsr_project\\nsr_project\\result_json'
    # result_file_name = f'parsing_data_{formatted_datetime}.json'
    # result_path = os.path.join(result_directory, result_file_name)
    # with open(result_path, 'w') as f:
    #     json.dump(header.parsing_data, f, indent=4)
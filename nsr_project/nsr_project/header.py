"""
=================================================
National Security Research Institute (NSR) 
Network topology automation analysis algorithm 
development project, Ajou University

Function     : header.py
Prototype    : import module
Author       : J.T Lee (Ajou University)
Revision     : v1.1   2023.07.10 New
Modified     : 2023.08.14
=================================================
"""

import xml.etree.ElementTree as ET
import pprint
import json
import re
import os
import shutil
import datetime

from analysis_data import analysis_data
from main_parse.parse_xml_conf import parse_xml_conf
from main_parse.parse_xml_arp import parse_xml_arp
from main_parse.parse_xml_interface import parse_xml_interface
from main_parse.parse_xml_route import parse_xml_route
from main_parse.parse_main import parse_main

parsing_data = {}
topology_data={}


def init_folder():
    path=os.getcwd()
    print('yes')
    lg_sys_folder=os.path.join(path,'logical_systems')
    result_folder=os.path.join(path,'result_json')

    delete_folder(lg_sys_folder)
    delete_folder(result_folder)



def delete_folder(folder_path):
    file_list=os.listdir(folder_path)
    if len(file_list)!=0 :
        for file_name in file_list:
            file_path=os.path.join(folder_path,file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
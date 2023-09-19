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
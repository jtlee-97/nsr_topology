"""
=================================================
National Security Research Institute (NSR) 
Commissioned Research Project, Ajou University

Function     : header.py
Prototype    : import module
Author       : Jongtae Lee (Ajou University)
Revision     : v1.1   2023.07.10 New
Modified     : 2023.07.12 By whdxo830
=================================================
"""

import xml.etree.ElementTree as ET
import pprint
import json
import re
import os


from parse_xml_conf import parse_xml_conf
from parse_xml_arp import parse_xml_arp
from parse_xml_interface import parse_xml_interface
from parse_xml_route import parse_xml_route


parse_data = {}
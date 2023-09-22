"""
=================================================
National Security Research Institute (NSR) 
Network topology automation analysis algorithm 
development project, Ajou University

Function     : __main__.py
Prototype    : __main__
Author       : Jongtae Lee (Ajou University)
Revision     : v1.2   2023.08.10 New
Modified     : 2023.09.19
=================================================
"""
import header

while True:
    answer = input("Would you like to update with new data? (Y/N) : ")
    if answer == 'Y' or answer == 'y':
        header.parse_main()
        break  
    elif answer == 'N' or answer == 'n':
        break  
    else:
        print("Invalid input. Please enter 'Y' or 'N'.")

# Analysis Process
#header.analysis_data() # Test ver. for Mid.

# Algorithm Process
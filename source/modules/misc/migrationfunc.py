"""
title           : migrationfunc.py
description     : includes 
                  a) functions to manipulate a dictionary that representes 
                     the consumption of a Raspberry Pi resources
                  b) functions for creating a json file from the dictionary and 
                     reading it from the file and converting it back to the original 
                     dictionary
source          :  
author          : Carlos Molina-Jimenez (Carlos.Molina@cl.cam.ac.uk)
date            : 22 Feb 2017
institution     : Computer Laboratory, University of Cambridge
version         : 1.0
usage           : 
notes           :
compile and run : % python3 migrationfunc.py
python_version  : Python 2.7.12    
====================================================
"""


import json


def get_ith_ele(i, migration_lst):
    try: 
       return ((migration_lst[i][0],    migration_lst[i][1],
               migration_lst[i][2],     migration_lst[i][3],
               migration_lst[i][4]))
    except IndexError:
       print("List index error")

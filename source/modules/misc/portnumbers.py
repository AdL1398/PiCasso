"""
title           : portnumbers.py
description     : finds a free port number: 
                :  - the returned number is an integer that belongs to the  
                :    low_bound and upper_bound interval and not listed in 
                :    the list of assigned ports [port2, port1, port9, ...]
                :   
author          : Carlos Molina-Jimenez (Carlos.Molina@cl.cam.ac.uk)
date            : 27 Feb 2017, 
institution     : Computer Laboratory, University of Cambridge
version         : 1.0
usage           : 
notes           :
compile and run : % python portnumber.py
python_version  : Python Python 2.7.12
====================================================
"""

def n_in_list(n, lst):
    if (n in lst):
       return True
    else:
       return False


"""
Expects:
-a list (possibly empty) of integers with values
   between low_bound and upper_bound.
- two integers low_bound < upper_bound

Returns 
- an integer withy value between low_bound and upper_bound
   and not included in the list.  
-1 when the list includes all the integers with values 
   between low_bound and upper_bound.
-2 when the list expands beyond the range of port numbers
-3 when the low_bound is greater than the upper_bound
"""
def get_free_port(lst_assigned_ports, low_bound, upper_bound):
    if (low_bound >= upper_bound):
       return (-3)
    elif (len(lst_assigned_ports) > (upper_bound - low_bound + 1)):
       return (-2)
    elif len(lst_assigned_ports) == 0:
       return low_bound
    else:
       for portN in range(low_bound, upper_bound):
           if (n_in_list(portN, lst_assigned_ports)):
              pass
           else:
              return (portN)
       return(-1)



#!/usr/bin/env python
"""
title           : dedata.py
description     : This is the implementation of the decision engine of the UMOBILE
                : project. 
source          : 
author          : Carlos Molina-Jimenez (Carlos.Molina@cl.cam.ac.uk)
institution     : Computer Laboratory, University of Cambridge
date            : 26 Feb 2017
version         : 1.0
usage           : 
notes           :
compile and run : % python dedata.py 
python_version  : Python 2.7.12   
====================================================

to change PiID value to SEG_1 SEG_2 after talking to adisorn
pi_status= {
    'PiID': '192.0.0.1',
    'hardResources': {'cpu': 'A 1.2GHz 64-bit quad-core ARMv8 CPU', 'mem': '1', 'disk': '32'}, 
    'softResources': {'OS': 'Linux'},
    'resourceUsage': {'cpuUsage': '30', 'cpuLoad': '70', 'memUsage':'20'},
    'containers':    [{'id': '64c1f6e0e5c19f9da2', 'cpuUsage': '23', 'memUsage': '3636', 'name': 'web1','status': 'Up 39 second', 'image': 'hypriot/rpi-busybox-httpd:latest'}
                     ]
   }


"""

import portnumbers
from modules.tools import pidict

Low_Bound=   8080   # low bound of port numbers 
Upper_Bound= 9090   # upper bound of port numbers

migrFolderPath= "./PIstatus/"

# Definition of the class. It has three methods 
class dedata(object):


   migration_rec_default= {
    'PiID'        :   'SEG_1',
    'PiIP'        :   '192.0.0.1',
    'image'       :   'hypriot/rpi-busybox-httpd:latest',
    'port'        :   '8001',
    'containerID' :   'some'
    }


   def __init__(self, jsonfolderpath):
      self.jsonfolderpath= jsonfolderpath 


   """
   Returns a list of file names found in a folder
   that stores the json files that correspond to the
   consumption records of each Pi.
   """
   def __get_lst_of_jsonfiles(self):
       import os.path
       path = self.jsonfolderpath 
       lst= [fname for fname in os.listdir(path)
             if (os.path.isfile(os.path.join(path, fname)) and (fname.find("SEG")>=0))]
       return (lst)


   """
   Expects a list of file names, each with a json object that represent
   a dictionary.
   Returns a list with the corresponding dictionaries.
   """
   def __jsonfiles_to__dict(self,lst_of_jsonfiles):
       import os.path
       path = self.jsonfolderpath
       lst= [piresources.read_jsonFile(os.path.join(path, fname)) for fname in lst_of_jsonfiles]
       return (lst)

   """
   Return a list of tuples. Each tuple corresponds to the resources
   consumed by a container running in a given Pi.
   The dictionaries of each Pi are stored in a list.
   l_dict[0] corresponds to the first Pi in the list, l_dict[1] corresponds
   to the second Pi, etc. In this example, which I'm using for testing,
   I'm manually selecting the Pi: l_dict[0]
   def __get_allContainersRU_of__Pi(self,dictionary):
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
       lst_of_tuples= piresources.get_allResources_of_allContainers_of_Pi(l_dict[2])
       return(lst_of_tuples[0])
   """ 

   """
   Expects: 
   -a list (possibly empty) of integers with values
     between low_bound and upper_bound.
   - two integers low_bound < upper_bound
   Returns an integer withy value between low_bound and upper_bound
   and not included in the list.  Returns -1 when the list includes
   all the integers with values between low_bound and upper_bound
   """ 
   def __get_free_portNum(self, lst_of_assigned_ports, low_bound, upper_bound):
       portNum= portnumbers.get_port(lst_of_assigned_ports, low_bound, upper_bound)
       return (portNum)


   """
   This funnction creates a json file on disk. I implemented
   for testing only: 21 Feb 2017
   """
   def create_json_file(self, pi_status, fname):
       import os.path
       piresources.create_jsonFile(pi_status, os.path.join(self.jsonfolderpath, fname))


   def prt_jsonfolderpath(self):
      print ("The location of the files is: " + self.jsonfolderpath)



   """
   returns the path where the json folder is located. 
   """
   def get_jsonfolderpath(self):
       return self.jsonfolderpath


   """
   returns the number of PIs that have contributed
   json files to the json folder
   """
   def get_num_of_PIs(self):
       return (len(self.__get_lst_of_jsonfiles()))


   """
   returns true if there is one or more json files ready
   for examination in the json folder path. Return False 
   otherwise. 
   """
   def are_monitoringFiles_ready(self):
       if (len(self.__get_lst_of_jsonfiles()) > 0) :
          return True
       else:
          return False 
       

   """
   returns a list that contains the names of the json files:
   [jsonFileNamePi, jsonFileNamePi, ..., jsonFileNamePi] 
   One json file for each Pi
   """
   def get_lst_of_jsonfiles(self):
       return (self.__get_lst_of_jsonfiles())


   """
   returns a list that contains the dictionary of all Pis
   [Pi_dict, Pi_dict, ... Pi_dict] 
   Each Pi_dict represents the resource consumption of the Pi.
   """
   def get_lst_of_dictionaries(self):
       lst_jsonfiles= self.__get_lst_of_jsonfiles()
       return(self.__jsonfiles_to__dict(l_jsonfiles))


   def get_resourceUsage(self):
       lst_jsonfiles= self.__get_lst_of_jsonfiles()
       lst_dict= self.__jsonfiles_to__dict(lst_jsonfiles)
       return(piresources.get_resourceUsage(lst_dict[0]))

   def get_lenL(self):
       lst_jsonfiles= self.__get_lst_of_jsonfiles()
       lst_dict= self.__jsonfiles_to__dict(lst_jsonfiles)
#     return(piresources.get_resourceUsage(lst_dict[0]))
       return(len(lst_dict))

   """
   Returns a list of tuples. A tuple respresents the
   resource usage of each PI: 
   [(PiID, cpuUsage, cpuLoad,memUsage), (PiID, cpuUsage, cpuLoad,memUsage), ...] 
   """
   def get_resourceUsage_of_allPis(self):
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
       lst= [(pi_status['PiID'], 
              pi_status['resourceUsage']['cpuUsage'],
              pi_status['resourceUsage']['cpuLoad'],
              pi_status['resourceUsage']['memUsage'])
              for pi_status in l_dict]
       return (lst) 

   """
   Expects the value of the cpuUsageThreshold.
   Returns a tuple of two lists:
   The first element of the tuple is the list of Pis with cpuUsage above the
   threshold. 
   The second element of the tuple is a list of Pis with cpuUsage 
   equal or below the threshold.
   Both lists are lists of tuples:
   [(PiID, cpuUsage), (PiID, cpuUsage,) , ...] 
   """
   def __get_lsts_of_PiIDs_of_cpuUsageExhausted_and_noExaustedPis(self,cpuUsageThreshold):
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
       l_exhaustedPis =   []
       l_noexhaustedPis = []
       for j in range (0, len(l_dict)):
           pi_cpuUsage= int(l_dict[j]['resourceUsage']['cpuUsage'])
           if (pi_cpuUsage > cpuUsageThreshold):
              l_exhaustedPis.append((l_dict[j]['PiID'],l_dict[j]['resourceUsage']['cpuUsage']))
           else:
              l_noexhaustedPis.append((l_dict[j]['PiID'],l_dict[j]['resourceUsage']['cpuUsage']))
       return(l_exhaustedPis, l_noexhaustedPis) 



   """
   Return a tuple with two lists: 
   lst1: the list of PiIDs with exhausted cpuUsage and the value of the cpuUsage
   lst2: the list of PiIDs with noexhausted cpuUsage and the value of the cpuUsage
   Each list has the following format:
   [(PiID, cpuUsage), (PiID, cpuUsage), ..., (PiID, cpuUsage)]
   """
   def get_PiIDs_and_cpuUsage_of_Pis(self,cpuUsageThreshold):
       tuple= self.__get_lsts_of_PiIDs_of_cpuUsageExhausted_and_noExaustedPis(cpuUsageThreshold) 
       return(tuple[0], tuple[1])


   """
   Return the list of PiIDs with exhausted cpuUsage
   [PiID, PiID, ,..., PiID]
   """
   def get_PiIDs_of_cpuUsageExhaustedPis(self,cpuUsageThreshold):
       tuple= self.__get_lsts_of_PiIDs_of_cpuUsageExhausted_and_noExaustedPis(cpuUsageThreshold) 
       l_of_tuples= tuple[0]
       l_of_exhausted_PiIDs=[ele[0] for ele in l_of_tuples]
       return l_of_exhausted_PiIDs
# The following 4 lines work OK as well
#      l=[]
#       for j in l_of_tuples:
#           l.append(j[0])
#       return l 


   """
   Return the list of PiIDs with noexhausted cpuUsage
   [PiID, PiID, ,..., PiID]
   """
   def get_PiIDs_of_cpuUsageVigorousPis(self,cpuUsageThreshold):
       tuple= self.__get_lsts_of_PiIDs_of_cpuUsageExhausted_and_noExaustedPis(cpuUsageThreshold) 
       l_of_tuples= tuple[1]
       l_of_noexhausted_PiIDs=[ele[0] for ele in l_of_tuples]
       return l_of_noexhausted_PiIDs
# The following 4 lines work OK as well
#      l=[]
#      for j in l_of_tuples:
#          l.append(j[0])
#      return l 




   """
   Returns a list of lists: [ [l_of_tuples], [l_of_tuples], ...]
   Each l_of_tuples corresponds to a Pi and has as many tuples
   as containers in the Pi: [(tuple ), (tuple ), ...].
   Each tuple contains the resource consumption of a container:
   (PiID, id, cpuUsage, memUsage, name, status, image).
   ...
   """ 
   def get_RU_of_allContainers_of_allPis(self):
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
       
       lst= [ [(pi_status['PiID'], 
               cont['id'],
               cont['cpuUsage'],
               cont['memUsage'],
               cont['name'],
               cont['status'],
               cont['image']) for cont in pi_status['containers']]
            for pi_status in l_dict]
       return (lst) 



   """
   Expects the value of  cpuUsageThreshold and
   returns a tuple of a list of exhausted and a list of vigorous containers
   running in a Pi:
   exhausted   list [(containerID, cpuUsage), (containerID, cpuUsage), ...]
   vigorous list [(containerID, cpuUsage), (containerID, cpuUsage), ...]
   This function is for testing only, the dictionary of the Pi is provided
   manually in the code as l_dict[1]
   """ 
   def get_cpuUsage_of_exhausted_and_vigorous_Conta_of_Pi(self,cpuUsageThreshold):
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
       lst_of_exh= piresources.get_cpuUsageExhaustedContainers_of_Pi(l_dict[1],cpuUsageThreshold)
       lst_of_vigorous= piresources.get_cpuUsageVigorousContainers_of_Pi(l_dict[1],cpuUsageThreshold)
       return (lst_of_exh, lst_of_vigorous)

   def get_cpuUsage_of_exhausted_and_vigorous_Conta_of_Pi_2(self,cpuUsageThreshold):
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
       lst_of_exh= piresources.get_cpuUsageExhaustedContainers_of_Pi(l_dict[1],cpuUsageThreshold)
       lst_of_vigorous= piresources.get_cpuUsageVigorousContainers_of_Pi(l_dict[1],cpuUsageThreshold)
       return (lst_of_exh, lst_of_vigorous)

   def get_cpuUsage_of_exhausted_and_vigorous_Conta_of_Pi_5(self,cpuUsageThreshold):
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
       lst_of_exh= piresources.get_cpuUsageExhaustedContainers_of_Pi(l_dict[4],cpuUsageThreshold)
       lst_of_vigorous= piresources.get_cpuUsageVigorousContainers_of_Pi(l_dict[4],cpuUsageThreshold)
       return (lst_of_exh, lst_of_vigorous)


   """
   Expects the value of  cpuUsageThreshold and
   returns a tuple of a list of exhausted and a list of vigorous containers
   running in a Pi:
   exhausted list    [(containerID, cpuUsage), (containerID, cpuUsage), ...]
   vigorous  list    [(containerID, cpuUsage), (containerID, cpuUsage), ...]
    del: This function is for testing only, the dictionary of the Pi is provided
    del: manually in the code as l_dict[1]
   """ 
   def __get_lsts_exha_and_vigo_conta_of_Pi(self, pi_dict, cpuUsageThreshold):
       lst_of_exhausted= piresources.get_cpuUsageExhaustedConta_of_Pi(pi_dict, cpuUsageThreshold)
       lst_of_vigorous= piresources.get_cpuUsageVigorousConta_of_Pi(pi_dict, cpuUsageThreshold)
       return (lst_of_exhausted, lst_of_vigorous)


   """
   Expects the value of  cpuUsageThreshold and
   returns a tuple of a list of exhausted and a list of vigorous containers
   running in a Pi:
   exhausted   list [(containerID, cpuUsage, image, port_host), (containerID, cpuUsage, image, port_host), ...]
   vigorous    list [(containerID, cpuUsage, image, port_host), (containerID, cpuUsage, image, port_host), ...]
   """ 
   def __get_lists_exhausted_and_vigorous_containers_of_Pi(self, pi_dict, cpuUsageThreshold):
       lst_of_exhausted= piresources.get_cpuUsageExhaustedContainers_of_Pi(pi_dict, cpuUsageThreshold)
       lst_of_vigorous= piresources.get_cpuUsageVigorousContainers_of_Pi(pi_dict,cpuUsageThreshold)
       return (lst_of_exhausted, lst_of_vigorous)




   """
   Returns a list of tuples of the form ((PiID,cpuUsage), l_exhausted_c, l_vigorous_c)),
   where the lists are expanded as follows:
   [((PiID, cpuUsage), 
     [(containerId, cpuUsage, image, port_host), (containerId, cpuUsage, image, port_host), ...],  <- l_exhausted_c
     [(containerId, cpuUsage, image, port_host), (containerId, cpuUsage, image, port_host), ...]), <- l_vigorous_c

    ((PiId, cpuUsage), 
     [(containerId, cpuUsage, image, port_host), (containerId, cpuUsage, image, port_host), ...],
     [(containerId, cpuUsage, image, port_host), (containerId, cpuUsage, image, port_host), ...]),
    ...
   ]
   A container is included in l_exhausted_c if its cpuUsage > cpuUsageThreshold otherwise it is
   included in l_vigorous_c
   One or both lists might be empty.
   The cpuUsage of the PiID might be less, equal or greater them cpuUsageThreshold
   """ 
   def __get_allPis_with_cpuUsage_of_exhausted_and_vigorous_containers(self, l_dict, cpuUsageThreshold):
       l_of_Pis_with_containers=[]
       for d in l_dict:
         l_of_t= self.__get_lists_exhausted_and_vigorous_containers_of_Pi(d, cpuUsageThreshold)
         l_of_Pis_with_containers.append( ((d['PiID'], d['resourceUsage']['cpuUsage']), l_of_t[0], l_of_t[1]) )
       return (l_of_Pis_with_containers)



   """
   Returns a list of tuples of the form ((PiID,cpuLoad), l_exhausted_c, l_vigorous_c)),
   where the lists are expanded as follows:
   [((PiID, cpuLoad), 
     [(containerId, cpuUsage, image, port_host), (containerId, cpuUsage, image, port_host), ...],  <- l_exhausted_c
     [(containerId, cpuUsage, image, port_host), (containerId, cpuUsage, image, port_host), ...]), <- l_vigorous_c

    ((PiId, cpuLoad), 
     [(containerId, cpuUsage, image, port_host), (containerId, cpuUsage, image, port_host), ...],
     [(containerId, cpuUsage, image, port_host), (containerId, cpuUsage, image, port_host), ...]),
    ...
   ]
   A container is included in l_exhausted_c if its cpuUsage > cpuUsageThreshold otherwise it is
   included in l_vigorous_c
   One or both lists might be empty.
   The cpuLoad of the PiID might be less, equal or greater than cpuLoadThreshold
   """ 
   def __get_allPis_cpuLoad_with_cpuUsage_of_exhausted_and_vigorous_containers(self, l_dict, cpuUsageThreshold):
       l_of_Pis_with_containers=[]
       for d in l_dict:
         l_of_t= self.__get_lists_exhausted_and_vigorous_containers_of_Pi(d, cpuUsageThreshold)
         l_of_Pis_with_containers.append( ((d['PiID'], d['resourceUsage']['cpuLoad']), l_of_t[0], l_of_t[1]) )
       return (l_of_Pis_with_containers)


   """
   Expects a cpuUsageThreshold that determine exhaustion of cpuUsage
   Returns a list of Pi that have only vigorous containers (cpuUsage <= cpuUsageThreshold).
   The format of the returnes list:
   [((PiID, cpuUsage), [(containerId, cpuUsage, image, port_host), 
                        (containerId, cpuUsage, image, port_host), ...]),

   ((PiID, cpuUsage), [(containerId, cpuUsage, image, port_host), 
                        (containerId, cpuUsage, image, port_host), ...]),
   ...
   ]
   The cpuUsage associated to PiID can be vigorous (less or equal than cpuUsageThreshold or 
   exhusted (cpuUsage > cpuUsageThreshold)
   """
   def get_allPis_with_cpuUsageVigorous_containers(self, cpuUsageThreshold): 
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
       l_of_tu= self.__get_allPis_cpuLoad_with_cpuUsage_of_exhausted_and_vigorous_containers(l_dict, cpuUsageThreshold) 
       l_of_Pis_with_vigorous_containers=[]
       for pi in l_of_tu:
           PiID_cpuUsage= (pi[0][0], pi[0][1])
           if (len(pi[1]) == 0):                      # pi[1] is list of exahusted containers 
              l_of_Pis_with_vigorous_containers.append((PiID_cpuUsage, pi[2]))
       return (l_of_Pis_with_vigorous_containers)     # pi[2] is list of vigorous containers


   """
   Expects a cpuUsageThreshold that determine exhaustion of cpuUsage
   Returns a list of Pi that have only vigorous containers (cpuUsage <= cpuUsageThreshold).
   The format of the returnes list:
   [((PiID, cpuLoad), [(containerId, cpuUsage, image, port_host), 
                        (containerId, cpuUsage, image, port_host), ...]),

   ((PiID, cpuLoad), [(containerId, cpuUsage, image, port_host), 
                        (containerId, cpuUsage, image, port_host), ...]),
   ...
   ]
   The cpuUsage associated to PiID can be vigorous (less or equal than cpuUsageThreshold or 
   exhusted (cpuUsage > cpuUsageThreshold)
   """
   def get_allPiscpuLoad_with_cpuUsageVigorous_containers(self, cpuUsageThreshold): 
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
       l_of_tu= self.__get_allPis_cpuLoad_with_cpuUsage_of_exhausted_and_vigorous_containers(l_dict, cpuUsageThreshold) 
       l_of_Pis_with_vigorous_containers=[]
       for pi in l_of_tu:
           PiID_cpuLoad= (pi[0][0], pi[0][1])
           if (len(pi[1]) == 0):                      # pi[1] is list of exahusted containers 
              l_of_Pis_with_vigorous_containers.append((PiID_cpuLoad, pi[2]))
       return (l_of_Pis_with_vigorous_containers)     # pi[2] is list of vigorous containers


   """
   Expects a cpuUsageThreshold that determine exhaustion of cpuUsage
   Returns a list of Pi with exhausted containers (cpuUsage > cpuUsageThreshold).
   The format of the returnes list:
   [((PiID, cpuUsage), [(containerId, cpuUsage, image, port_host), 
                        (containerId, cpuUsage, image, port_host), ...]),

   ((PiID, cpuUsage), [(containerId, cpuUsage, image, port_host), 
                        (containerId, cpuUsage, image, port_host), ...]),
   ...
   ]

   The cpuUsage associated to PiID can be vigorous (less or equal than cpuUsageThreshold or 
   exhusted (cpuUsage > cpuUsageThreshold)
   """
   def get_allPis_with_cpuUsageExhausted_containers(self, cpuUsageThreshold): 
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
       l_of_tu= self.__get_allPis_with_cpuUsage_of_exhausted_and_vigorous_containers(l_dict, cpuUsageThreshold) 
       l_of_Pis_with_exhausted_containers=[]
       for pi in l_of_tu:
           PiID_cpuUsage= (pi[0][0], pi[0][1]) # pi[1] is list of exahusted containers
           if (len(pi[1]) > 0):                # I want Pis with at least one exhausted container  
              l_of_Pis_with_exhausted_containers.append((PiID_cpuUsage, pi[1]))
       return (l_of_Pis_with_exhausted_containers) 


   """
   Expects a cpuUsageThreshold that determine exhaustion of cpuUsage
   Returns a list of Pi with exhausted containers (cpuUsage > cpuUsageThreshold).
   The format of the returnes list:
   [((PiID, cpuLoad), [(containerId, cpuUsage, image, port_host), 
                        (containerId, cpuUsage, image, port_host), ...]),

   ((PiID, cpuLoad), [(containerId, cpuUsage, image, port_host), 
                        (containerId, cpuUsage, image, port_host), ...]),
   ...
   ]

   The cpuUsage associated to PiID can be vigorous (less or equal than cpuUsageThreshold or 
   exhusted (cpuUsage > cpuUsageThreshold)
   """
   def get_allPiscpuLoad_with_cpuUsageExhausted_containers(self, cpuUsageThreshold): 
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
#      l_of_tu= self.__get_allPis_with_cpuUsage_of_exhausted_and_vigorous_containers(l_dict, cpuUsageThreshold) 
       l_of_tu= self.__get_allPis_cpuLoad_with_cpuUsage_of_exhausted_and_vigorous_containers(l_dict, cpuUsageThreshold) 
       l_of_Pis_with_exhausted_containers=[]
       for pi in l_of_tu:
           PiID_cpuLoad= (pi[0][0], pi[0][1]) # pi[1] is list of exahusted containers
           if (len(pi[1]) > 0):                # I want Pis with at least one exhausted container  
              l_of_Pis_with_exhausted_containers.append((PiID_cpuLoad, pi[1]))
       return (l_of_Pis_with_exhausted_containers) 



   """
   Expects a the PiID of a Pi, for example SEG_1.
   Returns a list with all the port numbers (INTEGERS) in use by the Pi 
   The format of the returned list of int:
   [port_host, port_host, ....] if PiID found and containers running in Pi
   []                           if PiID found but no containers running in Pi
   [-1]                         if PiID not found
   """
   def __get_porthosts_of_pi(self, PiID): 
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
       l_of_porthost=[-1]
       for pi in l_dict: # needs proection against PiID not found
           if (pi['PiID']== PiID): 
              l_of_porthost=[]
              l_of_conts= pi['containers']
              for c in l_of_conts:
                    port_host= c['port_host'] 
                    l_of_porthost.append(int(port_host))
       return(l_of_porthost)
                      

   """
   Returns a list with all Pis and the port numbers (INTEGERS) in use by the Pi 
   The format of the returned list:
   [(PiID, [port_host, port_host, ....]),  # each port_host is an int
    (PiID, [port_host, port_host, ....]),
    ...
   ]
   """
   def get_pis_and_porthosts(self): 
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
       l_of_pi_with_ports=[]

       for pi in l_dict:
           PiID= pi['PiID']               # get next Pi
           l_of_contas= pi['containers']  # get lst of containers of Pi

           l_of_contas_ports= []    # store ports used by containers of current Pi
           for conta in l_of_contas: 
               port_host= conta['port_host'] 
               l_of_contas_ports.append(int(port_host)) # include port in the list
           l_of_pi_with_ports.append((PiID,l_of_contas_ports))  # include a tuple in the
                                                        # return list
       return(l_of_pi_with_ports)



   """
   Returns a list with all Pis and the port numbers (INTEGERS) in use by the Pi 
   The format of the returned list:
   [((PiID,cpuLoad), [port_host, port_host, ....]),  # each port_host is an int
    ((PiID,cpuLoad), [port_host, port_host, ....]),
    ...
   ]
   """
   def get_pis_cpuLoad_and_porthosts(self): 
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
       l_of_pi_with_ports=[]

       for pi in l_dict:
           PiID=     pi['PiID']  # get next Pi
           cpuLoad= pi['resourceUsage']['cpuLoad']
           l_of_contas= pi['containers']  # get lst of containers of Pi

           l_of_contas_ports= []    # store ports used by containers of current Pi
           for conta in l_of_contas: 
               port_host= conta['port_host'] 
               l_of_contas_ports.append(int(port_host)) # include port in the list
           l_of_pi_with_ports.append(((PiID,cpuLoad),l_of_contas_ports))  # include a tuple in the
                                                        # return list
       return(l_of_pi_with_ports)

   """
   Returns a list with all Pis and the port numbers (INTEGERS) in use by the Pi 
   The format of the returned list:
   [((PiID,cpuUsaga), [port_host, port_host, ....]),  # each port_host is an int
    ((PiID,cpuUsage), [port_host, port_host, ....]),
    ...
   ]
   """
   def get_pis_cpuUsage_and_porthosts(self): 
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
       l_of_pi_with_ports=[]

       for pi in l_dict:
           PiID=     pi['PiID']  # get next Pi
           cpuUsage= pi['resourceUsage']['cpuUsage']
           l_of_contas= pi['containers']  # get lst of containers of Pi

           l_of_contas_ports= []    # store ports used by containers of current Pi
           for conta in l_of_contas: 
               port_host= conta['port_host'] 
               l_of_contas_ports.append(int(port_host)) # include port in the list
           l_of_pi_with_ports.append(((PiID,cpuUsage),l_of_contas_ports))  # include a tuple in the
                                                        # return list
       return(l_of_pi_with_ports)



   """
   Expects a cpuUsageThreshold that determine exhaustion of cpuUsage
   Returns a list of all Pis with 
    - cpuUsage
    - ports assigned to containers 
   The format of the returnes list:
   [((PiID, cpuUsage), [port_host, port_host, port_host, ....]),
    ((PiID, cpuUsage), [port_host, port_host, port_host, ....]),
    ...
   ]
   The cpuUsage associated to PiID can be vigorous (less or equal than 
   cpuUsageThreshold or exhusted (cpuUsage > cpuUsageThreshold)
   """
   def get_allPis_with_cpuUsage_and_ports(self, cpuUsageThreshold): 
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
       l_of_tu= self.__get_allPis_with_cpuUsage_of_exhausted_and_vigorous_containers(l_dict, cpuUsageThreshold) 
       l_of_Pis_and_ports =[]
       for pi in l_of_tu:
           PiID_cpuUsage= (pi[0][0], pi[0][1]) 
           l_of_ports =[]
           
           l_exha= pi[1] # p[1] is list of exahusted containers          
           for exhcont in l_exha:
              l_of_ports.append(exhcont[3])  # This index dependent solution is not
                                             # flexible. The list should be dictionaries.
           l_vigo= pi[2] # p[2] is list of exahusted containers          
           for vigocont in l_vigo:
              l_of_ports.append(vigocont[3])
           tu= (PiID_cpuUsage, l_of_ports)
               
           l_of_Pis_and_ports.append(tu)
       return (l_of_Pis_and_ports) 


   """
   Expects a cpuUsageThreshold that determine exhaustion of cpuUsage
   Returns a list of all Pis with 
    - cpuUsage
    - ports assigned to containers 
   The format of the returnes list:
   [((PiID, cpuUsage), [port_host, port_host, port_host, ....]),
    ((PiID, cpuUsage), [port_host, port_host, port_host, ....]),
    ...
   ]
   The cpuUsage associated to PiID is equal or less that cpuUsageThreshold
   the cpuUsage of the container (not include in the list) to the
   containers associated to each port might be less, equal or greater than 
   cpuUsageThreshold 
   """
   def get_allPis_with_vigorous_cpuUsage_and_ports(self, cpuUsageThreshold):
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
       l_of_tu= self.__get_allPis_with_cpuUsage_of_exhausted_and_vigorous_containers(l_dict, cpuUsageThreshold) 
       l_of_Pis_and_ports =[]
       for pi in l_of_tu:
         if (int(pi[0][1]) <= cpuUsageThreshold):
           PiID_cpuUsage= (pi[0][0], pi[0][1]) 
            
           l_of_ports =[]
           
           l_exha= pi[1] # p[1] is list of exahusted containers          
           for exhcont in l_exha:
              l_of_ports.append(exhcont[3])  # This index dependent solution is not
                                             # flexible. The list should be dictionaries.
           l_vigo= pi[2] # p[2] is list of exahusted containers          
           for vigocont in l_vigo:
              l_of_ports.append(vigocont[3])
          
           if (int(pi[0][1]) <= cpuUsageThreshold): 
              PiID_cpuUsage= (pi[0][0], pi[0][1]) 
              tu= (PiID_cpuUsage, l_of_ports)
           l_of_Pis_and_ports.append(tu)
       return (l_of_Pis_and_ports) 


   """
   Expects a cpuUsageThreshold that determine exhaustion of cpuUsage
   Returns a list of all Pis with 
    - cpuUsage
    - ports assigned to containers 
   The format of the returnes list:
   [((PiID, cpuUsage), [port_host, port_host, port_host, ....]),
    ((PiID, cpuUsage), [port_host, port_host, port_host, ....]),
    ...
   ]
   Where cpuUsage associated to PiID is equal or less that cpuUsageThreshold
   and the cpuUsage of the containers (not include in the list) running in the 
   Pi is less or equal cpuUsageThreshold
   """
   def get_allVigorousPis_and_ports(self, cpuUsageThreshold):
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
       l_of_tu= self.__get_allPis_with_cpuUsage_of_exhausted_and_vigorous_containers(l_dict, cpuUsageThreshold) 
       l_of_Pis_and_ports =[]
       for pi in l_of_tu:
         if (int(pi[0][1]) <= cpuUsageThreshold):
           PiID_cpuUsage= (pi[0][0], pi[0][1]) 
            
           l_of_ports =[]
           
           l_exha= pi[1] # p[1] is list of exahusted containers          
                                            
           if (len(l_exha) ==0):
             l_vigo= pi[2] # p[2] is list of exahusted containers          
             for vigocont in l_vigo:
                l_of_ports.append(vigocont[3]) # This index dependent solution is not
             if (int(pi[0][1]) <= cpuUsageThreshold): # flexible. The list should be dictionaries. 
                PiID_cpuUsage= (pi[0][0], pi[0][1]) 
                tu= (PiID_cpuUsage, l_of_ports)
             l_of_Pis_and_ports.append(tu)
       return (l_of_Pis_and_ports) 



   """
   Returns a list of tuples:
   [((PiId, cpuUsage), [(containerId, cpuUsage, image, port_host), (containerId, cpuUsage, image, port_host), ...]),  
    ((PiId, cpuUsage), [(containerId, cpuUsage, image, port_host), (containerId, cpuUsage, image, port_host), ...]),
    ((PiId, cpuUsage), [(containerId, cpuUsage, image, port_host), (containerId, cpuUsage, image, port_host), ...]),
    ]                  # This index dependent solution is not flexible. A a list of dictionaries should be used!!! 
   Each tuple of the returned list correspond to a Pi with at least a single
   container with exhausted cpuUsage (cpuUsage > cpuUsageThreshold).
   For example, for the fist line:
   (PiId, cpuUsage): The id of the Pi and its cpuUsage which is not necessarily exhausted.
   [(containerId,cpuUsage), (containerId,cpuUsage), ...]: the list of exhausted containers
     in the Pi and the cpuUsage (which is  > cpuUsageThreshold) of the container.   
   Delete!!! doesnt work 28 Feb 2017
   """ 
   def get_delete_allPis_with_cpuUsageExhaustedContainers(self,cpuUsageThreshold):
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
       l_of_Pis_with_exhaustedConta=[]
       for d in l_dict:
         lst_of_t= piresources.get_cpuUsageExhaustedContainers_of_Pi(d,cpuUsageThreshold)
         if (len(lst_of_t) > 0):
            l_of_Pis_with_exhaustedConta.append( ((d['PiID'], d['resourceUsage']['cpuUsage']), lst_of_t) )
       return (l_of_Pis_with_exhaustedConta)
      



 
   """
   Return a list of tuples. Each tuple corresponds to the resources
   consumed by a container running in a given Pi.
   The dictionaries of each Pi are stored in a list.
   l_dict[0] corresponds to the first Pi in the list, l_dict[1] corresponds
   to the second Pi, etc. In this example, which I'm using for testing,
   I'm manually selecting the Pi: l_dict[0]
   """ 
   def get_allContainersRU_of_one_Pi(self):
       l_jsonfiles= self.__get_lst_of_jsonfiles()
       l_dict= self.__jsonfiles_to__dict(l_jsonfiles)
       lst_of_tuples= piresources.get_allResources_of_allContainers_of_Pi(l_dict[2])
       return(lst_of_tuples[0])



   """
   Migration functions

   [((PiID, cpuUsage), [containerId, cpuUsage, image, port_host]),
    ((PiID, cpuUsage), [containerId, cpuUsage, image, port_host]),
    ...
   ]
   The cpuUsage associated to PiID can be vigorous (less or equal than cpuUsageThreshold or 
   exhusted (cpuUsage > cpuUsageThreshold)
   def get_allPis_with_cpuUsageExhausted_containers(self, cpuUsageThreshold): 
       l_jsonfiles= self.__get_lst_of_jsonfiles()
   """
   def replicate_cpuUsageExhaustedContainers(self, cpuUsageThreshold, migrRec= migration_rec_default):
    lst= self.get_allPis_with_cpuUsageExhausted_containers(cpuUsageThreshold) 

    l_of_pis_and_ports= self.get_pis_cpuUsage_and_porthosts()
    lst_of_vigorous= self.get_allVigorousPis_and_ports(cpuUsageThreshold)
    for tu in lst_of_vigorous:
        print("^^^^^PiId= " + tu[0][0] + " cpuUsage= " + tu[0][1])
        for portN in tu[1]:
          print ("^^^^^^port_host " + portN)
    print("................................................................\n\n")    
  
    migr_l_lo=[]  # list with containers to be migrated locally
    migr_l_re=[]  # list with containers to be migrated remotely

    for j in range(0, len(lst)):
        tuple= lst[j]
        PiIDcpuUsage= tuple[0]
        PiID=PiIDcpuUsage[0]
        cpuUsage=PiIDcpuUsage[1]
        l=            tuple[1]
        
        if (int(cpuUsage) <= cpuUsageThreshold):
           lts_of_porthosts= self.__get_porthosts_of_pi(PiID)
          
           for k in range(0, len(l)):
               container_tu= l[k]
               freeport= portnumbers.get_free_port(lts_of_porthosts, Low_Bound, Upper_Bound)
               lts_of_porthosts.append(freeport)
               """         2 Mar 2017: I (Carlos) couldnt make this approach work
               mr['PiID']= PiID               It seems to be a bug in the mr or the
               mr['PiIP']= '192.to.be.fixed'  Python compiler. The list woudl store
               mr['image']= container_tu[2]   the same mr in migr_l_lo[0] and migr_lst[1]
               mr['port']=  str(freeport)a    I abandoned the approach and included the
               mr['containerID']= 'some'      record manually.
               migr_l_lo.append(mr)
               """
               migr_l_lo.append({'PiID':        PiID,            'PiIP':  '192.168.to.fix', 
                                'image':       container_tu[2], 'port':  str(freeport),
                                'containerID': 'nothing'})

        else:
          for k in range(0, len(l)):
              container_tu= l[k]
              myPiID= lst_of_vigorous[0][0][0]  # first vigorous in the list 
              print(" ++++++++++++++++++++++++++++++myPiID vigorous" + myPiID)
              lst_of_porthosts= self.__get_porthosts_of_pi(myPiID)
              freeport= portnumbers.get_free_port(lts_of_porthosts, Low_Bound, Upper_Bound)
              lts_of_porthosts.append(freeport)
              
              migr_l_re.append({'PiID':         myPiID,          'PiIP': '192.168.to.fix', 
                             'image':       container_tu[2], 'port':  str(freeport),
                             'containerID': 'nothing'})
   
    if (len(migr_l_lo)==0 and len(migr_l_re)==0):
       print("Nothing to replicate")
    else:
       print("Some replication is needed!")
         

    for m in range(0, len(migr_l_lo)):
        fn= migrFolderPath +  "migrationTo_" + migr_l_lo[m]['PiID'] +  "_mgrRecSamePi" + str(m) + ".json" 
        piresources.create_jsonFile(migr_l_lo[m], fn)

    for n in range(0, len(migr_l_re)):
        fn= migrFolderPath +  "migrationTo_" + migr_l_re[n]['PiID'] +  "_mgrRecAnotherPi" + str(n) + ".json" 
        piresources.create_jsonFile(migr_l_re[n], fn)

    return (migr_l_lo, migr_l_re)


   """
   The cpuUsage associated to PiID can be vigorous (less or equal than cpuUsageThreshold or 
   exhusted (cpuUsage > cpuUsageThreshold)
   def get_allPis_with_cpuUsageExhausted_containers(self, cpuUsageThreshold): 
       l_jsonfiles= self.__get_lst_of_jsonfiles()
   """
   def delete_replicate_cpuUsageExhaustedContainersInAnotherPi(self, cpuUsageThreshold, migrRec= migration_rec_default):
    lst= self.get_allPis_with_cpuUsageExhausted_containers(cpuUsageThreshold) 

    pis_and_ports= self.get_pis_and_porthosts() 

    migr_l_lo=[]


    for j in range(0, len(lst)):
        tuple= lst[j]
        PiIDcpuUsage= tuple[0]
        PiID=PiIDcpuUsage[0]
        cpuUsage=PiIDcpuUsage[1]
        l=            tuple[1]
        
        if (int(cpuUsage) <= cpuUsageThreshold):
           lts_of_porthosts= self.__get_porthosts_of_pi(PiID)
          
           for k in range(0, len(l)):
               container_tu= l[k]
               freeport= portnumbers.get_free_port(lts_of_porthosts, Low_Bound, Upper_Bound)
               lts_of_porthosts.append(freeport)
               """         2 Mar 2017: I (Carlos) couldnt make this approach work
               mr['PiID']= PiID               It seems to be a bug in the mr or the
               mr['PiIP']= '192.to.be.fixed'  Python compiler. The list woudl store
               mr['image']= container_tu[2]   the same mr in migr_l_lo[0] and migr_lst[1]
               mr['port']=  str(freeport)a    I abandoned the approach and included the
               mr['containerID']= 'some'      record manually.
               migr_l_lo.append(mr)
               """
               migr_l_lo.append({'PiID':        PiID,            'PiIP':  '192.168.to.fix', 
                                'image':       container_tu[2], 'port':  str(freeport),
                                'containerID': 'sometobe'})
        else:
          pass            


    for m in range(0, len(migr_l_lo)):
        fn= migrFolderPath +  "migrationTo" + migr_l_lo[m]['PiID'] +  "mgrRec" + str(m) + ".json" 
        piresources.create_jsonFile(migr_l_lo[m], fn)

    return (migr_l_lo)




   """
   Return a 
   """ 
   def trigger_migration(self,migrationFolder):
       return (True)
 
   """
   Return a 
   """ 
   def get_migration_lst(self): 
       return[('192.0.0.1', 'hypriot/rpi-busybox-httpd:latest', '8001', 'some', 'SEG1'),
              ('192.0.0.2', 'hypriot/rpi-busybox-httpd:latest', '8002', 'some', 'SEG2'),
              ('192.0.0.3', 'hypriot/rpi-busybox-httpd:latest', '8003', 'some', 'SEG3')]
   
   """
   migration_rec_default= {
    'PiID':        'SEG_1',
    'PiIP':        '192.0.0.1',
    'image':       'hypriot/rpi-busybox-httpd:latest',
    'port':        '8001',
    'containerID': 'some'
    }
   """

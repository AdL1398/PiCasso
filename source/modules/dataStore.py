"""
title           : dataStore.py
description     : a dictionary contain information of Data content
source          :
author          : Adisorn Lertsinsrubtavee
date            : 23 May 2017
version         : 1.0
contributors    :
usage           :
notes           :
compile and run : It is a python module imported by a main python programme.
python_version  : Python 2.7.12
====================================================
"""

import json
import  os.path

class DataStore(object):

    def __init__(self):
        self.table = {
                            '/ndn/test1': {'Type': 'text', 'Content': 'Producer-Data1'},
                            '/ndn/test2': {'Type': 'text', 'Content': 'Producer-Data2'},
                            '/ndn/test3': {'Type': 'file', 'Content': '/home/test.img'},
                            '/ndn/monitoring': {'Type': 'function', 'Content': 'getPi()'},
                  }

        self.fname = "DataStore.json"
        self.path = "./DS/"

    def putDataStore (self, name, type, content):
        print "Register content name: %s" %name
        newData = {name: {'Type': type, 'Content': content}}
        self.table.update(newData)

    def getDataStore_Content (self, name):
        print "Request content name: %s" %name
        return self.table[name]['Content']

    def getDataStore_Type (self, name):
        print "Request content name: %s" %name
        return self.table[name]['Type']

    def creaDataStore_json(self, DS):
        print DS
        ds_filename = os.path.join(self.path, self.fname)
        try:
            os.remove(ds_filename)
        except OSError:
            pass
        with open(ds_filename, 'w') as json_outfile:
            json.dump(DS, json_outfile, ensure_ascii=False)
        return

    def readDataStore_json(self):
        json_data = self.path + self.fname
        with open(json_data) as json_infile:
            ds_loaded = json.load(json_infile)
        return ds_loaded

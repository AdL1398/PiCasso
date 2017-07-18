"""
title           : serviceRepo_main.py
description     : This class creates a ftp server for the service producers to upload their service image and service descriptor
source          :
author          : Adisorn Lertsinsrubtavee
date            : 18 July 2017
version         : 1.0
contributors    :
usage           :
notes           :
compile and run : It is a python module imported by a main python programme.
python_version  : Python 2.7.12
====================================================
"""

import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

class Service_Repo_Main(object):
    def __init__(self, port):
        self.port = port
        script_path = os.path.abspath(__file__)  # i.e. /path/to/dir/foobar.py
        script_dir = os.path.split(script_path)[0]  # i.e. /path/to/dir/
        folder = 'SC_repository/'
        repo_path = os.path.join(script_dir, folder)

        if not os.path.exists(repo_path):
            os.makedirs(repo_path)

    def run(self):


        # Instantiate a dummy authorizer for managing 'virtual' users
        authorizer = DummyAuthorizer()

        # Define a new user having full r/w permissions and a read-only
        # anonymous user
        authorizer.add_user('user', '12345', '.', perm='elradfmwM')
        authorizer.add_anonymous(os.getcwd())

        # Instantiate FTP handler class
        handler = FTPHandler
        handler.authorizer = authorizer

        # Define a customized banpyftpdlibner (string returned when client connects)
        handler.banner = "pyftpdlib based ftpd ready."

        # Specify a masquerade address and the range of ports to use for
        # passive connections.  Decomment in case you're behind a NAT.
        # handler.masquerade_address = '151.25.42.11'
        # handler.passive_ports = range(60000, 65535)

        # Instantiate FTP server class and listen on 0.0.0.0:2121
        address = ('', self.port)
        server = FTPServer(address, handler)

        # set a limit for connections
        server.max_cons = 256
        server.max_cons_per_ip = 5

        # start ftp server
        server.serve_forever()


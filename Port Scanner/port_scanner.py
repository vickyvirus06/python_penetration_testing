#!/usr/bin/python3

import sys
import socket
from datetime import datetime

if len(sys.argv) == 2:
    target = socket.gethostbyname(sys.argv[1])  # get first argument
    print("-" * 50)
    print("Scanning started on " + target)
    print("Started at " + str(datetime.now()))
    print("-" * 50)

    try:
        for port in range(1, 85):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # Set a timeout for the connection attempt
            # connect_ex will return 0 if port is open or 1
            connection_establish = sock.connect_ex((target, port))
            if connection_establish == 0:
                print(f"{target} has port open on {port}")
            sock.close()  # Close the socket after use

    except KeyboardInterrupt:
        print("\nExiting scanning")
        sys.exit()
    except socket.gaierror:
        print("\nHost name not found. Please check.")
        sys.exit()
    except socket.error:
        print("\nCannot establish connection to scan.")
        sys.exit()

else:
    print("\nInvalid Host name")
    print("\nSyntax: python3 port_scanner.py <ip>")
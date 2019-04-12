#!/usr/bin/env python3

# TODO : function set_selec(nb,delta) that does the modulo shit or random if required
# for increments and init sets

import os
import sys
import socket
import argparse

def send(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_IP, TCP_PORT))
    sock.send(msg.encode())
    data = sock.recv(BUFFER_SIZE)
    sock.close()

BUFFER_SIZE = 256

parser=argparse.ArgumentParser(description='arg parsing')
parser.add_argument("-d", "--delta",help="list of indexes to be added to the current indexes of the selection")
parser.add_argument("-p", "--port",default=5005,type=int,help="port of sel server")
parser.add_argument("-a", "--address",default="127.0.0.1",help="address of the sel server")

args = parser.parse_args(sys.argv[1:])
TCP_PORT = args.port
TCP_IP = args.address

#print(args)
send(args.delta) 

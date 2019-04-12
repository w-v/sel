#!/usr/bin/env python3

# TODO : function set_selec(nb,delta) that does the modulo shit or random if required
# for increments and init sets

import sched
import logging
import argparse
import time
import os
import sys
import random
import json
from pathlib import Path
import signal
import socket
import threading

#PATH='~/.config/fehbg/config.json'

#signal.setitimer(signal.ITIMER_PROF, 1, 1.0)
#signal.signal(signal.SIGPROF,change_bg)
LOGFILE = 'log'
logging.basicConfig(format='%(asctime)s %(message)s',filename=LOGFILE,level=logging.DEBUG)

def depth(L):
    if not L or not isinstance(L, list):
        return 0
    else:
        return max(map(depth, L))+1

def getSelec(L, s):
    logging.debug("selecting "+str(s))
    if L and isinstance(L, list) and s:
        return getSelec(L[s[0]], s[1:])
    else:
       return L 

def getDim(L, s):
    if L and isinstance(L, list) and s:
        return getDim(L[s[0]], s[1:])
    else:
       return len(L) 
    
def getListIndex(i):
    # get the index of the list at depth i (0 lowest depth)
    index=selec[:i]
    return index

def setselec(i, n):
    if randomize[i]:
        a = random.randrange(dims[i])
    else:
        a = (n)%dims[i]
    logging.info("setting "+str(i)+" to "+str(a)+" : "+str(selec))
    selec[i] = a


def renew(i, delta=1):
    if i == d-1:
        item = getSelec(array,selec)
        logging.info("item : "+str(item))
        os.system(command+item)
        logging.info("command done")

    if times[i] != 0 and delta != 0:
        setselec(i,selec[i]+delta)
    #if cycle[i] and ( selec[i]+delta > dims[i] or selec[i]+delta < 0):
    #    selec[i] = 0
    # cycle means you renew i-1

    logging.info(str(i)+" renewed "+str(selec)+" dim:"+str(dims[i]))

    if i < d-1:
        dims[i+1]=getDim(array, getListIndex(i+1))
        setselec(i+1,0) 
        
        if times[i+1] != 0:
            s.cancel(events[i+1])
        renew(i+1,1)
    if times[i] != 0:
        events[i] = s.enter(times[i],0,renew,argument=(i,))

def add(sel,delta):
    logging.info("adding "+str(delta)+" to "+str(sel))
    if len(sel) != len(delta):
        logging.critical("dimensions of selec and delta don't match "+str(len(sel))+" != "+str(len(delta)))
    else:
        for i in range(d):
            if delta[i] != 0:
               setselec(i, sel[i]+delta[i])
        for i in range(d):
            if delta[i] != 0:
                dims[i]=getDim(array, getListIndex(i))
                s.cancel(events[i])
                renew(i, 0)
                break


BUFFER_SIZE = 256

def send(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_IP, TCP_PORT))
    sock.send(msg.encode())
    data = sock.recv(BUFFER_SIZE)
    sock.close()
    
def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((TCP_IP, TCP_PORT))
    sock.listen(1)

    while 1:
        conn, addr = sock.accept()
        logging.info('Connection address:'+str(addr))
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        logging.info("received data:"+str(data))
        handle_client(data.decode())
        #conn.send(data)  # echo
        conn.close()

def handle_client(buff):
   logging.debug(buff)
   delta=json.loads(buff)
   add(selec,delta)

def read_args(args,d):
    parser=argparse.ArgumentParser(description='arg parsing')
    parser.add_argument("-s", "--selection",default=json.dumps([0]*d),help="list of indexes of the item to be selected in the array given in sdtin")
    parser.add_argument("-r", "--randomize",default=json.dumps([False]*d),help="list of booleans coding wether each dimension should be chosen randomly")
    parser.add_argument("-t", "--time",default=json.dumps([0]*d),help="list of time intervals in seconds after wich the corresponding dimension will be updated, 0 means there is no timer on that dimension")
    parser.add_argument("-c", "--cycle",default=json.dumps([False]*d),help="list of booleans coding wether a dimension is to be cycled through or should cause the next dimension to update when it reaches the end of its indexes")
    parser.add_argument("-p", "--port",default=5005,type=int,help="port of sel server")
    parser.add_argument("-a", "--address",default="127.0.0.1",help="address of the sel server")

    return parser.parse_args(sys.argv[1:])

# read stdin
array=json.loads(sys.stdin.read())
d=depth(array)

# read args
args = read_args(sys.argv[1:],d)
logging.debug(args)
TCP_IP = args.address
TCP_PORT = args.port
selec=json.loads(args.selection)#list(map(lambda x : int(x), args.selection))
dims=[]
times=json.loads(args.time)#list(map(lambda x : int(x), args.time))
randomize=json.loads(args.randomize)
cycle=json.loads(args.cycle)
s=0
#command="feh --bg-fill --no-fehbg --no-xinerama "
command="echo "
events=[]


if d != len(selec):
    logging.critical("dimensions of default "+str(selec)+" and json dont match "+str(d)+" != "+str(len(selec)))

server = threading.Thread(None, server, None)
server.start()

for i in range(d):
    dims.append(getDim(array, getListIndex(i)))
    if randomize[i]:
        selec[i] = random.randrange(dims[i])

s = sched.scheduler(time.time, time.sleep)
for i in range(d):
    if times[i] != 0:
        events.append(s.enter(times[i],0,renew,argument=(i,)))
    else:
        # so that indexes are preserved
        events.append(0)

s.run()
#print(getSelec(array,[1,0,1,0]))
#print(getDim(array,[0,0,0]))


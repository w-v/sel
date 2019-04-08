#!/usr/bin/env python3

# TODO : function set_selec(nb,delta) that does the modulo shit or random if required
# for increments and init sets

import sched
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
CONF_PATH='fehbg.json'
selec=[0,0,0]
dims=[]
times=[6000,600,10]
randomize=[False,True,True]
cycle=[False,False,True]
s=0
d=0
command="feh --bg-fill --no-fehbg --no-xinerama "
events=[]

def read_conf(path): 
    f = open(path, 'r')
    return json.loads(f.read())

def load_path(path):
    if os.path.exists(path):
        sets=subdirs(path)
  
def main(): 
    conf = read_conf(CONF_PATH)
    print(conf["supersets"])
    selec=conf["default"]["cat"]
    dir=conf["default"]["dir"]
    superset=conf["supersets"][cat]["dirs"][dir]
    load_path(superset)
    print(sets)

#signal.setitimer(signal.ITIMER_PROF, 1, 1.0)
#signal.signal(signal.SIGPROF,change_bg)

#!/usr/bin/env python




def depth(L):
    print(L)
    if not L or not isinstance(L, list):
        return 0
    else:
        return max(map(depth, L))+1

def getSelec(L, s):
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
        return random.randrange(dims[i])
    else:
        return (n)%dims[i]


def renew(i, delta=1):
    if i == d-1:
        item = getSelec(array,selec)
        print("item : "+str(item))
        os.system(command+item)
        print("command done")

    if times[i] != 0 and delta != 0:
        selec[i] = setselec(i,selec[i]+delta)
    #if cycle[i] and ( selec[i]+delta > dims[i] or selec[i]+delta < 0):
    #    selec[i] = 0
    # cycle means you renew i-1

    print(str(i)+" renewed "+str(selec)+" dim:"+str(dims[i]))

    if i < d-1:
        setselec(i+1,0) 
        dims[i+1]=getDim(array, getListIndex(i+1))
        if times[i+1] != 0:
            s.cancel(events[i+1])
        renew(i+1)
    if times[i] != 0:
        events[i] = s.enter(times[i],0,renew,argument=(i,))

def add(sel,delta):
    if len(sel) != len(delta):
        print("dimensions of selec and delta don't match "+str(len(sel))+" != "+str(len(delta)))
    else:
        for i in range(d):
            if delta[i] != 0:
                selec[i] = setselec(i, sel[i]+delta[i])
        for i in range(d):
            if delta[i] != 0:
                dims[i]=getDim(array, getListIndex(i))
                s.cancel(events[i])
                renew(i, 0)
                break


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 256

def send(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_IP, TCP_PORT))
    sock.send(msg.encode())
    data = sock.recv(BUFFER_SIZE)
    sock.close()
    
def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((TCP_IP, TCP_PORT))
    sock.listen(1)

    while 1:
        conn, addr = sock.accept()
        print('Connection address:', addr)
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        print("received data:", data)
        handle_client(data.decode())
        #conn.send(data)  # echo
        conn.close()

def handle_client(buff):
   data = buff.split(" ")
   print(data)
   if len(data) > 1 and data[0] == "-d":
       delta=json.loads(data[1])
       add(selec,delta)


if len(sys.argv) > 1 and sys.argv[1] == "-s":
    send(" ".join(sys.argv[2:]))
    sys.exit(0)

a=sys.stdin.read()
array=json.loads(a)
d=depth(array)
if d != len(selec):
    print("dimensions of default "+str(selec)+" and json dont match "+str(d)+" != "+str(len(selec)))

server = threading.Thread(None, server, None)
server.start()

for i in range(d):
    dims.append(getDim(array, getListIndex(i)))
    if randomize[i]:
        selec[i] = random.randrange(dims[i])

item = getSelec(array,selec)
os.system(command+item)

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
print(array)
print('done')


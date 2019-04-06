#!/usr/bin/env python3

import sched
import time
import os
import sys
import json
from pathlib import Path
import signal

#PATH='~/.config/fehbg/config.json'
CONF_PATH='fehbg.json'
selec=[0,0,0,0]
dims=[]
times=[60,20,5,1]
s=0
d=0
events=[]

def read_conf(path): 
    f = open(path, 'r')
    return json.loads(f.read())

def load_path(path):
    if os.path.exists(path):
        sets=subdirs(path)

def subdirs(path):
    p = Path(path)
    return [x for x in p.iterdir() if x.is_dir()]
  
def main(): 
    conf = read_conf(CONF_PATH)
    print(conf["supersets"])
    selec=conf["default"]["cat"]
    dir=conf["default"]["dir"]
    superset=conf["supersets"][cat]["dirs"][dir]
    load_path(superset)
    print(sets)

def change_bg():
  os.system("fehbg --bg-fill --randomize "+str(sets[set]))

def p(a,b):
    print('ok')

#signal.setitimer(signal.ITIMER_PROF, 1, 1.0)
#signal.signal(signal.SIGPROF,change_bg)


def depth(L):
    return L and isinstance(L, list) and max(map(depth, L))+1

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

def t(i):
    print(i)

def renew(i):
    print(str(i)+" renewed "+str(selec)+" dim:"+str(dims[i]))
    selec[i]=(1+selec[i])%dims[i]
    if i == d-1:
        item = getSelec(array,selec)
        print("item : "+str(item))
    else:
        dims[i+1]=getDim(array, getListIndex(i+1))
    events[i] = s.enter(times[i],0,renew,argument=(i,))

a=sys.stdin.read()
array=json.loads(a)
d=depth(array)
if d != len(selec):
    print("dimensions of default "+str(selec)+" and json dont match "+str(d)+" != "+str(len(selec)))

s = sched.scheduler(time.time, time.sleep)


for i in range(d):
    dims.append(getDim(array, getListIndex(i)))
    if times[i] != 0:
        events.append(s.enter(times[i],0,renew,argument=(i,)))

s.run()
#print(getSelec(array,[1,0,1,0]))
#print(getDim(array,[0,0,0]))
print(array)
print('done')


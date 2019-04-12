#!/usr/bin/env python3

import subprocess
import sys
import json
from functools import reduce

def is_not_empty(arr):
    return (isinstance(arr, bool) and arr) or arr["type"] == "file" or(arr["type"] == "directory" and "contents" in arr and arr["contents"] and reduce(lambda a,b : is_not_empty(a) and is_not_empty(b), arr["contents"]))

def cleanup(json):
    return list(map(remove_meta, json))

def remove_meta(e):
    if e["type"] == "directory" :
        return cleanup(e["contents"]) 
    else:
        return e["name"]


path=sys.argv[1]
# add an option for depth
out = subprocess.Popen(['tree', '-J', "--noreport","-L", "2","-f", path],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
st,str=out.communicate()
b = st.decode()
o=json.loads(b)
a=cleanup(o)
print(json.dumps(a))

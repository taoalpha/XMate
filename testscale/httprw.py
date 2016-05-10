#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, random
import moment
import multiprocessing
from httpinit import generateUser

para_list = []
for i in range(0,1000):
    para_list.append(generateUser(i))
post_url = "http://192.168.99.100:4000/user/"
numprocess = 100

def sendrwrequest():

    st = moment.now().epoch()

    for i in range(0,100):
        j =  random.randint(0,999)
        action = ["read", "write"][(random.random() > 0.86)]
        if(action == "read"):
            r = requests.get(post_url+para_list[j]["_id"])
        else:
            #r = requests.put(post_url+para_list[i]["_id"],para_list[i])
            r = requests.put(post_url+para_list[j]["_id"],para_list[j])
            #print r.text
            #print r.status_code
        if(r.status_code != 200 or "status" in r.json()):
            print i
            print "read write failed"
            break 
   
    runt = moment.now().epoch() - st
    print runt



plist = []

for i in range (0,numprocess):
    p = multiprocessing.Process(target = sendrwrequest)
    plist.append(p)

for i in range (0,numprocess):   
    plist[i].start()








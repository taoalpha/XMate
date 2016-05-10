#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, random
import moment
import multiprocessing

id_list = []
for i in range(0,1000):
    id_list.append(str(i)+"tao")

post_url = "http://192.168.99.100:4000/user/"
numprocess = 100

# r = requests.get(post_url+"10000tao")
# print r.text

def sendreadrequest():

    st = moment.now().epoch()
    for i in range(0,100):
        j = random.randint(0,999)
        #r = requests.put(post_url+para_list[i]["_id"],para_list[i])
        r = requests.get(post_url+id_list[j])
        #print r.text
        #print r.status_code
        if(r.status_code != 200 or "status" in r.json()):
            print i
            print "read failed"
            break 
    runt = moment.now().epoch() - st
    print runt

##########################################################
plist = []
for i in range (0,numprocess):
    p = multiprocessing.Process(target = sendreadrequest)
    plist.append(p)

for i in range (0,numprocess):   
    plist[i].start()
# sendrequest()


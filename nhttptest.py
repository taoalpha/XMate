#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import moment

para_list = []
for i in range(0,1000):
    para = {"_id":str(i)+"tao","gender":"male"}
    para_list.append(para)
post_url = "http://192.168.99.100:3000/user/"


# r = requests.get(post_url+"10000tao")
# print r.text


st_time = moment.now().epoch()
for i in range(0,1000):
	r = requests.put(post_url+para_list[i]["_id"],para_list[i])
	#r = requests.get(post_url+para_list[i]["_id"])
	#print r.text
   	#print r.status_code
	if(r.status_code != 200 or "status" in r.json()):
	 	print i
	 	break

runt = moment.now().epoch() - st_time
print runt



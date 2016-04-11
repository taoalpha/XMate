import sys, random, time, moment
from datetime import datetime
from db import CDatabase
#from msgdelivery import sendJoin

mydb = CDatabase()
res = mydb.buildConnection()

res = mydb.selectCollection("xmateHistoryPost")
mydb.removeData({})
print list(mydb.getData({})["content"])

res = mydb.selectCollection("xmatePost")
mydb.removeData({})
print list(mydb.getData({})["content"])

res = mydb.selectCollection("xmateUser")
mydb.removeData({})
print list(mydb.getData({})["content"])

res = mydb.selectCollection("xmateMessage")
mydb.removeData({})
print list(mydb.getData({})["content"])

#print list(mydb.getData({})["content"])


#match_list = {"fbid":"3"}
#ndata = {"gender":"female", "age":28, "history_partner":[], "schedule_list":[],"history_events":[],"unprocessed_message":[],"fbid":"3"}
#res = mydb.updateData({},{"conflict_list":[]})
#print list(mydb.getData(match_list)["content"])[0]

#res = mydb.selectCollection("xmatePost")
#match_list = {"ssid":"8"}
#ndata = {"time_range":{"time_start":moment.now().subtract(hours=12).epoch(), "time_end": moment.now().subtract(hours=6).epoch()}, "type":"Fucking", "member":[], "related_member":[], "owner":"", "ssid":"8"}
#res = mydb.insertData(ndata)
#print list(mydb.getData(match_list)["content"])[0]


# for i in range(1,5):
#     for j in range(2,6):
#             print i, j


# res = mydb.selectCollection("xmatePost")
# res = mydb.getData({"sid":0})
# cur = list(res["content"])
# pid =  cur[0]["_id"]


# res = sendJoin(uid, pid, mydb)
# if(res["status"]):
#      print res["msg"]
# print res["content"]
# def addn(l, a):
#     l.append(a)
# l = [1,2,3,4,5]
# addn(l, 6)
# print l





# res = mydb.selectCollection("xmateUser")
# res = mydb.getData({})
# cursor = res["content"]

# uid = 0
# cnt = 0
# nlist = set()

# for doc in cursor:
#     if(cnt == 2):
#         break
#     else:
#         cnt += 1
#         nlist.add(doc["_id"])
# nlist = list(nlist)

# match_list = {"_id": {"$in": nlist}}

# res = mydb.getData(match_list)
# cursor = res["content"]
# for doc in cursor:
#     if doc["_id"] == nlist[0]:
#         print doc, nlist[0]
#     else:
#         print doc
# ndata = {"gender":"female"}
# mydb.updateData({"_id":nlist[0]}, ndata)






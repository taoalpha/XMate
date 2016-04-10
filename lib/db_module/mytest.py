import sys, random, time, moment
from datetime import datetime
from db import CDatabase
#from msgdelivery import sendJoin

# mydb = CDatabase()
# res = mydb.buildConnection()

# res = mydb.selectCollection("xmateUser")
# match_list = {"uid":0}
# ndata = {"gender":"male", "age":25}
# res = mydb.updateData(match_list, ndata)

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






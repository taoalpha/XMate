import string, random, sys
from userModule import CUser

usercoll = CUser()
res = usercoll.buildConnection()
if(res['status']):
     print(res)

match_list = {}
res = usercoll.getData(match_list)
if(res['status']):
    print(res)
else:
    print(res['content'].count())
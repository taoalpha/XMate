import requests
import random
import time
import userdata as DG

postUrl = "http://192.168.99.100:1000"

def sendUser(profile):
    print "#user data#"
    print profile
    r = requests.post(postUrl+'/user/', data = profile)
    if ("status" in r.json() and r.json()["status"] != 1) :
        raise Exception('Fail', 'Send User')

def sendPost(profile):
    r = requests.post(postUrl+'/schedule/', data = profile)
    print r.json()
    if ("status" in r.json() and r.json()["status"] != 1) :
        raise Exception('Fail', 'Send Post')
    return r.json()

def sendMsg(profile):
    r = requests.post(postUrl+'/message/', data = profile)
    if ("status" in r.json() and r.json()["status"] != 1) :
        raise Exception('Fail', 'Send Msg')
    return r.json()

def getMsg(id):
    r = requests.get(postUrl+'/message/'+id)
    if ("status" in r.json() and r.json()["status"] != 1) :
        raise Exception('Fail', 'Get Msg')
    return r.json()

def getUser(id):
    r = requests.get(postUrl+'/user/'+id)
    if ("status" in r.json() and r.json()["status"] != 1) :
        raise Exception('Fail', 'Get User')
    return r.json()

def getPost(id):
    r = requests.get(postUrl+'/schedule/'+id)
    if ("status" in r.json() and r.json()["status"] != 1) :
        raise Exception('Fail', 'Get Post')
    return r.json()





def sendMsgPut(profile):
    r = requests.put(postUrl+'/message/', data = profile)
    if ("status" in r.json() and r.json()["status"] != 1) :
        raise Exception('Fail', 'Deal Msg')
    return r.json()



# create some users and store all the fbids

fbids = {}

userNum = 10
for i in range(userNum):
    userData = DG.generateUser()
    sendUser(userData)
    fbids[userData['_id']] = {}
    fbids[userData['_id']]["posts"] = []
    fbids[userData['_id']]["invite_msg"] = []
    fbids[userData['_id']]["join_msg"] = []


# use a id from the fbids to create a post and store all the pids from return reponse

pids = {}
postNum = 10
for i in range(postNum):
    uid = (fbids.keys())[int(random.random()*userNum)]
    post = DG.generatePost(uid)
    # send schedule profile request and get the id
    r = sendPost(post)
    pids[r["_id"]] = {}
    pids[r['_id']]["members"] = []
    # update fbdis._id.posts
    fbids[uid]["posts"].append(r["_id"])

# TODO: check correctness

# use a uid generate some invite messages

msgNum = 5
for i in range(msgNum):
    sid = (fbids.keys())[int(random.random()*userNum)]
    rid = (fbids.keys())[int(random.random()*userNum)]
    # post must be in sender's posts list
    userPostLen = len(fbids[sid]["posts"])
    if userPostLen > 0:
        pid = fbids[sid]["posts"][int(random.random()*userPostLen)]
        # generate msg
        rid = "10156733796340393"
        msg = DG.generateMsg(sid,rid,pid,"invite")
        # send msg request
        r = sendMsg(msg)
        # store msgid
        fbids[rid]["invite_msg"].append(r["_id"])

# use a uid generate some join messages
for i in range(msgNum):
    sid = (fbids.keys())[int(random.random()*userNum)]
    rid = (fbids.keys())[int(random.random()*userNum)]
    # join : post must be in receiver's posts list
    userPostLen = len(fbids[rid]["posts"])
    if userPostLen > 0:
        pid = fbids[rid]["posts"][int(random.random()*userPostLen)]
        # generate msg
        sid = "10156733796340393"
        msg = DG.generateMsg(sid,rid,pid,"join")
        # send msg request
        r = sendMsg(msg)
        # store msgid
        fbids[rid]["join_msg"].append(r["_id"])

print "##########"

for i in pids:
    post = getPost(i)
    if (set(post["member"]) != set(pids[i]["members"])):
        print i

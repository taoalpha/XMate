import requests
import random
import userdata as DG

postUrl = "http://192.168.99.100:2000"

def sendUser(profile):
    r = requests.post(postUrl+'/user/', data = profile)
    if ("status" in r.json() and r.json()["status"] != 1) :
        raise Exception('Fail', 'Send User')

def sendPost(profile):
    r = requests.post(postUrl+'/schedule/', data = profile)
    if ("status" in r.json() and r.json()["status"] != 1) :
        raise Exception('Fail', 'Send Post')
    return r.json()

def sendMsg(profile):
    r = requests.post(postUrl+'/message/', data = profile)
    if ("status" in r.json() and r.json()["status"] != 1) :
        raise Exception('Fail', 'Send Msg')
    return r.json()


# create some users and store all the fbids

fbids = {}

userNum = 10
for i in range(userNum):
    userData = DG.generateUser()
    sendUser(userData)
    fbids[userData['_id']] = {}
    fbids[userData['_id']]["posts"] = []
    fbids[userData['_id']]["msg"] = []


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
    pids[r['_id']]["msg"] = []
    # update fbdis._id.posts
    fbids[uid]["posts"].append(r["_id"])

# TODO: check correctness

# use a uid generate some invite messages

msgNum = 10
for i in range(msgNum):
    sid = (fbids.keys())[int(random.random()*userNum)]
    rid = (fbids.keys())[int(random.random()*userNum)]
    # post must be in sender's posts list
    userPostLen = len(fbids[sid]["posts"])
    if userPostLen > 0:
        pid = fbids[sid]["posts"][int(random.random()*userPostLen)]
        # generate msg
        msg = DG.generateMsg(sid,rid,pid,"invite")
        # send msg request
        r = sendMsg(msg)
        # store msgid
        fbids[rid]["msg"].append(r["_id"])
        pids[pid]["msg"].append(r["_id"])

# use a uid generate some join messages
for i in range(msgNum):
    sid = (fbids.keys())[int(random.random()*userNum)]
    rid = (fbids.keys())[int(random.random()*userNum)]
    # join : post must be in receiver's posts list
    userPostLen = len(fbids[rid]["posts"])
    if userPostLen > 0:
        pid = fbids[rid]["posts"][int(random.random()*userPostLen)]
        # generate msg
        msg = DG.generateMsg(sid,rid,pid,"join")
        # send msg request
        r = sendMsg(msg)
        # store msgid
        fbids[rid]["msg"].append(r["_id"])
        pids[pid]["msg"].append(r["_id"])


print fbids
print pids

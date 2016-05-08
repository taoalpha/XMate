import requests
import json

postUrl = "http://192.168.99.100:2000"

def getMsg():
    r = requests.get(postUrl+'/adminbackup_need_password/message')
    if ("status" in r.json() and r.json()["status"] != 1) :
        raise Exception('Fail', 'Get Msg')
    return r.json()

def getUser():
    r = requests.get(postUrl+'/adminbackup_need_password/user')
    if ("status" in r.json() and r.json()["status"] != 1) :
        raise Exception('Fail', 'Get User')
    return r.json()

def getPost():
    r = requests.get(postUrl+'/adminbackup_need_password/schedule')
    if ("status" in r.json() and r.json()["status"] != 1) :
        raise Exception('Fail', 'Get Post')
    return r.json()

def getCache():
    r = requests.get(postUrl+'/adminbackup_need_password/cache')
    if ("status" in r.json() and r.json()["status"] != 1) :
        raise Exception('Fail', 'Get Cache')
    return r.json()


dataset = {}
dataset["user"] = getUser()["content"]
dataset["schedule"] = getPost()["content"]
dataset["message"] = getMsg()["content"]
dataset["cache"] = getCache()["content"]

with open('data.json', 'w') as outfile:
    json.dump(dataset, outfile)

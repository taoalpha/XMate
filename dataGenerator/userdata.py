import random
import string
import moment

U_FIELD = {
    "_id" : "",
    "username" : "",
    "age" : "",
    "gender" : "",
    "preferred_gender" : "",
    "city": "",
    "credits" : "",
    "latitude" : "",
    "longitude" : "",
    "last_time_login" : "",
    "height" : "",
    "weight" : "",
    "schedule_list" : [],
    "conflict_list" : [],
    "history_partner" : [],
    "history_events" : [],
    "unprocessed_message" : []
}

def generateUser():
    '''
        generate user data
        user data fields:
        FIELDS = {
            "_id" : "",
            "username" : "",
            "age" : "",
            "gender" : "",
            "preferred_gender" : "",
            "city": "",
            "credits" : "",
            "latitude" : "",
            "longitude" : "",
            "last_time_login" : "",
            "height" : "",
            "weight" : "",
            "schedule_list" : [],
            "conflict_list" : [],
            "history_partner" : [],
            "history_events" : [],
            "unprocessed_message" : []
        }
    '''
    user = {}
    user["_id"] = ''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(8))
    user["username"] = random.choice(string.ascii_uppercase)+''.join(random.choice(string.ascii_lowercase) for _ in range(7)) +  " " + random.choice(string.ascii_uppercase)+''.join(random.choice(string.ascii_lowercase) for _ in range(7))
    user["age"] = ''.join(random.choice(string.digits) for _ in range(2))
    user["gender"] = ["male", "female"][(random.random() > 0.5)]
    user["preferred_gender"] = ["male", "female"][(random.random() > 0.5)]
    user["city"] = ''.join(random.choice(string.ascii_uppercase) for _ in range(2))
    user["latitude"] = float(''.join(random.choice(string.digits) for _ in range(5))) / 1000
    user["longitude"] = float(''.join(random.choice(string.digits) for _ in range(5))) / 1000
    user["height"] = int(''.join(random.choice(string.digits) for _ in range(3))) % 180
    user["weight"] = ''.join(random.choice(string.digits) for _ in range(2))
    user["credits"] = int(random.random()*100)
    # < 10 days to now
    user["last_time_login"] = moment.now().epoch() - int(random.random()*86400*10)
    for i in U_FIELD:
        if i not in user:
            user[i] = U_FIELD[i]
    return user


P_FIELD = {
    "type":"",
    "latitude":"",
    "longitude":"",
    "start_time":"",
    "end_time":"",
    "created_time":"",
    "owner":"",
    "creator":"",
    "member":[]
}

def generatePost(uid):
    '''
        Create a data for requesting to create a post
        @param {string} uid - the user id associated ith this post
    '''
    post = {}
    post["owner"] = uid
    post["creator"] = uid
    post["type"] = ["tennis","running","swimming","hiking","poker","movie","gym","game","concert","skating"][int(random.random()*10)]
    post["latitude"] = float(''.join(random.choice(string.digits) for _ in range(5))) / 1000
    post["longitude"] = float(''.join(random.choice(string.digits) for _ in range(5))) / 1000
    # < 10 days from now
    post["start_time"] = moment.now().epoch() - int(random.random()*86400*10)
    # < 3 hours from start_time
    post["end_time"] = post["start_time"] + int(random.random()*3*60*60)
    # < 2 days to now
    post["created_time"] = moment.now().epoch() - int(random.random()*86400*2)

    for i in P_FIELD:
        if i not in post:
            post[i] = P_FIELD[i]
    return post

def generateMsg(sid, rid, pid, type):
    '''
        Generate message
        @param {string} sid - sender_id
        @param {string} rid - receiver_id
        @param {string} pid - post_id
        @param {string} type - msg type
    '''
    msg = {}
    msg["sender_id"] = sid
    msg["receiver_id"] = rid
    msg["post_id"] = pid
    msg["type"] = type
    return msg

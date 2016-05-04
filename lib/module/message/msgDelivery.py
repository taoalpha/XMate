import sys, random, time, moment
from datetime import datetime
# from db import CDatabase


def returnHelper(status = 1, msg = None,content = None):
    return_val = {}
    return_val["status"] = status
    return_val["msg"] = msg
    return_val["content"] = content

    return return_val



def createMsg(mtype, send_id, receive_id, post_id, content, mydb, create_time = None):
    #create a new message and return its id
    msg = {}
    msg["type"] = mtype
    msg["post_id"] = post_id
    msg["sender_id"] = send_id
    msg["receiver_id"] = receive_id
    msg["content"] = content
    msg["create_time"] = moment.now().epoch()
    data_list = []
    data_list.append(msg)

    res = mydb.insertData("message", data_list)

    if(res["status"] != 1):
        return res

    return returnHelper(content = res["content"])



def insertMessage(uid, mid, mydb):
    #update the user's unprocessed message list
    id_list = []
    data_list = []
    id_list.append(uid)
    res = mydb.getData("user",id_list)
    if(res["status"] != 1):
        return res
    doc = res["content"][0]
    if(mid not in doc["unprocessed_message"]):
        doc["unprocessed_message"].append(mid)
        data_list.append(doc)
        res = mydb.updateData("user",id_list,data_list)
        if(res["status"] != 1):
            return res

    return returnHelper(content = {"_id":mid})


def leavecheck(uid,pid,mydb):

    #get the unprocessed message list from user
    id_list = []
    id_list.append(uid)
    res = mydb.getData("user",id_list)
    if(res["status"] != 1):
        return res
    doc = res["content"][0]
    msg_list = doc["unprocessed_message"]
    if(len(msg_list) == 0):
        return returnHelper()

    #check whether there are unprocessed message associated with the post
    id_list = msg_list
    res = mydb.getData("message",id_list)
    if(res["status"] != 1):
        return res
    cursor = res["content"]
    for doc in cursor:
        if(doc["post_id"] == pid and doc["type"] == "join"):
            return returnHelper(0, msg = "You should first processe the join request msgs associated with this post")

    return returnHelper()



def updateConflict(post_list, conflict_list, post_id, mydb):
    #get the new conflict list of a user
    if(post_id == None):
        if(len(post_list) < 2):
            return returnHelper(content = [])
        id_list = post_list
        res = mydb.getData("schedule",id_list)
        if(res["status"] != 1):
            return res
        cursor = res["content"]
        nconflict_list = set()
        for i in range(0,len(cursor)-1):
            for j in range(i+1,len(cursor)):
                minen = min(cursor[i]["end_time"],cursor[j]["end_time"])
                maxst = max(cursor[i]["start_time"],cursor[j]["start_time"])
                if(minen > maxst):
                    nconflict_list.add(cursor[i]["_id"])
                    nconflict_list.add(cursor[j]["_id"])

        nconflict_list = list(nconflict_list)
        return returnHelper(content = nconflict_list)

    else:
        if(len(post_list) == 0 or post_id in conflict_list):
            return returnHelper(content = conflict_list)

        id_list = post_list
        id_list.append(post_id)
        res = mydb.getData("schedule",id_list)
        if(res["status"] != 1):
            return res
        cursor = res["content"]
        flag = False
        st = 0
        en = 0

        for doc in cursor:
            if(doc["_id"] == post_id):
                st = doc["start_time"]
                en = doc["end_time"]
        for doc in cursor:
            if(doc["_id"] != post_id):
                minen = min(en, doc["end_time"])
                maxst = max(st, doc["start_time"])
                if(maxst < minen):
                    flag = True
                    if(doc["_id"] not in conflict_list):
                        conflict_list.append(doc["_id"])
        if(flag):
            conflict_list.append(post_id)
        nconflict_list = conflict_list

        return returnHelper(content = nconflict_list)


def sendJoin(uid, pid, mydb):
    #get the post owner's info
    id_list = []
    id_list.append(pid)
    res = mydb.getData("schedule",id_list)
    print "###get message from send join"
    print res
    if(res["status"] != 1):
        return res
    doc = res["content"][0]
    owner_id = doc["owner"]

    #create a msg
    id_list = []
    id_list.append(uid)
    res = mydb.getData("user",id_list)
    if(res["status"] != 1):
        return res
    user = res["content"][0]
    sender_name = user["username"]
    res = createMsg("join", uid, owner_id, pid,str(sender_name) + " want to join your post", mydb)
    if(res["status"] != 1):
        return res

    msg = res["content"][0]
    msg_id = msg["_id"]

    #update the info of receiver message list
    return insertMessage(owner_id, msg_id, mydb)


def sendInvitation(uid, pid, rid, mydb):
    #create message

    res = createMsg("invation", uid, rid, pid, "You are invited to the post", mydb)
    if(res["status"] != 1):
        return res

    msg = res["content"][0]
    msg_id = msg["_id"]

    return insertMessage(rid, msg_id, mydb)



def declineRequest(uid, mid, mydb):
    #get sender info from message
    id_list = []
    id_list.append(mid)
    res = mydb.getData("message",id_list)
    if(res["status"] != 1):
        return res
    msg = res["content"][0]

    rid = msg["sender_id"]
    msg_type = msg["type"]
    post_id = msg["post_id"]

    #generate message info by different type
    content = ""
    if(msg_type == "join"):
        content = "You are declined to join the post"
    else:
        id_list = []
        id_list.append(post_id)
        res = mydb.getData("schedule",id_list)
        if(res["status"] != 1):
            return res

        id_list = []
        id_list.append(uid)
        res = mydb.getData("user",id_list)
        if(res["status"] != 1):
            return res
        user = res["content"][0]
        content = "Your invitation to "+ user["username"] + " is declined"

    #Create plaintext message
    res = createMsg("plaintext", uid, rid, post_id, content, mydb)
    if(res["status"] != 1):
        return res
    msg_id = res["content"][0]

    #update the recevier's message list
    res = insertMessage(rid, msg_id, mydb)
    if(res["status"] != 1):
        return res

    return finishReadMsg(uid, mid, mydb)



def acceptRequest(uid, mid, mydb):
    #get sender, receiver and post info from message
    id_list = []
    id_list.append(mid)
    res = mydb.getData("message",id_list)
    if(res["status"] != 1):
        return res
    msg = res["content"][0]
    post_id = msg["post_id"]
    sid = msg["sender_id"]
    rid = msg["receiver_id"]
    msg_type = msg["type"]

    #add the user to the post member_list(update)
    id_list = []
    id_list.append(post_id)
    res = mydb.getData("schedule",id_list)
    if(res["status"] != 1):
        return res
    doc = res["content"][0]
    user_id = ""
    if(msg_type == "join"):
        user_id = sid
    else:
        user_id = rid
    if(user_id in doc["member"]):
        pass
    else:
        doc["member"].append(user_id)
        data_list = []
        data_list.append(doc)
        res = mydb.updateData("schedule",id_list,data_list)
        if(res["status"] != 1):
            return res

    #add the post to the user's post list
    id_list = []
    id_list.append(user_id)
    res = mydb.getData("user",id_list)
    if(res["status"] != 1):
        return res
    user = res["content"][0]
    if(post_id in user["schedule_list"]):
        pass
    else:
        res = updateConflict(user["schedule_list"], user["conflict_list"],post_id, mydb)
        if(res["status"] != 1):
            return res
        user["conflict_list"] = res["content"]
        user["schedule_list"].append(post_id)
        data_list = []
        data_list.append(user)
        res = mydb.updateData("user",id_list,data_list)
        if(res["status"] != 1):
            return res

    return finishReadMsg(uid, mid, mydb)


def leavePost(uid, pid, mydb):

    #get owner id from pid
    id_list = []
    id_list.append(pid)
    res = mydb.getData("schedule",id_list)
    if(res["status"] != 1):
        return res
    doc = res["content"][0]

    deletePost = False
    if(uid == doc["owner"]):
        res = leavecheck(uid,pid,mydb)
        if(res["status"] != 1):
            return res
        if(len(doc["member"]) > 0):
            new_owner = random.choice(doc["member"])
            doc["member"].remove(new_owner)
            doc["owner"] = new_owner
            data_list = []
            data_list.append(doc)
            res = mydb.updateData("schedule",id_list,data_list)
            if(res["status"] != 1):
                return res

            res = createMsg("plaintext", uid, new_owner, pid,"You become the owner of the Post",mydb)
            if(res["status"] != 1):
                return res
            msg_id = res["content"][0]
            res = insertMessage(new_owner, msg_id, mydb)
        else:
            deletePost = True
    else:
        if(uid in doc["member"]):
            doc["member"].remove(uid)
            data_list = []
            data_list.append(doc)
            res = mydb.updateData("schedule",id_list,data_list)
            if(res["status"] != 1):
                return res

            res = createMsg("plaintext", uid, doc["owner"], pid,"Someone leaves your post",mydb)
            if(res["status"] != 1):
                return res
            msg_id = res["content"][0]
            res = insertMessage(doc["owner"], msg_id, mydb)


    #delete post in the user's post list
    id_list = []
    id_list.append(uid)
    res = mydb.getData("user",id_list)
    if(res["status"] != 1):
        return res
    user = res["content"][0]
    if(pid in user["schedule_list"]):
        user["schedule_list"].remove(pid)

    res = updateConflict(user["schedule_list"], user["conflict_list"], None, mydb)
    if(res["status"] != 1):
        return res
    user["conflict_list"] = res["content"]
    data_list = []
    data_list.append(user)
    res = mydb.update("user",id_list,data_list)
    if(res["status"] != 1):
        return res

    if(deletePost):
        id_list = []
        id_list.append(pid)
        res = mydb.removeData("schedule",id_list)
        if(res["status"] != 1):
            return res

    return returnHelper()


######remind Tao to delete for plaintext
def finishReadMsg(uid, mid, mydb):

    #update the user unprocessed list by removing the message
    id_list = []
    data_list = []
    id_list.append(uid)
    res = mydb.getData("user",uid)
    if(res["status"] != 1):
        return res
    doc = res["content"][0]
    if(mid in doc["unprocessed_message"]):
        doc["unprocessed_message"].remove(mid)
        data_list.append(doc)
        res = mydb.updateData("user",id_list,data_list)
        if(res["status"] != 1):
            return res


    #remove the message from database
    id_list = []
    id_list.append(mid)
    res = mydb.removeData("message",id_list)
    if(res["status"] != 1):
        return res

    return returnHelper()



def checkMsg(mydb):

    #get all messages and check the out of time message
    id_list = []
    res = mydb.getData("message", id_list)
    if(res["status"] != 1):
        return res
    cursor = res["content"]

    outoftime_msg = []
    related_user = {}
    current_time = moment.now().epoch()
    st = current_time - 86400
    for msg in cursor:
        if(msg["create_time"] < st):
            outoftime_msg.append(doc["_id"])
            if(msg["receiver_id"] in related_user.keys()):
                pass
            else:
                related_user[msg["receiver_id"]] = []
            related_user[msg["receiver_id"]].append(msg["_id"])
    if(len(outoftime_msg) == 0):
        return returnHelper()

    #update users' unprocessed msg list by removing the out of date msgs
    id_list = related_user.keys()
    res = mydb.getData("user",id_list)
    if(res["status"] != 1):
        return res
    cursor = res["content"]

    id_list = []
    data_list = []
    for user in cursor:
        for msg_id in related_user[user["_id"]]:
            if(msg_id in user["unprocessed_message"]):
                user["unprocessed_message"].remove(msg_id)
        id_list.append(user["_id"])
        data_list.append(user)
    res = mydb.updateData("user",id_list, data_list)
    if(res["status"] != 1):
        return res


    #delete the out of time messages in database
    id_list = outoftime_msg
    res = mydb.removeData("message", id_list)
    if(res["status"] != 1):
        return res

    return returnHelper()




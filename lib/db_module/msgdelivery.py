import sys, random, time, moment
from datetime import datetime
from db import CDatabase



def returnHelper(status = 0, msg = None,content = None):
    return_val = {}
    return_val["status"] = status
    return_val["msg"] = msg
    return_val["content"] = content

    return return_val


def createMsg(mtype, send_id, receive_id, post_id, content, mydb, create_time = None):
    msg = {}
    msg["type"] = mtype
    msg["post_id"] = post_id
    msg["sender_id"] = send_id
    msg["receiver_id"] = receive_id
    msg["content"] = content
    msg["create_time"] = moment.now().epoch()
    msg_id = 0;

    res = mydb.selectCollection("xmateMessage")
    if(res["status"]):
        return res
    match_list = {"sender_id":send_id,"receiver_id":receive_id,"post_id":post_id}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor = list(res["content"])

    if(len(cursor) > 0):
        msg_id = cursor[0]["_id"]
        res = mydb.update(match_list,{"create_time":msg["create_time"]})
        if(res["status"]):
            return res
    else:
        res = mydb.insertData(msg)
        if(res["status"]):
            return res
        msg_id = res["content"].inserted_id
    
    return returnHelper(content = msg_id)




def insertMessage(uid, msg_id, mydb):
    
    res = mydb.selectCollection("xmateUser")
    if(res["status"]):
        return res
    match_list = {"_id": uid}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor = list(res["content"])

    msg_list = cursor[0]["unprocessed_message"]
    if(msg_id in msg_list):
        pass
    else:
        msg_list.append(msg_id)
        ndata = {"unprocessed_message":msg_list}
        res = mydb.updateData(match_list, ndata)
        if(res["status"]):
            return res
    
    return returnHelper(content = msg_id)




def sendJoin(uid, pid, mydb):

    #to get the post owner's info
    res = mydb.selectCollection("xmatePost")
    if(res["status"]):
        return res
    match_list = {"_id":pid}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor = list(res["content"])
    ############################################################
    if(len(cursor) == 0):
        return returnHelper(1, msg = "The post has been deleted")

    owner_id = cursor[0]["owner"]
    post_type = cursor[0]["type"]

    #create a msg and insert into database
    sender_name = ""
    res = mydb.selectCollection("xmateUser")
    if(res["status"]):
        return res
    match_list = {"_id": uid}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor = list(res["content"])
    sender_name = cursor[0]["username"]

    res = createMsg("join", uid, owner_id, pid, str(sender_name) + " want to join your " + str(post_type) + " activity", mydb)
    if(res["status"]):
        return res
    msg_id = res["content"]

    #update the info of receiver message list
    return insertMessage(owner_id, msg_id, mydb)



def sendInvation(uid, pid, rid, mydb):
    #create message
    res = createMsg("invation", uid, rid, pid, "You are invited to join the post",mydb)
    if(res["status"]):
        return res
    msg_id = res["content"]

    return insertMessage(rid, msg_id, mydb)
    


def declineRequest(uid, mid, mydb):
    #get sender info from user ID
    res = mydb.selectCollection("xmateMessage")
    if(res["status"]):
        return res
    match_list = {"_id":mid}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor = list(res["content"])
    msg_type = cursor[0]["type"]
    post_id = cursor[0]["post_id"]
    rid = cursor[0]["sender_id"]
    content = ""

    #Generate info by different type
    if(msg_type == 'join'):
        content = "You are declined to join post"
    else:
        res = mydb.selectCollection("xmatePost")
        if(res["status"]):
            return res
        match_list = {"_id":post_id}
        res = mydb.getData(match_list)
        if(res["status"]):
            return res
        cursor = list(res["content"])
        if(len(cursor) == 0):
            return finshReadMsg(uid, mid, mydb)
        else:
            res = mydb.selectCollection("xmateUser")
            if(res["status"]):
                return res
            match_list = {"_id":uid}
            res = mydb.getData(match_list)
            if(res["status"]):
                return res
            cursor = list(res["content"])
            content = "Your invitation to "+ str(cursor[0]["username"])+" is declined"

    #Create plaintext message
    res = createMsg("plaintext", uid, rid, post_id, content, mydb)
    if(res["status"]):
        return res
    msg_id = res["content"]

    #update the sender's message list
    res = insertMessage(rid, msg_id, mydb)
    if(res["status"]):
        return res

    return finshReadMsg(uid, mid, mydb)






def acceptRequest(uid, mid, mydb):
    #get sender, receiver and post info from message
    res = mydb.selectCollection("xmateMessage")
    if(res["status"]):
        return res
    match_list = {"_id":mid}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor = list(res["content"])

    msg_type = cursor[0]["type"]
    sid = cursor[0]["sender_id"]
    rid = cursor[0]["receiver_id"]
    post_id = cursor[0]["post_id"]


    #add the user to the post member_list
    res = mydb.selectCollection("xmatePost")
    if(res["status"]):
        return res
    match_list = {"_id":post_id}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor = list(res["content"])
    ##################################################################
    if(len(cursor) == 0):
        return returnHelper(1, msg = "The post has been deleted")
    
    userid = ""
    if(msg_type == "join"):
        userid = sid
    else:
        userid = rid

    mem_list = cursor[0]["member"]
    if(userid in mem_list):
        pass
    else:
        mem_list.append(userid)
        ndata = {"member":mem_list}
        res = mydb.updateData(match_list,ndata)
        if(res["status"]):
            return res

    #add the post to the user's post list
    res = mydb.selectCollection("xmateUser")
    if(res["status"]):
        return res
    match_list = {"_id":userid}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor = list(res["content"])

    post_list = cursor[0]["schedule_list"]
    conflict_list = cursor[0]["conflict_list"]
    if(post_id in post_list):
        pass
    else:
        res = checkConflict(post_list, post_id, conflict_list, mydb)
        if(res["status"]):
            return res
        post_list.append(post_id)
        
        res = mydb.selectCollection("xmateUser")
        if(res["status"]):
            return res
        ndata = {"schedule_list":post_list, "conflict_list":conflict_list}
        res = mydb.updateData(match_list, ndata)
        if(res["status"]):
            return res

    return finshReadMsg(uid, mid, mydb)



def leavePost(uid, pid, mydb):
    #get owner info
    res = mydb.selectCollection("xmatePost")
    if(res["status"]):
        return res
    match_list = {"_id":pid}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor = list(res["content"])
    owner_id = cursor[0]["owner"]
    mem_list = cursor[0]["member"]

    deletePost = False

    if(uid == owner_id):
        res = leavecheck(uid,pid,mydb)
        if(res["status"]):
            return res
        if(len(mem_list) > 0):
            new_owner_id = random.choice(mem_list)
            mem_list.remove(new_owner_id)
            res = mydb.selectCollection("xmatePost")
            if(res["status"]):
                return res
            match_list = {"_id":pid}
            ndata = {"owner":new_owner_id, "member":mem_list}
            res = mydb.updateData(match_list,ndata)
            if(res["status"]):
                return res

            res = mydb.selectCollection("xmateMessage")
            if(res["status"]):
                return res
            res = createMsg("plaintext",owner_id,new_owner_id,pid,"You become the owner of the Post",mydb)
            if(res["status"]):
                return res
            msg_id = res["content"]
            #update the sender's message list
            res = insertMessage(new_owner_id, msg_id, mydb)
            if(res["status"]):
                return res
        else:
            deletePost = True
    else:
        if(uid in mem_list):
            mem_list.remove(uid)
            ndata = {"member":mem_list}
            res = mydb.updateData(match_list,ndata)
            if(res["status"]):
                return res
    
    #delete post in the user's post list
    res = mydb.selectCollection("xmateUser")
    if(res["status"]):
        return res
    match_list = {"_id":uid}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor = list(res["content"])
    post_list = cursor[0]["schedule_list"]
    conflict_list = cursor[0]["conflict_list"]


    if(pid in post_list):
        post_list.remove(pid)
        ndata = {"schedule_list":post_list}
        res = mydb.updateData(match_list,ndata)
        if(res["status"]):
            return res

    res = updateConflict(post_list,mydb)
    if(res["status"]):
        return res
    nconflict_list = res["content"]
    if(pid in conflict_list):
        conflict_list.remove(pid)
    if(nconflict_list == conflict_list):
        pass
    else:
        res = mydb.selectCollection("xmateUser")
        if(res["status"]):
            return res
        match_list = {"_id":uid}
        ndata = {"conflict_list":nconflict_list}
        res = mydb.updateData(match_list,ndata)
        if(res["status"]):
            return res

    if(deletePost):
        res = mydb.selectCollection("xmatePost")
        if(res["status"]):
            return res
        match_list = {"_id": pid}
        res = db.removeData(match_list)
        if(res["status"]):
            return res

    return returnHelper()



def updateConflict(post_list, mydb):

    rlist = []
    res = mydb.selectCollection("xmatePost")
    if(res["status"]):
        return res
    match_list = {"_id": {"$in": post_list}}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor = list(res["content"])
    l = len(cursor)

    for i in range(0,l-1):
        for j in range(i+1,l):
            sti = cursor[i]["time_range"]["start_time"]
            eni = cursor[i]["time_range"]["end_time"]
            stj = cursor[j]["time_range"]["start_time"]
            enj = cursor[j]["time_range"]["end_time"]
            if(max(sti,stj) < min(sti,stj)):
                if(cursor[i]["_id"] in rlist):
                    pass
                else:
                    rlist.append(cursor[i]["_id"])
                if(cursor[j]["_id"] in rlist):
                    pass
                else:
                    rlist.append(cursor[j]["_id"])

    return returnHelper(content = rlist)




def leavecheck(uid,pid,mydb):

    res = mydb.selectCollection("xmateMessage")
    if(res["status"]):
        return res
    match_list = {"receiver_id":uid,"post_id":pid}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor = list(res["content"])
    if(len(cursor) > 0):
        return returnHelper(1,"You should first processe the join requests message associated with this post")
    
    return returnHelper()



def checkConflict(post_list, postid, conflict_list, mydb):
    if(len(post_list) == 0 or postid in conflict_list):
        return returnHelper()

    res = mydb.selectCollection("xmatePost")
    if(res["status"]):
        return res
    post_list.append(postid)
    match_list = {"_id": {"$in": post_list}}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor = list(res["content"])
    st = 0
    et = 0
    for doc in cursor:
        if(doc["_id"] == postid):
            st = doc["time_range"]["start_time"]
            et = doc["time_range"]["end_time"]
        else:
            pass
    flag = False
    for doc in cursor:
        if(doc["_id"] == postid):
            pass
        else:
            mst = max(st, doc["time_range"]["start_time"])
            met = min(et, doc["time_range"]["end_time"])
            if(mst < met):
                flag = True
                if(doc["_id"] in conflict_list):
                    pass
                else:
                    conflict_list.append(docu["_id"])
    if(flag):
        conflict_list.append(postid)

    return returnHelper()



##########################remind Tao to delete for plaintext
def finshReadMsg(uid, mid, mydb):
    #remove the message from the user unprocessed list
    res = mydb.selectCollection("xmateUser")
    if(res["status"]):
        return res
    match_list = {"_id":uid}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor = list(res["content"])
    msg_list = cursor[0]["unprocessed_message"]
    if(mid in msg_list):
        msg_list.remove(mid)
        ndata = {"unprocessed_message":msg_list}
        res = mydb.updateData(match_list, ndata)
        if(res["status"]):
            return res

    #remove the message from database
    res = mydb.selectCollection("xmateMessage")
    if(res["status"]):
        return res
    match_list = {"_id":mid}
    res = mydb.removeData(match_list)
    if(res["status"]):
        return res
    
    return returnHelper()



def checkMsg(mydb):

    res = mydb.selectCollection("xmateMessage")
    if(res["status"]):
        return res

    #find out of date messages(more than 24hr)
    current_time = moment.now().epoch()
    st = current_time - 86400
    match_list = {"created_time":{"$lt":st}}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor = list(res["content"])
    #delete out of date msg_ids in users' unprocessed msg list
    user_msg = {}
    outoftime_msg = []
    related_userlist = set()
    
    if(len(cursor) == 0):
        return returnHelper()
    for msg in cursor:
        outoftime_msg.append(msg["_id"])
        related_userlist.add(msg["receiver_id"])
        if(msg["receiver_id"] in user_msg.keys()):
            pass
        else:
            user_msg[msg["receiver_id"]] = []
        user_msg[msg["receiver_id"]].append([msg["_id"]])
    related_userlist = list(related_userlist)


    res = mydb.selectCollection("xmateUser")
    if(res["status"]):
        return res
    match_list = {"_id": {"$in": related_userlist}}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor =  res["content"]

    for users in cursor:
        uid = users["_id"]
        nlist = users["unprocessed_message"]
        for mid in user_msg[uid]:
            if(mid in nlist):
                nlist.remove(mid)

        match_list = {"_id":uid}
        ndata = {"unprocessed_message":nlist}
        res = mydb.updateData(match_list,ndata)
        if(res["status"]):
            return res

    #delete the messages in database
    res = mydb.selectCollection("xmateMessage")
    if(res["status"]):
        return res
    match_list = {"_id": {"$in": outoftime_msg}}
    res = mydb.removeData(match_list)
    if(res["status"]):
        return res

    return returnHelper()



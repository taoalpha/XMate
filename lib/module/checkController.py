#!/usr/bin/python
import moment

# Dispatch function for user api

# check message and get rid of all outdated messages

def returnHelper(status = 1, msg = None,content = None):
    return_val = {}
    return_val["status"] = status
    return_val["msg"] = msg
    return_val["content"] = content

    return return_val

def checkCache(mydb):
    #Remove the entries which are not updated for a long time

    id_list = []
    res = mydb.getData("cache", id_list)
    if(res["status"] != 1):
        return res
    cursor = res["content"]

    outoftime_cache = []
    current_time = moment.now().epoch()
    for doc in cursor:
        if(doc["create_time"] < current_time - 86400):
            outoftime_cache.append(doc["_id"])

    id_list = outoftime_cache
    res = mydb.removeData("cache", id_list)
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


def updateConflict(post_list,mydb):
    #get the new conflict list of a user
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


def updateUser(user_list, pid, t, mydb):
    id_list = user_list
    res = mydb.getData("user",id_list)
    if(res["status"] != 1):
        return res
    cursor = list(res["content"])
    del_msg = set()

    for user in cursor:
        user["history_events"].append(pid)
        user["schedule_list"].remove(pid)
        user["conflict_list"] = updateConflict(user["schedule_list"],mydb)
        user["total_activities"] = len(user["history_events"])
        user["total_time"] += t
        user["total_hours"] = (int)(user["total_time"] / 3600)


        id_list = user["unprocessed_message"]        
        mres = mydb.getData("message",id_list)
        if(mres["status"] != 1):
            return mres
        mcursor = list(mres["content"])
        for msg in mcursor:
            if(msg["post_id"] == pid):
                del_msg.add(msg["_id"])
                user["unprocessed_message"].remove(msg["_id"])

    id_list = user_list
    data_list = cursor
    res = mydb.updateData("user",id_list,data_list)
    if(res["status"] != 1):
        return res

    id_list = list(del_msg)
    res = mydb.removeData("message",id_list)
    if(res["status"] != 1):
        return res

    return returnHelper()



def checkSchedule(mydb):
    #Remove the schedules which have been finished
    id_list = []
    res = mydb.getData("schedule",id_list)
    if(res["status"] != 1):
        return res
    cursor = res["content"]

    current_time = moment.now().epoch()
    for doc in cursor:
        if("finish" not in doc.keys() and doc["end_time"] < current_time):
            user_list = []
            user_list = doc["member"]
            user_list.append(doc["owner"])
            t = doc["end_time"] - doc["start_time"]

            res = updateUser(user_list,doc["_id"],t,mydb)
            if(res["status"] != 1):
                return res

            doc["finish"] = True
            id_list = [doc["_id"]]
            data_list = [doc]
            res = mydb.updateData("schedule",id_list,data_list)
            if(res["status"] != 1):
                return res

    return returnHelper()





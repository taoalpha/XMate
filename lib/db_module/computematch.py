import sys, random, time
from datetime import datetime
import moment
from geopy.distance import vincenty



def computeMatchPosts(uid, post_content, mydb):

    dis_threshold = 2.0
    docu_list = []

    id_list = []
    res = mydb.getData("schedule",id_list)
    if(res["status"] != 1):
        return res
    cursor = res["content"]

    f1 = True
    f2 = True
    if(post_content["time_range"] == None):
        f1 = False
    if(post_content["latitude"] == None):
        f2 = False


    for doc in cursor:
        flag = True
        if(post_content["type"] == None or post_content["type"] == doc["type"]):
            if(post_content["time_range"] == None):
                pass
            else:
                ##########################modicfication!!!
                st = moment.unix(post_content["start_time"])
                nst = moment.date(st.year, st.month, st.day, 0).epoch()
                if(doc["start_time"] > nst and doc["start_time"] < nst + 86400*1.5):
                    doc["timediff"] = abs(doc["start_time"] - st)
                    pass
                else:
                    flag = False
        else:
            flag = False
        if(flag):
            if(post_content["latitude"] == None):
                pass
            else:
                pointa = (doc["latitude"],doc["longitude"])
                pointb = (post_content["latitude"],post_content["longitude"])
                dist = vincenty(loca, locb).miles
                if(dist < dis_threshold):
                    doc["diff"] = dist
                    pass
                else:
                    flag = False

        if(flag):
            docu_list.append(doc)

    if(f1 and f2):
        docu_list.sort(key = lambda postd: (postd["time_diff"],postd["diff"]))
    elif(f1 == False):
        if(f2):
            docu_list.sort(key = lambda postd: postd["diff"]) 
        else:
            docu_list.sort(key = lambda postd: postd["post_datetime"],reverse = True) 
    else:
        docu_list.sort(key = lambda postd: postd["time_diff"]) 

    return returnHelper(content = docu_list)



def computeMatchUsers(uid, pid, mydb):

    #history user? the first version just use history schedule
    recommend_user_list = set()
    id_list = []
    id_list.append(uid)
    res = mydb.getData("user",id_list)
    if(res["status"] != 1):
        return res
    user = res["content"][0]
    history_events = user["history_events"]

    #select suitable user from the current events
    id_list = []
    id_list.append(pid)
    res = mydb.getData("schedule",id_list)
    if(res["status"] != 1):
        return res
    doc = res["content"]
    post_type = doc["type"]

    id_list = []
    res = mydb.getData("schedule",id_list)
    if(res["status"] != 1):
        return res
    for doc in res["content"]:
        if(doc["type"] == post_type):
            for user_id in doc["member"]:
                recommend_user_list.add(user_id)

    #select users from history events
    id_list = history_events
    res = mydb.getData("history_schedule",id_list)
    if(res["status"] != 1):
        return res
    for doc in res["content"]:
        if(doc["type"] == post_type):
            for user_id in doc["member"]:
                recommend_user_list.add(user_id)

    recommend_user_list = list(recommend_user_list)
    return returnHelper(content = recommend_user_list)




def returnHelper(status = 1, msg = None,content = None):
    return_val = {}
    return_val["status"] = status
    return_val["msg"] = msg
    return_val["content"] = str(content)

    return return_val





import sys, random, time
from datetime import datetime
import moment
from geopy.distance import vincenty
from bson.objectid import ObjectId


def calculateDistance(pointa, pointb):

    loca = (pointa["latitude"],pointa["longitude"])
    locb = (pointb["latitude"],pointb["longitude"])
    return (vincenty(loca, locb).miles)


def computeMatchPosts(uid, post_content, mydb):

    res = mydb.selectCollection("xmatePost")
    if(res['status']):
        return res

    dis_threshold = 2.0
    match_list = {}
    docu_list = []

    if(post_content["type"] == None):
        pass
    else:
        match_list["type"] = post_content["type"]

    if(post_content["time_range"] == None):
        pass
    else:
        #st = datetime.fromtimestamp(post_content["time_range"]["start_time"])
        st = moment.unix(post_content["time_range"]["start_time"])
        #en = datetime.fromtimestamp(post_content["time_range"]["end_time"])
        en = moment.unix(post_content["time_range"]["end_time"])
        #nst = datetime(st.year, st.month, st.day, 0)
        nst = moment.date(st.year, st.month, st.day, 0).epoch()
        #nen = datetime(st.year, st.month, st.day, 23,59)
        nen = moment.date(st.year, st.month, st.day, 23,59).epoch()
        match_list["time_range.start_time"] = {'$gt': nst}
        #match_list["time_range.end_time"] = {'$lt': datetime.timestamp(nen)}
        match_list["time_range.end_time"] = {'$lt': nen}


    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor = res["content"]
    
    if(post_content["location"] == None):
        for doc in cursor:
            docu_list.append(doc)
        docu_list.sort(key = lambda postd: postd["post_datetime"], reverse = True)
    else:
        for doc in cursor:
            # if(doc["related_member"].count(uid) > 0):
            #     continue
            dist = calculateDistance(doc["location"], post_content["location"])
            if(dist < dis_threshold):
                doc["diff"] = dist
                docu_list.append(doc)
        docu_list.sort(key = lambda postd: (postd["post_datetime"],postd["diff"]))


    return returnHelper(content = docu_list)



def computeMatchUsers(uid, pid, mydb):
    #history user? the first version just use history schedule
    recommend_user_list = set()

    res = mydb.selectCollection("xmateUser")
    if(res["status"]):
        return res
    match_list = {"_id":ObjectId(uid)}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor = list(res["content"])
    history_events_list = cursor[0]["history_events"]

    #get post info and select user from current post
    res = mydb.selectCollection("xmatePost")
    if(res["status"]):
        return res
    match_list = {"_id":ObjectId(pid)}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor = list(res["content"])
    post_type = cursor[0]["type"]

    match_list = {"type":post_type}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res
    cursor = list(res["content"])
    if(len(cursor) > 0):
        for doc in cursor:
            for userid in doc["member"]:
                recommend_user_list.add(userid)


    #select users from history events
    res = mydb.selectCollection("xmateHistoryPost")
    if(res["status"]):
        return res
    history_events_list_objectid = []
    for doc in history_events_list:
        history_events_list_objectid.append(ObjectId(doc))
    match_list = {{"_id": {"$in": history_events_list_objectid}},"type":post_type}
    res = mydb.getData(match_list)
    if(res["status"]):
        return res

    cursor = list(res["content"])
    if(len(cursor) > 0):
        for doc in cursor:
            for userid in doc["member"]:
                recommend_user_list.add(userid)
            recommend_user_list.add(doc["owner"])

    recommend_user_list = list(recommend_user_list)
    return returnHelper(content = recommend_user_list)




def returnHelper(status = 0, msg = None,content = None):
    return_val = {}
    return_val["status"] = status
    return_val["msg"] = msg
    return_val["content"] = str(content)

    return return_val





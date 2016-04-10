import sys, random, time
from datetime import datetime
from geopy.distance import vincenty
from db import CDatabase


def calculateDistance(pointa, pointb):
    '''
        Desc: 
            Compute distance between pointa and pointb
        Args:
            pointa, pointb = {"latitude":..., "lonfitude":...}(must contain these two keys)
        Ret:
            return the distance(miles)
    '''

    loca = (pointa["latitude"],pointa["longitude"])
    locb = (pointb["latitude"],pointb["longitude"])
    return (vincenty(loca, locb).miles)

def getTimeDiff(time1,time2):
    '''
        Desc: 
            Get time difference   
        Args:
            time: realtime - 1970.1.1 seconds
        Ret:
            two time's difference(minutes)
    '''
    timediff = (time1 - time2) / 60
    return abs(timediff) 
       

def giveSearchResult(post_content, mydb):
    '''
        Desc: 
            Give "search" result
            
        Args:
            mydb: CDatabase object()
            post_content: {"type:"..., "time_range":..., "location":...}
        Ret:
            Return the result documents list
    '''
    res = mydb.selectCollection("xmatePost") ###### 
    if(res['status']):
        print(res)
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
        st = post_content["time_range"]["start_time"]
        en = post_content["time_range"]["end_time"]
        match_list["time_range.start_time"] = {'$gt': st}
        match_list["time_range.end_time"] = {'$lt': en}

    res = mydb.getData(match_list)
    if(res["status"]):
        print(res)
    else:
        cursor = res["content"]

    if(post_content["location"] == None):
        for doc in cursor:
            docu_list.append(doc)
        docu_list.sort(key = lambda postd: postd["post_datetime"], reverse = True)
    else:

        for doc in cursor:
            dist = calculateDistance(doc["location"], post_content["location"])
            if(dist < dis_threshold):
                doc["diff"] = dist
                docu_list.append(doc)
        docu_list.sort(key = lambda postd: (postd["post_datetime"],postd["diff"]))

    return docu_list
#post_content --> sid
def computeMatchPosts(sid, mydb):
    
    res = mydb.selectCollection("xmatePost") ###### 
    if(res['status']):
        print(res)

    dis_threshold = 2.0
    match_list = {}
    docu_list = []

    st = datetime.fromtimestamp(post_content["time_range"]["start_time"])
    en = datetime.fromtimestamp(post_content["time_range"]["start_time"])

    nst = datetime(st.year, st.month, st.day, 0)
    nen = datetime(st.year, st.month, st.day, 23,59)


    match_list["type"] = post_content["type"]
    match_list["time_range.start_time"] = {'$gt': datetime.timestamp(nst)}
    match_list["time_range.end_time"] = {'$lt': datetime.timestamp(nen)}

    res = mydb.getData(match_list)
    if(res["status"]):
        print(res)
    else:
        cursor = res["content"]

    for doc in cursor:
        if(doc["related_member"].count(uid) > 0):
            continue

        dist = calculateDistance(doc["location"], post_content["location"])
        if(dist < dis_threshold):
            doc["diff"] = dist
            docu_list.append(doc)
    docu_list.sort(key = lambda postd: (postd["post_datetime"],postd["diff"]))

    return docu_list






#def computeMatchUsers(uid, post_content):

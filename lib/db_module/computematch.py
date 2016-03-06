import sys, random, time
from datetime import date
from geopy.distance import vincenty
from db import CDatabase



def calculateDistance(pointa, pointb):
    '''
        Desc: 
            Compute distance between pointa and pointb
        Args:
            pointa, pointb = {"city":..., "lat":..., "lon":...}
        Ret:
            return the distance(miles)
    '''

    loca = (pointa["latitude"],pointa["longitude"])
    locb = (pointb["latitude"],pointb["longitude"])
    return (vincenty(loca, locb).miles)

def getTimeDiff(time1,time2):
    '''
        Desc: 
            Get time difference by offset seconds
            
        Args:
            time: realtime - 1970.1.1
        Ret:
            two time's difference(minutes)
    '''
    timediff = (time1 - time2) / 60
    return abs(timediff)


def giveSearchResult(post_content, mydb):
    dis_threshold = 2.0
    match_list = {}

    ploc = post_content["location"]
    pt = post_content["time_range"]
    ptype = post_content["type"]

    if(ptype == None):
        pass
    else:
        match_list["type"] = ptype

    if(pt == None):
        pass
    else: 
        st = post_content["time_range"]["start_time"]
        en = post_content["time_range"]["end_time"]
        match_list["time_range.start_time"] = {'$gt': st}
        match_list["time_range.end_time"] = {'$lt': en}

    mydb.selectCollection("xmatePost") ######
    print(match_list)
    res = mydb.getData(match_list)     #####

    if(res["status"]):
        print(res)
    else:
        cursor = res["content"]

    docu_list = []
    if(ploc == None):
        for doc in cursor:
            docu_list.append(doc)
        docu_list.sort(key = lambda postd: postd["post_datetime"], reverse = True)
    else:

        for doc in cursor:
            dist = calculateDistance(doc["location"], ploc)
            if(dist < dis_threshold):
                doc["diff"] = dist
                docu_list.append(doc)
        docu_list.sort(key = lambda postd: (postd["post_datetime"],postd["diff"]))

    return docu_list



# def computeMatchPosts(uid, post_content):



# def computeMatchUsers(uid, post_content):
#     pass










































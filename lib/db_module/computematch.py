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
        match_list["type"] = ptype
    
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

def computeMatchPosts(uid, post_content, mydb):
    
    res = mydb.selectCollection("xmatePost") ###### 
    if(res['status']):
        print(res)

    dis_threshold = 2.0
    match_list = {}










def computeMatchUsers(uid, post_content):










































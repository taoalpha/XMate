import sys, random, time
from datetime import date
from geopy.distance import vincenty

from userModule import CUser
from postModule import CPost
from historyPostModule import CHistoryPost



def calculateDistance(pointa, pointb):
    '''
        Desc: 
            Compute distance between pointa and pointb
        Args:
            pointa, pointb = {"city":..., "lat":..., "lon":...}
        Ret:
            return the distance(miles)
    '''

    loca = (pointa["lat"],pointa["lon"])
    locb = (pointb["lat"],pointb["lon"])
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


def computeMatchPosts(uid, post_content):



def computeMatchUsers(uid, post_content):
    pass

def giveSearchResult(uid, post_content):
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
        match_list[]
































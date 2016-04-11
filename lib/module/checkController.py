#!/usr/bin/python
import moment
from bson.objectid import ObjectId

# Dispatch function for user api

# check message and get rid of all outdated messages

def returnHelper(status = 0, msg = None,content = None):
    return_val = {}
    return_val["status"] = status
    return_val["msg"] = msg
    return_val["content"] = str(content)

    return return_val



def checkMsg(mydb):

    res = mydb.selectCollection("xmateMessage")
    if(res["status"]):
        return res

    #find out of date messages(more than 24hr)
    current_time = moment.now().epoch()
    st = current_time - 86400
    match_list = {"create_time":{"$lt":st}}
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
        related_userlist.add(ObjectId(msg["receiver_id"]))
        if(ObjectId(msg["receiver_id"]) in user_msg.keys()):
            pass
        else:
            user_msg[ObjectId(msg["receiver_id"])] = []
        user_msg[ObjectId(msg["receiver_id"])].append(msg["_id"])
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


def checkSchedule(db):
    '''
    What needs to be done in this function

    Target: all schedules end before current time.
    Logic:
        1. Move this schedule to historyPost collection
        2. Remove all related message
            1). Remove all these messages from its receiver's unprocessed_list
        3. Move this schedule from schedule_list to history_schedule_list in all members' profile
        4. Add this schedule to its owner's history_schedule_list
        5. Add members and owner to all members and owner's history_partner
        6. Update owner and member's conflict_list
    '''

    res = db.selectCollection("xmatePost")
    # handle db err
    if(res["status"]):
        return res

    # find all outdated messages
    current_time = moment.now().epoch()
    match_list = {"time_range.time_end": {"$lt":current_time}}
    res = db.getData(match_list)

    # handle db err
    if(res["status"]):
        return res

    cursor = list(res["content"])

    # move these schedules to historyPost
    tobe_moved_schedule = []
    tobe_moved_msg = []
    tobe_affected_user = []

    # no match, then return
    if(len(cursor) == 0):
        return returnHelper()

    # found matches, handle one ny one instead of all at last time
    # if err happens, then stop
    # handler logic order:
    # move to history post if not exist -> update unprocess_list if exist -> update schedule_list and history_schedule_list -> update conflict_list (need recompute) -> update history_partner -> remove from current post
    for schedule in cursor:
        print ""
        print ""
        print ""
        print "##############"
        print schedule
        print "start copying to history"
        res = moveToHistoryPost(schedule,db)
        if res["status"]:
            # fail to move to history_post
            return res

        print "start updating msg"
        res = updateMsg(schedule,db)
        if res["status"]:
            # fail to handle the related msg
            return res

        print "start updating schedule"
        res = updateUserScheduleList(schedule,db)
        if res["status"]:
            # fail to handle the schedule_list update
            # or the conflict_list update
            return res

        print "start updating historypartner"
        res = updateUserHistoryPartner(schedule,db)
        if res["status"]:
            # fail to handle the history partner update
            return res


        print "start removing post"
        # delete the post from current post collection at the last step
        res = removeFromPost(schedule,db)
        if res["status"]:
            # fail to handle the schedule_list update
            return res
        '''
        '''

    return returnHelper()

def updateUserHistoryPartner(schedule, db):
    '''
    Update everyone's historypartner field
    '''
    res = db.selectCollection("xmateUser")
    # handle db err
    if res["status"]:
        return res

    # get the member list
    user_list = schedule["member"]
    user_list.append(schedule["owner"])
    uids = list(set(user_list))

    for uid in uids:
        match_list = {"_id": ObjectId(uid)}
        res = db.getData( match_list )
        # handle db err
        if res["status"]:
            return res

        match_res = list(res["content"])

        print "#################### number of history partner:"
        print len(match_res)
        if len(match_res) > 0:
            # if exist
            history_partner = match_res[0]["history_partner"]
            history_partner.extend(uids)
            print "############HISTORY PARTNER########"
            print history_partner
            print "############HISTORY PARTNER########"
            # update the history_events
            print "update the history partner"
            res = db.updateData( match_list , {"history_partner":list(set(history_partner))} )
            # handle db err
            if res["status"]:
                return res
            # if nothing wrong, remove it from current schedule_list

    # if nothing wrong happened
    res["status"] = 0
    return res



def updateUserScheduleList(schedule,db):
    '''
    Add it to all members' history_schedule list (set)
    Remove from the schedule_list
    '''
    res = db.selectCollection("xmateUser")
    # handle db err
    if res["status"]:
        return res


    # get the member list
    user_list = schedule["member"]
    user_list.append(schedule["owner"])

    for uid in list(set(user_list)):
        match_list = {"_id": ObjectId(uid)}
        res = db.getData( match_list )
        # handle db err
        if res["status"]:
            return res

        match_res = list(res["content"])
        print "####### the number of user found"
        print len(match_res)
        print "#######"


        # add to history_events
        if len(match_res) > 0:
            print "found the user"
            # if exist
            history_events = match_res[0]["history_events"]
            history_events.append(str(schedule["_id"]))
            # update the history_events
            print "update the history events"
            print history_events
            res = db.updateData( match_list , {"history_events":list(set(history_events))} )
            # handle db err
            if res["status"]:
                return res
            # if nothing wrong, remove it from current schedule_list
            schedule_list = match_res[0]["schedule_list"]

            if str(schedule["_id"]) in schedule_list:
                schedule_list.remove(str(schedule["_id"]))

            # update the schedule_list
            print "update the schedule list"
            print schedule_list
            res = db.updateData( match_list , { "schedule_list" : list(set(schedule_list)) } )
            # handle db err
            if res["status"]:
                return res
            # need to recheck the conflict
            # get current conflict_list
            conflict_list = match_res[0]["conflict_list"]
            # if the removed id is in conflict
            if str(schedule["_id"]) in conflict_list:
                conflict_res = checkConflict(schedule_list,db)
                # handle err
                if conflict_res["status"]:
                    return res
                # if nothing wrong, then update the conflict
                res = updateConflictList(match_list,conflict_res["conflict"],db)
                # handle err
                if res["status"]:
                    return res


    # if nothing wrong happened
    res["status"] = 0
    return res


def updateConflictList(match_list, conflict_list,db):
    '''
    Reset the conflict list
    '''
    res = db.selectCollection("xmateUser")
    # handle db err
    if res["status"]:
        return res

    print "update the conflict list"
    res = db.updateData( match_list , { "conflict_list": list(set(conflict_list)) } )
    # handle db err
    if res["status"]:
        return res

    # if nothing wrong happened
    res["status"] = 0
    return res




def checkConflict(raw_schedule_list,db):
    '''
    Check the conflict among the user's schedule_list
    '''
    res = db.selectCollection("xmatePost")
    # handle db err
    if res["status"]:
        return res

    schedule_list = []
    for sid in list(set(raw_schedule_list)):
        schedule_list.append(ObjectId(sid))

    res = db.getData( { "_id": { "$in" : schedule_list } } )
    # handle db err
    if res["status"]:
        return res

    schedules = list(res["content"])
    conflict_list = []

    for i in range(0,len(schedules)):
        for j in range(i+1,len(schedules)):
            if isConflict(schedules[i],schedules[j]):
                conflict_list.append(schedules[i])
                conflict_list.append(schedules[j])

    # if nothing wrong happened
    res["status"] = 0
    res["conflict"] = conflict_list
    return res

def isConflict(s1,s2):
    '''
    Check whether the two schedules are conflict or not
    Conflict rules:
        1. s1.start_time > s2.start_time && s1.start_time < s2.end_time
        2. s1.end_time > s2.start_time && s1.end_time < s2.end_time
    '''
    if (s1["time_range"]["time_start"] > s2["time_range"]["time_start"] and s1["time_range"]["time_start"] < s2["time_range"]["time_end"]) or (s1["time_range"]["time_end"] > s2["time_range"]["time_start"] and s1["time_range"]["time_end"] < s2["time_range"]["time_end"]) :
        return true
    else:
        return false





def updateMsg(schedule,db):
    '''
    Remove it from all receiver's unprocess_list
    Remove the msg
    '''
    print "entering updating msg"
    res = db.selectCollection("xmateMessage")
    # handle db err
    if res["status"]:
        return res

    res = db.getData( { "post_id": str(schedule["_id"]) } )
    # handle db err
    if res["status"]:
        return res

    list_msg = list(res["content"])

    print "####### number of related messages"
    print len(list_msg)
    print "#######"

    if len(list_msg) > 0:
        # found related msg and ready to remove them
        for msg in list_msg:
            # remove it from its receiver's unprocess_list
            receiver_id = msg["receiver_id"]
            print "update unprocess list"
            res = updateUserUnprocessedList(receiver_id,msg["_id"],db)
            # handle db err
            if res["status"]:
                return res
            # then remove the msg from the msg collection
            print "remove the msg"
            res = db.selectCollection("xmateMessage")
            # handle db err
            if res["status"]:
                return res
            res = db.removeData( {"_id": msg["_id"] } )
            # handle db err
            if res["status"]:
                return res

    # if nothing wrong happened
    res["status"] = 0
    return res


def updateUserUnprocessedList(uid,mid,db):
    '''
    Remove the msg id from the unrprocessedList of the user
    '''
    res = db.selectCollection("xmateUser")
    # handle db err
    if res["status"]:
        return res

    # get the user data
    res = db.getData( { "_id": ObjectId(uid) } )
    # handle db err
    if res["status"]:
        return res

    # get the current unprocessed_list
    unprocessed_list = list(res["content"])[0]["unprocessed_message"]
    print "current user's unprocessed list:"
    print unprocessed_list

    if str(mid) in unprocessed_list:
        # update the list if it has the message
        unprocessed_list.remove(str(mid))
        res = db.updateData({ "_id": ObjectId(uid) }, { "unprocessed_message": unprocessed_list })
        if res["status"]:
            return res

    # if nothing wrong happened
    res["status"] = 0
    return res



def removeFromPost(schedule,db):
    '''
    Remove it from current post collection
    '''
    res = db.selectCollection("xmatePost")
    # handle db err
    if res["status"]:
        return res

    print "remove from the post"
    res = db.removeData( { "_id": schedule["_id"] } )
    # handle db err
    if res["status"]:
        return res

    # if nothing wrong happened
    res["status"] = 0
    return res




def moveToHistoryPost(schedule,db):
    '''
    Insert the schedule to history post collection
    '''
    print "entering moving to history"
    res = db.selectCollection("xmateHistoryPost")
    # handle db err
    if res["status"]:
        return res

    res = db.getData( { "_id": schedule["_id"] } )
    # handle db err
    if res["status"]:
        return res

    if len(list(res["content"])) == 0:
        # not exist
        print "not exist, will move to history"
        res = db.insertData(schedule)
        # handle db err
        if res["status"]:
            return res
        '''
        '''
    else:
        print "exist, do nothing"

    # if nothing wrong happened
    res["status"] = 0
    return res

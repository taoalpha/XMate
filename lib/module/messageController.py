#!/usr/bin/python
FIELD = {
    "_id":"",
    "post_id":"",
    "sender_id":"",
    "receiver_id":"",
    "type":""
}
# Dispatch function for user api
from ..db_module import computematch as CM
import moment
from .message import msgDelivery as msgDelivery


def messageDispatch(mid,action,request,db):
    '''
        Desc:
            dispatch request to proper handelr
        Args:
            mid: message id, None if no
            action: like join or invite
            request: including the http method like get/post... and form data
            db: reference to the db instance
    '''

    res = {}  # store all temp result
    res["_id"] = mid

    # content stores all validate information
    res["status"] = 1

    # forbid deleting message from the http request
    # all outdated message (>24 hours) will be deleted by our self-check procedure
    if request.method == "DELETE":
        #tempResp = checkController.checkMsg(db)
        #tempResp = checkController.checkSchedule(db)
        res["status"] = 4
	res["msg"] = "Forbidden operation!!"
	return res


    if request.method == "POST":
        res["action"] = request.form["type"]
        if res["action"] == "join":
            tempRes = msgDelivery.sendJoin(request.form["sender_id"],request.form["post_id"],db)
            if tempRes["status"] != 1:
                # some errors happen
                res["status"] = tempRes["status"]
                res["msg"] = tempRes["msg"]
                return res
            else:
                # reeturn the message id in our system
                res["content"] = tempRes["content"]
                return res["content"]
        elif res["action"] == "invite":
            tempRes = msgDelivery.sendInvitation(request.form["sender_id"], request.form["post_id"], request.form["receiver_id"], db)
            if tempRes["status"] != 1:
                # some errors happen
                res["status"] = tempRes["status"]
                res["msg"] = tempRes["msg"]
                return res
            else:
                # reeturn the message id in our system
                res["content"] = tempRes["content"]
                return res["content"]

    # for decline or accept or read
    elif request.method == "PUT":
        res["action"] = request.form["type"]
        if res["action"] == "decline":
            tempRes = msgDelivery.declineRequest(request.form["sender_id"], request.form["_id"], db)
            if tempRes["status"] != 1:
                # some errors happen
                res["status"] = tempRes["status"]
                res["msg"] = tempRes["msg"]
                return res
            else:
                # success
                res["content"] = {}
                return res["content"]
        elif res["action"] == "accept":
            tempRes = msgDelivery.acceptRequest(request.form["sender_id"], request.form["_id"], db)
            if tempRes["status"] != 1:
                # some errors happen
                res["status"] = tempRes["status"]
                res["msg"] = tempRes["msg"]
                return res
            else:
                # success accepted
                res["content"] = {}
                return res["content"]
        elif (res["action"] == "leave" or request.form["type"]=="leave"):
            tempRes = msgDelivery.leavePost(request.form["sender_id"], request.form["post_id"], db)
	    if tempRes["status"] != 1:
                # some errors happen
                res["status"] = tempRes["status"]
                res["msg"] = tempRes["msg"]
                return res
            else:
                # leave the group
                res["content"] = {}
                return res["content"]
        elif res["action"] == "read" or request.form["type"]=="read":
            # only for plain message -- type
            tempRes = msgDelivery.finishReadMsg(request.form["sender_id"], request.form["_id"], db)
	    if tempRes["status"] != 1:
                # some errors happen
                res["status"] = tempRes["status"]
                res["msg"] = tempRes["msg"]
                return res
	    else:
                # leave the group
                res["content"] = {}
                return res["content"]
    elif request.method == "GET":
        '''
            Desc:
                fetch all data about the schedule
            Args:
                request: request with different data
                res: result that we need to update and return
            Err:
                1. invalid objectId
                2. fail to get data
                3. no match result
        '''
        # error handler for invalid objectid

        data = res["_id"]
        docs = db.getData("message",[data])
        if docs["status"] != 1:
            return docs

        return docs["content"][0]

    # if any err, return with err status
    if res["status"] != 1:
        return res

    return res["content"]

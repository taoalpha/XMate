#!/usr/bin/python

# Dispatch function for user api
from .message import getHandler as getHandler
from .message import postHandler as postHandler
from .message import putHandler as putHandler
from .message import deleteHandler as deleteHandler
from .message import msgDelivery as msgDelivery
from . import checkController

# define dispatch dictionary
DISPATCH = {
    "GET": getHandler.getData,
    "POST": postHandler.postData,
    "PUT": putHandler.putData,
    "DELETE": deleteHandler.delData
}

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
    res["action"] = action
    res["mid"] = mid

    # content stores all validate information
    res["rawdata"] = {}
    res["content"] = {}

    # store err msg
    res["err"] = {"status":0}

    # forbid deleting message from the http request
    # all outdated message (>24 hours) will be deleted by our self-check procedure
    if request.method == "DELETE":
        #tempResp = checkController.checkMsg(db)
        tempResp = checkController.checkSchedule(db)
	res["err"]["status"] = 1
	res["err"]["msg"] = "Forbidden operation!!"
        res["err"]["content"] = tempResp
	return res["err"]

    if request.method == "POST":
        res["action"] = request.form["type"]
        if res["action"] == "join":
            tempRes = msgDelivery.sendJoin(request.form["sender"],request.form["post"],db)
            if tempRes["status"] == 1:
                # some errors happen
                res["err"]["status"] = 1
                res["err"]["msg"] = tempRes["msg"]
                return res["err"]
            else:
                # reeturn the message id in our system
                res["content"] = {"_id":tempRes["content"]}
                return res["content"]
        elif res["action"] == "invite":
            tempRes = msgDelivery.sendInvitation(request.form["sender_id"], request.form["post_id"], request.form["receiver_id"], db)
	    print tempRes
            if tempRes["status"] != 1:
                # some errors happen
                res["err"]["status"] = 1
                res["err"]["msg"] = tempRes["msg"]
                return res["err"]
            else:
                # reeturn the message id in our system
                res["content"] = {"_id":tempRes["content"]}
                return res["content"]
    elif request.method == "PUT":
        if res["action"] == "decline":
            tempRes = msgDelivery.declineRequest(request.form["sender"], request.form["mid"], db)
            if tempRes["status"] == 1:
                # some errors happen
                res["err"]["status"] = 1
                res["err"]["msg"] = tempRes["msg"]
                return res["err"]
            else:
                # success
                res["content"] = {}
                return res["content"]
        elif res["action"] == "accept":
            tempRes = msgDelivery.acceptRequest(request.form["sender"], request.form["mid"], db)
            if tempRes["status"] == 1:
                # some errors happen
                res["err"]["status"] = 1
                res["err"]["msg"] = tempRes["msg"]
                return res["err"]
            else:
                # success accepted
                res["content"] = {}
                return res["content"]
        elif (res["action"] == "leave" or request.form["type"]=="leave"):
            tempRes = msgDelivery.leavePost(request.form["sender"], request.form["post"], db)
            if tempRes["status"] == 1:
                # some errors happen
                res["err"]["status"] = 1
                res["err"]["msg"] = tempRes["msg"]
                return res["err"]
            else:
                # leave the group
                res["content"] = {}
                return res["content"]
        elif res["action"] == "read" or request.form["type"]=="read":
            # only for plain message -- type
            tempRes = msgDelivery.finishReadMsg(request.form["sender"], request.form["mid"], db)
            if tempRes["status"] == 1:
                # some errors happen
                res["err"]["status"] = 1
                res["err"]["msg"] = tempRes["msg"]
                return res["err"]
            else:
                # leave the group
                res["content"] = {}
                return res["content"]
    elif request.method == "GET":
        DISPATCH[request.method](request,res,db)

    # if any err, return with err status
    if res["err"]["status"]:
        return res["err"]

    # dispatch with field and args, but only for get
    # just copy the rawdata to content
    if request.method == "GET":
        res["content"] = res["rawdata"]
        # return data

    return res["content"]

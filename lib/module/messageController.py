#!/usr/bin/python

# Dispatch function for user api
from .message import getHandler as getHandler
from .message import postHandler as postHandler
from .message import putHandler as putHandler
from .message import deleteHandler as deleteHandler

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
	res["err"]["status"] = 1
	res["err"]["msg"] = "Forbidden operation!!"
	return res["err"]

    # dispatch with method: GET/POST/PUT/DELETE
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

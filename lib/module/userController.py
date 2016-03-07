#!/usr/bin/python

# Dispatch function for user api
from .user import getHandler as getHandler
from .user import postHandler as postHandler
from .user import putHandler as putHandler
from .user import deleteHandler as deleteHandler

# define dispatch dictionary
DISPATCH = {
    "GET": getHandler.getData,
    "POST": postHandler.postData,
    "PUT": putHandler.putData,
    "DELETE": deleteHandler.delData,
    #"PATCH": patchHandler.patchData,
}

# define dispatch handler for user
def userDispatch(uid,field,request,db):
    '''
        Desc:
            dispatch request to proper handelr
        Args:
            uid: user id, None if no
            field: specify the return combination of the data
    '''
    res = {}  # store all temp result
    res["field"] = field
    res["uid"] = uid

    # content stores all validate information
    res["rawdata"] = {}
    res["content"] = {}

    # store err msg
    res["err"] = {"status":0}

    # dispatch with method: GET/POST/PUT/DELETE
    DISPATCH[request.method](request,res,db)

    # if any err, return with err status
    if res["err"]["status"]:
        return res["err"]

    # dispatch with field and args, but only for get
    # there is no field option for PUT and DELETE
    if request.method == "GET":
        if field != None:
            # filter data with field, like user/uid/profle, user/uid/messages ...
            # no need to pass the db since only filter with specific field ...
            getHandler.filterData(request,res)
        else:
            # other wise, no need to filter the data
            res["content"] = res["rawdata"]

    # return data
    return res["content"]

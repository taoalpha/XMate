#!/usr/bin/python

# Dispatch function for user api
from .schedule import getHandler as getHandler
from .schedule import postHandler as postHandler
from .schedule import putHandler as putHandler
from .schedule import deleteHandler as deleteHandler

# define dispatch dictionary
DISPATCH = {
    "GET": getHandler.getData,
    "POST": postHandler.postData,
    "PUT": putHandler.putData,
    "DELETE": deleteHandler.delData,
}

def scheduleDispatch(sid,field,request,db):
    '''
        Desc:
            schedule dispatch based on different http request methods
        Args:
            sid: schedule id
            field: search or match, to get the search result or match result of a specific schedule

    '''
    res = {}
    res["field"] = field
    res["sid"] = sid

    # store any possible err msg
    res["err"] = {}

    # rawdata stores all rough information
    res["rawdata"] = {}
    # content stores all validate information
    res["content"] = {}

    # dispatch with method
    DISPATCH[request.method](request,res,db)

    # return early if there is any err
    if res["err"]["status"]:
        return res["err"]

    # dispatch with field and args
    if field != None:
        # dispatch to search or match or any other possible fields
        getHandler.filterData(request,res,db)
    else:
        # if no field, which means just need to get info of this schedule
        res["content"] = res["rawdata"]
    return res["content"]

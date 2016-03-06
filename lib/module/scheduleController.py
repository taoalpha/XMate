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
    res = {}
    res["field"] = field
    res["sid"] = sid
    res["err"] = {}

    # content stores all validate information

    res["rawdata"] = {}
    res["content"] = {}
    # dispatch with method

    DISPATCH[request.method](request,res,db)

    # dispatch with field and args
    if field != None:
        getHandler.filterData(request,res,db)
    else:
        res["content"] = res["rawdata"]
    return res["content"]

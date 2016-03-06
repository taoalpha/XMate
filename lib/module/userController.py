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
    "DELETE":{
    },
    "PATCH":{
    }
}

def userDispatch(uid,action,request):
    res = {}
    res["action"] = action
    res["uid"] = uid
    # content stores all validate information
    res["rawdata"] = {}
    res["content"] = {}
    res["err"] = {"status":0}
    # dispatch with method

    DISPATCH[request.method](request,res)

    print(res)

    if res["err"]["status"]:
        print(res)
        return res["err"]

    # dispatch with action and args
    if request.method == "GET":
        if action != None:
            getHandler.filterData(request,res)
        else:
            res["content"] = res["rawdata"]
    return res["content"]

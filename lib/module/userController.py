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
def userDispatch(uid,field,request):
    '''
        Desc:
            dispatch request to proper handelr
        Args:
            uid: user id, None if no
            field: specify the return combination of the data
    '''
    res = {}
    res["field"] = field
    res["uid"] = uid
    # content stores all validate information
    res["rawdata"] = {}
    res["content"] = {}
    res["err"] = {"status":0}
    # dispatch with method

    DISPATCH[request.method](request,res)

    if res["err"]["status"]:
        return res["err"]

    # dispatch with field and args
    if request.method == "GET":
        if field != None:
            getHandler.filterData(request,res)
        else:
            res["content"] = res["rawdata"]
    return res["content"]

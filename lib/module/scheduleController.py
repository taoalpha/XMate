#!/usr/bin/python

# Dispatch function for user api
from ...db_module import computematch as CM

FIELDS = {
    "_id":"",
    "type":"",
    "latitude":"",
    "longitude":"",
    "start_time":"",
    "end_time":"",
    "post_time":"",
    "owner":"", 
    "member":[]
}
# define dispatch dictionary
DISPATCH = {
    "GET": getData,
    "POST": postData,
    "PUT": putData,
    "DELETE": delData,
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
    res["status"] = 1

    # content stores all validate information
    res["content"] = {}
    if request.method == "DELETE":
        res["status"] = 4
        res["msg"] = "Forbidden operation"
        return res

    # dispatch with method
    DISPATCH[request.method](request,res,db)

    # return early if there is any err
    if (res["status"] != 1):
        return res
    return res
def delData(request,res,db):
    '''
        Desc:
            delete the schedule exercise by id
        Args:
            request: maybe useful
            res: id stores in res["sid"], and update res with proper information
        Err:
            1. invalid objectId
            2. fail to delete data
    '''

    # error handler for invalid objectid

    docs = db.removeData("schedule",[res["_id"]])
    return res
# define the update for post
def putData(request,res,db):
    '''
        Desc:
            update some fields of a schedule exercise
        Args:
            request: store the updated information of exercise within request.form
            db: referrence to db object
            res: store the status
        Err:
            1. fail to update data
    '''
    data = FIELD;
    # if request.form is a validate dictionary, may ignore this part
    for key in request.form:
        data[key] = request.form[key]

    res = db.updateData("schedule",[res["_id"]],[data])

    return res
def postData(request,res,db):
    '''
        Desc:
            create a new schedule exercise
        Args:
            request: store the details of exercise within request.form
            db: referrence to db object
            res: store the status
        Err:
            1. fail to insert data
    '''
    data = FIELD;
    # if request.form is a validate dictionary, may ignore this part
    for key in request.form:
        data[key] = request.form[key]

    res = db.insertData("schedule",[data])
    return res

# define the getData function
def getData(request,res,db):
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
    docs = db.getData("schedule",data)

    return docs

# define the filterData function
# def filterData(request,res,db):
#     '''
#         Desc:
#             Filter data with field parameter
#         Args:
#             request : request object
#             res : result needs to return
#     '''
#     if res["field"] == None:
#         res["content"] = res["rawdata"]
#         return res
#     elif res["field"] == "search":
#         # call search function to get search results
#         # search happens when no sid but field = search
#         # all parameters should pass in by request.form
#         res["content"]["entries"] = []
#         res["content"]["entries"] = CM.giveSearchResult(10,res["rawdata"],db)
#         return res
#     elif res["field"] == "match":
#         # call match function to get match results
#         # match happens when there is a sid and field = match
#         res["content"]["entries"] = []
#         res["content"]["entries"] = CM.computeMatchPosts(10,res["rawdata"],db)
#         print(len(res["content"]["entries"]))
#         return res





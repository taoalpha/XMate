#!/usr/bin/python
FIELD = {
    "_id":"",
    "type":"",
    "latitude":123123.12,
    "longitude":123123.12,
    "start_time":123812938.12,
    "end_time":16253724.2,
    "owner":"",
    "date":"",
    "member":[]
}
# Dispatch function for user api
from ..db_module import computematch as CM
from .message import msgDelivery as MD
import moment

def delData(request,res,db):
    '''
        Desc:
            delete the schedule exercise by id
        Args:
            request: maybe useful
            res: id stores in res["_id"], and update res with proper information
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

    if "action" in request.form:
        # if request for matching, then forward to it
        if request.form["action"] == "match":
            return getMatch(request.form["uid"],request.form['pid'],db)
        # if request for searching, then forward to it
        if request.form["action"] == "search":
            searchData = {"start_time": -1, "end_time": -1, "type":"", 'latitude':-1, 'longitude': -1}
            for i in request.form:
                if i in searchData:
                    searchData[i] = request.form[i]
            return getSearch(searchData,db)
        if request.form["action"] == "leave":
            return MD.leavePost(request.form["uid"], request.form["pid"],db)

    # normal requests
    data = FIELD;
    # if request.form is a validate dictionary, may ignore this part
    for key in request.form:
        data[key] = request.form[key]

    data["created_time"] = moment.now().epoch()
    data["end_time"] = float(data["end_time"])
    data["start_time"] = float(data["start_time"])
    data["longitude"] = float(data["longitude"])
    data["latitude"] = float(data["latitude"])

    res = db.insertData("schedule",[data])

    if (res["status"] != 1):
        return res

    pid = res['content'][0]["_id"]

    # update schedule_list for its owner
    userRes = db.getData("user",[request.form["creator"]])

    if (userRes["status"] != 1):
        return userRes
    user = userRes["content"][0]
    # need to check conflict
    print "####"
    print pid
    user["schedule_list"].append(pid)
    userRes = db.updateData("user",[request.form["creator"]],[user])
    if (userRes["status"] != 1):
        return userRes

    return res

# special for get match and get search
def getMatch(uid,pid,db):
    '''
        Desc:
            Get the match list of a list
        Args:
            post_id: which post we want to get the match list (of users)
    '''
    res = CM.computeMatchUsers(uid,pid,db)
    return res

def getSearch(form, db):
    '''
        Desc:
            Get the search result
        Args:
            form.start_time
            form.end_time
            form.type
            form.latitude
            form.longitude
            form.uid
    '''
    form["start_time"] = float(form["start_time"])
    form["end_time"] = float(form["end_time"])
    form["latitude"] = float(form["latitude"])
    form["longitude"] = float(form["longitude"])
    res = CM.computeMatchPosts(form,db)
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
    docs = db.getData("schedule",[data])

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
    res["_id"] = sid
    # store any possible err msg
    res["status"] = 1

    # content stores all validate information
    res["content"] = {}
    if request.method == "DELETE":
        res["status"] = 4
        res["msg"] = "Forbidden operation"
        return res

    # dispatch with method
    res = DISPATCH[request.method](request,res,db)

    if "action" in request.form:
	if (res["status"] != 1):
       	    return res
	return res["content"]

    # return early if there is any err
    if (res["status"] != 1):
        return res
    return res["content"][0]

# define dispatch dictionary
DISPATCH = {
    "GET": getData,
    "POST": postData,
    "PUT": putData,
    "DELETE": delData,
}



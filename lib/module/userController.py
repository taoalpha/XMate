#!/usr/bin/python

# define the profile update for post
def putData(request,res,db):
    '''
        Desc:
            Put to update user attributes
        Args:
            request: with all information, may only use request.form
            res: status after updating
            db: a reference to db
        Return:
            res
    '''
    data = FIELDS
    for key in request.form:
        data[key] = request.form[key]

    res = db.updateData("user",[res["_id"]],[data])

    return res

# define the getData function
def getData(request,res,db):
    '''
        Desc:
            fetch all data about the user
        Args:
            request: request with different data
            res: result that we need to update and return
        Err with status:
            0. no match
            1. normal
            2. other err, see msg
    '''
    data = [res["_id"]]

    docs = db.getData("user",data)

    # error handler for getting data
    return docs

# define the profile update for post
def postData(request,res,db):
    '''
        Desc:
            Post to create a new user
        Args:
            request: with all information, may only use request.form
            res: result stores mainly created uid
            db: a reference to db
        Return:
            uid: ObjectId
    '''
    # store requested form
    data = FIELDS
    for key in request.form:
        data[key] = request.form[key]

    # convert uid to int, can be deleted later(we don't need uid, use ObjectId instead)
    res = db.insertData("user",[data])
    print "########"
    print res

    # deal with inserting error
    return res

def delData(request,res,db):
    '''
        Desc:
            fetch all data about the user
        Args:
            request: request with different data
            res: result that we need to update and return
        Err:
            1. invalid objectId
            2. fail to delete data
    '''

    res = db.removeData("user",[res["_id"]])

    return res

# define dispatch dictionary
DISPATCH = {
    "GET": getData,
    "POST": postData,
    "PUT": putData,
    "DELETE": delData,
}

FIELDS = {
    "_id" : "",
    "username" : "",
    "age" : "",
    "gender" : "",
    "preferred_gender" : "",
    "city": "",
    "credits" : "",
    "latitude" : "",
    "longitude" : "",
    "last_time_login" : "",
    "height" : "",
    "weight" : "",
    "schedule_list" : [],
    "conflict_list" : [],
    "history_events" : [],
    "unprocessed_message" : [],
    "total_hours":0,
    "total_time":0,
    "total_activities":0
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
    res["_id"] = uid

    # content stores all validate information
    res["content"] = {}

    # set to 1 by default
    res["status"] = 1

    # forbid deleting users from the http request
    if request.method == "DELETE":
	res["status"] = 4
	res["msg"] = "Forbidden operation!!"
	return res

    # dispatch with method: GET/POST/PUT/DELETE
    res = DISPATCH[request.method](request,res,db)

    if res["status"] != 1:
	return res

    # if any err, return with err status
    return res["content"][0]

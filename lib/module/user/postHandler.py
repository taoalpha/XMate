#!/usr/bin/python

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
            "history_partner" : [],
            "history_events" : [],
            "unprocessed_message" : [],
    }
    # store requested form
    data = FIELDS
    for key in request.form:
        data[key] = request.form[key]

    # convert uid to int, can be deleted later(we don't need uid, use ObjectId instead)
    res = db.insertData("user",[data])

    # deal with inserting error
    return res

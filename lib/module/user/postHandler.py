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

    # store requested form
    data = {}
    for key in request.form:
        data[key] = request.form[key]

    # convert uid to int, can be deleted later(we don't need uid, use ObjectId instead)
    data["uid"] = int(data["uid"])
    docs = db.insertData(data)

    # store the return from inserting into res
    res["err"] = docs

    # deal with inserting error
    if docs["status"] == 1:
        return res

    # store the ObjectId to _id
    res["content"]["_id"] = str(docs["content"].inserted_id)
    return res

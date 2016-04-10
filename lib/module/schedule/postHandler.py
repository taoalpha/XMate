from bson.objectid import ObjectId

# define the profile update for post
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

    # if request.form is a validate dictionary, may ignore this part
    data = {}
    for key in request.form:
        data[key] = request.form[key]

    # TODO: remove this part, will use objectId as the identifier
    data["sid"] = int(data["sid"])

    docs = db.insertData(data)

    # catch the err of inserting
    if docs["status"]:
        res["err"] = docs
        return res

    # return the objectId of this schedule we just created
    res["content"]["_id"] = str(docs["content"].inserted_id)
    return res

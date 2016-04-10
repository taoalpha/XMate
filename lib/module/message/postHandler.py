
FIELDS = {
    "profile": ["username","age","gender","preferred","address"],
    "schedule": ["schedule_list"],
    "DELETE": ["_id"],
    "history": ["history_events","history_partner"],
    "stats": ["rate","lasttime_login","credits"],
    "message": ["unprocessed_message"]
}

# define the profile update for post
def postData(request,res,db):
    data = {}
    for key in request.form:
        data[key] = request.form[key]
    # print data
    docs = db.insertData(data)
    # print docs
    res["err"] = docs

    #FIXME: change uid to object ID
    res["content"]["_id"] = str(docs["content"].inserted_id)
    return res

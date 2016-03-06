from ...db_module.userModule import CUser

db_model = CUser()
connection = db_model.buildConnection()

FIELDS = {
    "profile": ["username","age","gender","preferred","address"],
    "schedule": ["schedule_list"],
    "DELETE": ["_id"],
    "history": ["history_events","history_partner"],
    "stats": ["rate","lasttime_login","credits"],
    "message": ["unprocessed_message"]
}

# define the profile update for post
def postData(request,res):
    if connection["status"]:
        res["content"]["status"] = "successful"
        return res

    data = {}
    for key in request.form:
        data[key] = request.form[key]
    data["uid"] = int(data["uid"])
    docs = db_model.insertData(data)
    res["err"] = docs

    #FIXME: change uid to object ID
    res["content"]["_id"] = str(docs["content"].inserted_id)
    return res

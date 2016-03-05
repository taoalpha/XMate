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

    data = request.form
    docs = db_model.insertData(data)
    res["content"]["status"] = docs["status"]
    res["content"]["uid"] = docs["uid"]
    return res

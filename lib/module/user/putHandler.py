from bson.objectid import ObjectId
FIELDS = {
    "profile": ["username","age","gender","preferred","address"],
    "schedule": ["schedule_list"],
    "DELETE": ["_id"],
    "history": ["history_events","history_partner"],
    "stats": ["rate","lasttime_login","credits"],
    "message": ["unprocessed_message"]
}

# define the profile update for post
def putData(request,res,db):
    #if connection["status"]:
    #    res["content"]["status"] = "successful"
    #    return res

    if not ObjectId.is_valid(res["uid"]):
        #res["err"]["status"] = 1
        #res["err"]["msg"] = "wrong id"
        #return res
        match_data = {"uid":int(res["uid"])}
    else:
        match_data = {"_id":ObjectId(res["uid"])}

    data = request.form
    docs = db.updateData(match_data,data)
    res["content"]["status"] = docs["status"]
    return res

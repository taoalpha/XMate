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

    if not ObjectId.is_valid(res["sid"]):
        #res["err"]["status"] = 1
        #res["err"]["msg"] = "wrong id"
        #return res
        match_data = {"sid":int(res["sid"])}
    else:
        match_data = {"_id":ObjectId(res["sid"])}


    data = request.form
    docs = db.updateData(match_data,data)
    res["content"]["status"] = docs["status"]
    return res

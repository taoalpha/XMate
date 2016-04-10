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
    match_data = {"mid":int(res["mid"])}
    data = request.form
    docs = db.updateData(match_data,data)
    res["content"]["status"] = docs["status"]
    return res

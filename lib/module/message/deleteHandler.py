FIELDS = {
    "profile": ["username","age","gender","preferred","address"],
    "schedule": ["schedule_list"],
    "DELETE": ["_id"],
    "history": ["history_events","history_partner"],
    "stats": ["rate","lasttime_login","credits"],
    "message": ["unprocessed_message"]
}

# define the getAll function
def delData(request,res,db):
    '''
        Desc:
            fetch all data about the user
        Args:
            request: request with different data
            res: result that we need to update and return
        Err:
            1. connection err
            2. invalid objectId
            3. fail to delete data
    '''
    # error handler for invalid objectid
    data = {"_id":res["mid"]}

    # data = {"sid":{"$in":schedule_list}}
    docs = db.removeData(data)

    # error handler for getting data
    if docs["status"]:
        res["err"] = docs
        return res

    #
    # normal process
    #
    return res

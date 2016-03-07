from bson.objectid import ObjectId

# define the delete function
def delData(request,res,db):
    '''
        Desc:
            delete the schedule exercise by id
        Args:
            request: maybe useful
            res: id stores in res["sid"], and update res with proper information
        Err:
            1. invalid objectId
            2. fail to delete data
    '''

    # error handler for invalid objectid
    if not ObjectId.is_valid(res["sid"]):
        res["err"]["status"] = 1
        res["err"]["msg"] = "wrong id"
        return res

    data = {"_id":ObjectId(res["sid"])}

    # data = {"sid":{"$in":schedule_list}}
    docs = db.removeData(data)

    # error handler for getting data
    if docs["status"]:
        res["err"] = docs
        return res

    #
    # normal process
    #
    res["content"]["status"] = "successful"
    return res

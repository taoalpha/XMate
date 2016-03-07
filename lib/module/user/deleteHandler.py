from bson.objectid import ObjectId

# define the getAll function
def delData(request,res,db):
    '''
        Desc:
            fetch all data about the user
        Args:
            request: request with different data
            res: result that we need to update and return
        Err:
            1. invalid objectId
            2. fail to delete data
    '''

    # error handler for invalid objectid
    if not ObjectId.is_valid(res["uid"]):
        res["err"]["status"] = 1
        res["err"]["msg"] = "wrong id"
        return res

    data = {"_id":ObjectId(res["uid"])}

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

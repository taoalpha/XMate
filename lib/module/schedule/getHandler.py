from bson.objectid import ObjectId

FIELDS = {
    "profile": ["username","age","gender","preferred","address"],
    #"profile": ["username","age","gender","preferred","address","height","width","avatar"],
    "schedule": ["schedule_list"],
    "DELETE": ["_id"],
    "history": ["history_events","history_partner"],
    "stats": ["rate","lasttime_login","credits"],
    "message": ["unprocessed_message"]
}

# define the getAll function
def getData(request,res,db):
    '''
        Desc:
            fetch all data about the user
        Args:
            request: request with different data
            res: result that we need to update and return
        Err:
            1. connection err
            2. invalid objectId
            3. fail to get data
            4. no match result
    '''

    # error handler for connection
    #if connection["status"]:
    #    res["err"]["status"] = 1
    #    res["err"]["msg"] = "fail to connect"
    #    return res

    # error handler for invalid objectid
    if not ObjectId.is_valid(res["sid"]):
        #res["err"]["status"] = 1
        #res["err"]["msg"] = "wrong id"
        #return res
        data = {"sid":int(res["sid"])}
    else:
        data = {"_id":ObjectId(res["sid"])}

    # data = {"sid":{"$in":schedule_list}}
    docs = db.getData(data)

    # error handler for getting data
    if docs["status"]:
        res["err"] = docs
        return res

    # error handler for no match result
    if docs["content"].count() == 0:
        res["err"]["status"] = 1
        res["err"]["msg"] = "no matches"
        return res


    #
    # normal process
    #

    for doc in docs["content"]:
        for i,key in enumerate(FIELDS["DELETE"]):
            # remove all non-neccessary fields
            # del doc[key]
            doc[key] = str(doc[key])
        if docs["content"].count() > 1:
            res["rawdata"]["entries"] = []
            res["rawdata"]["entries"].append(doc)
        else:
            res["rawdata"] = doc
    return res

# define the filterData function
def filterData(request,res):
    '''
        Desc:
            Filter data with field parameter
        Args:
            request : request object
            res : result needs to return
    '''
    if res["field"] == None:
        res["content"] = res["rawdata"]
        return res
    else:
        for i,field in enumerate(FIELDS[res["field"]]):
            res["content"][field] = res["rawdata"][field]
        return res

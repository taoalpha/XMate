#!/usr/bin/python
from bson.objectid import ObjectId

# define all combination of attributes contained in each field
FIELDS = {
    "profile": ["username","age","gender","preferred","address"],
    #"profile": ["username","age","gender","preferred","address","height","width","avatar"],
    "schedule": ["schedule_list"],
    "DELETE": ["_id"],
    "history": ["history_events","history_partner"],
    "stats": ["rate","lasttime_login","credits"],
    "message": ["unprocessed_message"]
}

# define the getData function
def getData(request,res,db):
    '''
        Desc:
            fetch all data about the user
        Args:
            request: request with different data
            res: result that we need to update and return
        Err:
            1. invalid objectId
            2. fail to get data
            3. no match result
    '''
    # error handler for invalid objectid
    if not ObjectId.is_valid(res["uid"]):
        #res["err"]["status"] = 1
        #res["err"]["msg"] = "wrong id"
        #return res
        data = {"uid":int(res["uid"])}
    else:
        data = {"_id":ObjectId(res["uid"])}

    # data = {"sid":{"$in":schedule_list}}
    # get the data based on uid
    # docs:
    #   status: success or not
    #   content: cursor contains the result
    docs = db.getData(data)

    # error handler for getting data
    # return early
    if docs["status"]:
        res["err"] = docs
        return res

    # error handler for no match result
    # return early
    if docs["content"].count() == 0:
        res["err"]["status"] = 1
        res["err"]["msg"] = "no matches"
        return res

    #
    # normal process
    #
    for doc in docs["content"]:
        #for i,key in enumerate(FIELDS["DELETE"]):
            # remove all non-neccessary fields
        # convert objectId to string for jsonify
        doc["_id"] = str(doc["_id"])

        # just in case we have multiple matches (should not happen for uid search)
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

    # double check the res["field"], if no need to filter, return
    if res["field"] == None:
        res["content"] = res["rawdata"]
        return res
    else:
        # return attributes based on pre-defined FIELDS
        for i,field in enumerate(FIELDS[res["field"]]):
            res["content"][field] = res["rawdata"][field]
        return res

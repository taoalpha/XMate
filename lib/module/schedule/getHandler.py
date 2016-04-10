from bson.objectid import ObjectId
from ...db_module import computematch as CM

# define the getData function
def getData(request,res,db):
    '''
        Desc:
            fetch all data about the schedule
        Args:
            request: request with different data
            res: result that we need to update and return
        Err:
            1. invalid objectId
            2. fail to get data
            3. no match result
    '''
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

    res["err"]["status"] = 0

    for doc in docs["content"]:
        doc["_id"] = str(doc["_id"])
        if docs["content"].count() > 1:
            res["rawdata"]["entries"] = []
            res["rawdata"]["entries"].append(doc)
        else:
            res["rawdata"] = doc
    return res

# define the filterData function
def filterData(request,res,db):
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
    elif res["field"] == "search":
        # call search function to get search results
        # search happens when no sid but field = search
        # all parameters should pass in by request.form
        res["content"]["entries"] = []
        res["content"]["entries"] = CM.giveSearchResult(10,res["rawdata"],db)
        return res
    elif res["field"] == "match":
        # call match function to get match results
        # match happens when there is a sid and field = match
        res["content"]["entries"] = []
        res["content"]["entries"] = CM.computeMatchPosts(10,res["rawdata"],db)
        print(len(res["content"]["entries"]))
        return res

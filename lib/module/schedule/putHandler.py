from bson.objectid import ObjectId

# define the update for post
def putData(request,res,db):
    '''
        Desc:
            update some fields of a schedule exercise
        Args:
            request: store the updated information of exercise within request.form
            db: referrence to db object
            res: store the status
        Err:
            1. fail to update data
    '''


    if not ObjectId.is_valid(res["sid"]):
        #res["err"]["status"] = 1
        #res["err"]["msg"] = "wrong id"
        #return res
        match_data = {"sid":int(res["sid"])}
    else:
        match_data = {"_id":ObjectId(res["sid"])}

    docs = db.updateData(match_data,request.form)

    # catch the error of updating
    if docs["status"]:
        res["err"] = docs
        return res

    # return the status
    res["content"]["status"] = docs["status"]

    return res

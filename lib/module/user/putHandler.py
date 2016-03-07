#!/usr/bin/python

from bson.objectid import ObjectId

# define the profile update for post
def putData(request,res,db):
    '''
        Desc:
            Put to update user attributes
        Args:
            request: with all information, may only use request.form
            res: status after updating
            db: a reference to db
        Return:
            res
    '''
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

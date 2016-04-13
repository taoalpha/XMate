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

    res = db.removeData("type",[res["_id"]])

    return res

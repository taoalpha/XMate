#!/usr/bin/python

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

    res = db.updateData("user",[res["_id"]],[data])

    return res

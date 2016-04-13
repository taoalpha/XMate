#!/usr/bin/python
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
        Err with status:
            0. no match
            1. normal
            2. other err, see msg
    '''
    data = [res["_id"]]

    docs = db.getData(type,data)

    # error handler for getting data
    return docs

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

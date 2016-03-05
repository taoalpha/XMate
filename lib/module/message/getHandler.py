from ...db_module.userModule import CUser

db_model = CUser()
connection = db_model.buildConnection()

FIELDS = {
    "profile": ["username","age","gender","preferred","height","weight"],
    "schedules": ["schedule_list"],
    "test": ["name","gender"],
    "DELETE": ["_id"],
    "messages": ["unprocessed_message"]
}

# define the getAll function
def getData(request,res):
    '''
        Desc:
            fetch all data about the user
        Args:
            request: request with different data
            res: result that we need to update and return
    '''
    if connection["status"]:
        res["status"] = "fail"
        return res

    data = {"uid":res["uid"]}
    #data = {"sid":{"$in":schedule_list}}
    docs = db_model.getData(data)
    for doc in docs["content"]:
        for i,key in enumerate(FIELDS["DELETE"]):
            # remove all non-neccessary fields
            del doc[key]
        res["rawdata"] = doc
    return res

# define the filterData function
def filterData(request,res):
    if res["action"] == None:
        res["content"] = res["rawdata"]
        return res
    else:
        for i,field in enumerate(FIELDS[res["action"]]):
            res["content"][field] = res["rawdata"][field]
        return res

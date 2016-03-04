# Dispatch function for user api
import module.getHandler as getHandler
import module.postHandler as postHandler
import module.putHandler as putHandler
import module.deleteHandler as deleteHandler

# define dispatch dictionary
DISPATCH = {
    "GET":{
        "all" : getHandler.allIn,
        "profile" : getHandler.userProfile,
        "messages" : getHandler.userMessage,
        "histories" : getHandler.userHistory,
        "schedules" : getHandler.userSchedule,
        "stats" : getHandler.userStats,
    },
    "POST":{
        "all" : postHandler.allIn,
        "profile" : postHandler.userProfile
    },
    "PUT":{
    },
    "DELETE":{
    },
    "PATCH":{
    }
}

def userDispatch(uid,action,request):
    res = {}
    DISPATCH[request.method][action](request,res)
    # TODO: filter res with args
    return res

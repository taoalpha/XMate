# define the getAll function
def allIn(request,res):
    res["profile"] = userProfile(request)
    res["message"] = userMessage(request)
    res["history"] = userHistory(request)
    res["schedule"] = userSchedule(request)
    res["stats"] = userStats(request)
    return res

# define the getUserProfile function
def userProfile(request,res=None):
    # get all data field of user from mongo
    # res = {}
    # TODO: use user model
    if res != None:
        res["profile"] = {
            "username": "TaoAlpha",
            "address": "Ithaca",
            "phone": "9196275224",
            "prefer": "Female",
            "avatar": "https://scontent-yyz1-1.xx.fbcdn.net/hphotos-xpt1/v/t1.0-9/12241195_723467147784895_9035525538091629756_n.jpg?oh=224f93fe9f15339905eb1c7f68eea118&oe=5762291D",
        }
    else:
        res = {
            "username": "TaoAlpha",
            "address": "Ithaca",
            "phone": "9196275224",
            "prefer": "Female",
            "avatar": "https://scontent-yyz1-1.xx.fbcdn.net/hphotos-xpt1/v/t1.0-9/12241195_723467147784895_9035525538091629756_n.jpg?oh=224f93fe9f15339905eb1c7f68eea118&oe=5762291D",
        }
    return res

# define the getUserMessage function
def userMessage(request,res=None):
    if res != None:
        res["message"] = {
            "msg": "Hi",
            "createTime": "2016/02/29 12:00:00"
        }
    else:
        res = {
            "msg": "Hi",
            "createTime": "2016/02/29 12:00:00"
        }
    return res

# define the getUserHistory function
def userHistory(request,res=None):
    if res != None:
        res["schedule"] = {
            "prefer": "Female",
            "avatar": "https://scontent-yyz1-1.xx.fbcdn.net/hphotos-xpt1/v/t1.0-9/12241195_723467147784895_9035525538091629756_n.jpg?oh=224f93fe9f15339905eb1c7f68eea118&oe=5762291D",
        }
    else:
        res = {
            "prefer": "Female",
            "avatar": "https://scontent-yyz1-1.xx.fbcdn.net/hphotos-xpt1/v/t1.0-9/12241195_723467147784895_9035525538091629756_n.jpg?oh=224f93fe9f15339905eb1c7f68eea118&oe=5762291D",
        }
    return res

# define the getUserSchedule function
def userSchedule(request,res=None):
    if res != None:
        res["schedule"] = {
            "schedules": [1,3,5,6,2,1]
        }
    else:
        res = {
            "schedules": [1,3,5,6,2,1]
        }
    return res

# define the getUserStats function
def userStats(request,res=None):
    if res != None:
        res["stats"] = {
            "stats": [12,13,14,15]
        }
    else:
        res = {
            "stats": [12,13,14,15]
        }
    return res

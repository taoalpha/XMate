import sys, random, time, hashlib
import moment
from geopy.distance import vincenty

def getHash(post_content):
    
    strhash = ""
    strhash += str(post_content["type"])
    
    st = moment.unix(post_content["start_time"])
    strhash += str(st.month) + str(st.day) 

    if(post_content["latitude"] == ""):
        pass
    else:
        lat = '{:.1f}'.format(post_content["latitude"])
        lon = '{:.1f}'.format(post_content["longitude"])
        strhash += str(lat) + str(lon)


    return hashlib.md5(strhash).hexdigest()

def Judge(type,cache_return):
    t = cache_return["create_time"]
    current_time = moment.now().epoch()

    threshold = 3600
    if(type == "post"):
        threshold = 7200

    if(t < current_time - threshold):
        return True
    else:
        return False


def computeMatchPosts(post_content, mydb):

    dis_threshold = 9.0
    docu_list = []
    oodflag = 0

    #if the search has already been cached, return it
    search_id = getHash(post_content)
    id_list = []
    id_list.append(search_id)
    res = mydb.getData("cache",id_list)
    if(res["status"] != 0):
        if(res["status"] == 1):
            outofdate = Judge("post",res["content"][0])
            if(outofdate):
                oodflag = 1
                pass
            else:
                return returnHelper(content = res["content"][0]["match_list"])
        else:
            return res
   
    id_list = []
    res = mydb.getData("schedule",id_list)
    if(res["status"] != 1):
        return res
    cursor = res["content"]

    f1 = True
    f2 = True
    if(post_content["start_time"] == ""):
        f1 = False
    if(post_content["latitude"] == ""):
        f2 = False

    print "######"
    #Find the match document list
    for doc in cursor:

        flag = True
        current_time = moment.now().epoch()
        if(doc["start_time"] < current_time):
            continue

        if(post_content["type"] == "" or post_content["type"] == doc["type"]):
            if(post_content["start_time"] == ""):
                pass
            else:
                st = moment.unix(post_content["start_time"])
                nst = moment.date(st.year, st.month, st.day, 0).epoch()
                
                if(doc["start_time"] > nst - 86400 and doc["start_time"] < nst + 86400*1.5):
                    doc["time_diff"] = abs(doc["start_time"] - post_content["start_time"])
                else:
                    flag = False
        else:
            flag = False

        if(flag):
	    print doc
            if(post_content["latitude"] == ""):
                pass
            else:
                pointa = (doc["latitude"],doc["longitude"])
                pointb = (post_content["latitude"],post_content["longitude"])
                dist = vincenty(pointa, pointb).miles
                if(dist < dis_threshold):
                    doc["diff"] = dist
                else:
                    flag = False

        if(flag):
            docu_list.append(doc)
    

    if(f1 and f2):
        docu_list.sort(key = lambda postd: (postd["time_diff"],postd["diff"]))
    elif(f1 == False):
        if(f2):
            docu_list.sort(key = lambda postd: postd["diff"]) 
        else:
            docu_list.sort(key = lambda postd: postd["post_datetime"],reverse = True) 
    else:
        docu_list.sort(key = lambda postd: postd["time_diff"])

    #Insert the data into the cache
    current_time = moment.now().epoch()

    data_list = []
    data = {"_id":search_id, "match_list":docu_list, "create_time":current_time}
    data_list.append(data)
    
    if(oodflag == 0):
        res = mydb.insertData("cache",data_list)
        if(res["status"] != 1):
            return res
    else:
        id_list = [search_id]
        res = mydb.updateData("cache",id_list,data_list)
        if(res["status"] != 1):
            return res

    return returnHelper(content = docu_list)



def computeMatchUsers(uid, pid, mydb):

    oodflag = 0 #out of date flag

    #Check whether the same match has been in cache
    strhash = str(uid)+str(pid)
    match_id = hashlib.md5(strhash).hexdigest()
    id_list = []
    id_list.append(match_id)
    res = mydb.getData("cache",id_list)

    if(res["status"] != 0):
        if(res["status"] == 1):
            outofdate = Judge("user",res["content"][0])
            if(outofdate):
                oodflag = 1
                pass
            else:
                return returnHelper(content = res["content"][0]["match_list"])
        else:
            return res

    recommend_user_list1 = set()
    recommend_user_list2 = set()
    #compute from schedule list
    id_list = [pid]
    res = mydb.getData("schedule",id_list)

    if(res["status"] != 1):
        return res
    mpost = res["content"][0]

    id_list = [uid]
    res = mydb.getData("user",id_list)
    if(res["status"] != 1):
        return res
    history_events_list = res["content"][0]["history_events"]


    id_list = []
    res = mydb.getData("schedule",id_list)
    if(res["status"] != 1):
        return res
    cursor = res["content"]

    for doc in cursor:
        if(doc["type"] == mpost["type"]):
            if(doc["owner"] in history_events_list):
                recommend_user_list1.add(doc["owner"])
            else:
                recommend_user_list2.add(doc["owner"])

            for user_id in doc["member"]:
                if(user_id in history_events_list):
                    recommend_user_list1.add(user_id)
                else:
                    recommend_user_list2.add(user_id)

    recommend_user_list = list(recommend_user_list1) + list(recommend_user_list2)
    
    #if recommendation set size is too small, give some random results
    if(len(recommend_user_list) < 5):
        id_list = []
        res = mydb.getData("user",id_list)
        if(res["status"] != 1):
            return res
        cursor = list(res["content"])
        tmplist = random.sample(cursor,5)
        ranlist = []

        for doc in tmplist:
            if(doc["_id"] not in recommend_user_list):
            	ranlist.append(doc["_id"])
        recommend_user_list += ranlist

    #get the user name from the recommended list
    r_list = []
    for i in range(0, len(recommend_user_list)):
        data = {"_id":recommend_user_list[i]}
        r_list.append(data)
    
    id_list = recommend_user_list
    res = mydb.getData("user",id_list)

    if(res["status"] != 1):
        return res
    
    cursor = res["content"]
    for doc in cursor:
        pos = recommend_user_list.index(doc["_id"])
        r_list[pos]["username"] = doc["username"]

    #insert or update data into cache
    current_time = moment.now().epoch()
    data_list = []
    data = {"_id":match_id, "match_list":r_list, "create_time":current_time}
    data_list.append(data)

    if(oodflag == 0):
	print "a"
        res = mydb.insertData("cache",data_list)
	print res
        if(res["status"] != 1):
            return res
    else:
        id_list = [match_id]
        res = mydb.updateData("cache",id_list,data_list)
        if(res["status"] != 1):
            return res

    return returnHelper(content = r_list)


def returnHelper(status = 1, msg = None,content = None):
    return_val = {}
    return_val["status"] = status
    return_val["msg"] = msg
    return_val["content"] = content

    return return_val





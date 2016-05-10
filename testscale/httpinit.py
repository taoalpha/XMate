import random, string, requests, moment



U_FIELD = {
    "_id" : "",
    "username" : "",
    "age" : "",
    "gender" : "",
    "preferred_gender" : "",
    "city": "",
    "credits" : "",
    "latitude" : "",
    "longitude" : "",
    "last_time_login" : "",
    "height" : "",
    "weight" : "",
    "schedule_list" : [],
    "conflict_list" : [],
    "history_partner" : [],
    "history_events" : [],
    "unprocessed_message" : []
}

def generateUser(num):
    user = {}
    user["_id"] = str(num)+"tao"
    user["username"] = random.choice(string.ascii_uppercase)+''.join(random.choice(string.ascii_lowercase) for _ in range(7)) +  " " + random.choice(string.ascii_uppercase)+''.join(random.choice(string.ascii_lowercase) for _ in range(7))
    user["age"] = ''.join(random.choice(string.digits) for _ in range(2))
    user["gender"] = ["male", "female"][(random.random() > 0.5)]
    user["preferred_gender"] = ["male", "female"][(random.random() > 0.5)]
    user["city"] = ''.join(random.choice(string.ascii_uppercase) for _ in range(2))
    user["latitude"] = float(''.join(random.choice(string.digits) for _ in range(5))) / 1000
    user["longitude"] = float(''.join(random.choice(string.digits) for _ in range(5))) / 1000
    user["height"] = int(''.join(random.choice(string.digits) for _ in range(3))) % 180
    user["weight"] = ''.join(random.choice(string.digits) for _ in range(2))
    user["credits"] = int(random.random()*100)
    # < 10 days to now
    user["last_time_login"] = moment.now().epoch() - int(random.random()*86400*10)
    for i in U_FIELD:
        if i not in user:
            user[i] = U_FIELD[i]
    return user


para_list = []
for i in range(0,1000):
    para = generateUser(i)
    para_list.append(para)
post_url = "http://192.168.99.100:4000/user/"

for i in range(0,1000):
    #r = requests.put(post_url+para_list[i]["_id"],para_list[i])
    r = requests.post(post_url, para_list[i])
    #print r.status_code
    if(r.status_code != 200 or "status" in r.json()):
        print i
    
print "###################"
print "Finish initliaize"





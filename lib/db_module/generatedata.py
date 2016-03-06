import string, random, sys
from userModule import CUser

def str_generator(size, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def getrandomlist(size, array_len):
    num = random.randrange(0,array_len)
    tmpset = {num}
    while len(tmpset) < max(1,size):
        tmpset.add(random.randrange(0,array_len))
    tmpset = list(tmpset)
    return tmpset

mystr = 'abcdefghijklmnopqrstuvwxyz'
myid = '1234567890abcdef'

#userSet:2000, scheduleSet:2000, historySet:2000
#msgSet = generate_randomlist(1000, 10, myid)
userdocu_list = [{} for x in range(2000)]
postmemeber_list = [[] for x in range(2000)]
hpostmember_list = [[] for x in range(2000)]


def generate_userdocu():

    for i in range(0, 2000):
        userdocu_list[i]['uid'] = i
        userdocu_list[i]['username'] = str_generator(8,mystr)
        userdocu_list[i]['age'] = random.randrange(15,50)

        if random.randrange(0,2) == 0:
            userdocu_list[i]['gender'] = 'male'
        else:
            userdocu_list[i]['gender'] = 'female'

        userdocu_list[i]['preferred'] = {}
        if random.randrange(0,2) == 0:
            userdocu_list[i]['preferred']['gender'] = 'male'
        else:
            userdocu_list[i]['preferred']['gender'] = 'female'
        userdocu_list[i]['preferred']['ages'] = random.randrange(15,40)
        userdocu_list[i]['preferred']['agee'] = min(userdocu_list[i]['preferred']['ages'] + 15, 50)

        userdocu_list[i]['address'] = {}
        userdocu_list[i]['address']['city'] = 'Ithaca'
        userdocu_list[i]['rate'] = random.randrange(1,6)
        userdocu_list[i]['credits'] = random.randrange(10,200)
        userdocu_list[i]['lasttime_login'] = None

        userdocu_list[i]['schedule_list'] = []
        userdocu_list[i]['history_events'] = []
        userdocu_list[i]['history_partner'] = []

        listsize = random.randrange(0,5)
        userdocu_list[i]['schedule_list'] = getrandomlist(listsize, 2000)
        
        for j in range(0, len(userdocu_list[i]['schedule_list'])):
            postmemeber_list[userdocu_list[i]['schedule_list'][j]].append(i)

        listsize = random.randrange(2,5)
        userdocu_list[i]['history_events'] = getrandomlist(listsize, 2000)
        #print(hpostmember_list[0])
        for j in range(0, len(userdocu_list[i]['history_events'])):
            # print(userdocu_list[i]['history_events'][j])
            hpostmember_list[ userdocu_list[i]['history_events'][j] ].append(i)
        # print(hpostmember_list[0])
        
        userdocu_list[i]['unprocessed_message'] = []





usercoll = CUser()
res = usercoll.buildConnection()
if(res['status']):
     print(res)

generate_userdocu()

for i in range(0,2000):
    for j in range(0, len(hpostmember_list[i])-1):
        # print(len(hpostmember_list[i]))
        for k in range(j+1,len(hpostmember_list[i])):
            # print(str(i)+"-"+str(j)+"-"+str(k))
            userdocu_list[hpostmember_list[i][j]]['history_partner'].append(hpostmember_list[i][k])
            userdocu_list[hpostmember_list[i][k]]['history_partner'].append(hpostmember_list[i][j])

#print(userdocu_list[0])

res = usercoll.insertManyData(userdocu_list)
if(res['status']):
    print(res)
print(usercoll.collection.count())






























    


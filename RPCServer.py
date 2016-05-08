from System import Action
import clr
clr.AddReference('Vsync') # The profile of the dll file.
import Vsync
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import json

#from threading import Thread

Vsync.VsyncSystem.Start()


# define RequestHandler
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# define the server for later use
server = SimpleXMLRPCServer(("localhost", 8000),requestHandler=RequestHandler)
server.register_introspection_functions()

group = Vsync.Group("Master")

print "Created Master group"
users = {}
schedules = {}
messages = {}
cache = {}


'''
global
'''
def backup():
    '''
        backup data.
    '''
    dataset = {}
    dataset["user"] = users
    dataset["schedule"] = schedules
    dataset["message"] = messages
    dataset["cache"] = cache

    with open('data.json', 'w') as outfile:
        json.dump(dataset, outfile)

    del dataset

"""
    User DHT
"""
def postUserData_api(id, profile):
	"""
            Forward user POST to vsync
            @param {string} id - user id
            @param {string} profile - stringified user profile
	"""
        # delegate to vsync
	group.Send(0, id, profile)

	return "profile" # just for flask

def postUserData(id, profile):
        '''
            add a profile with id to the users DHT.
            @param {string} id - user id
            @param {string} profile - stringified user profile
        '''
	users[id] = profile
        backup()

        # for debugging
        if profile == "-1":
            print "Delete the user with id :"+id
        else:
            print "Add the user with id :"+id

def getUserData_api(id):
	"""
            Forward user GET to vsync
            @param {string} id - user id
            @return {string} - either return the profile content or -1 for not found / deleted
	"""
	if id in users and users[id] != "-1":
		return users[id]
	return "-1"

def getUserData(id):
        '''
            get a user profile from the user DHT with the given id.
            @param {string} id - user id
        '''
	if id in users:
		group.Reply(users[id])
	else:
		group.Reply(-1)
        print("Get user with id :" + id)

def removeUserData_api(id):
	"""
            Forward user DELETE to vsync
            @param {string} id - user id
	"""
        # delegate to vsync post
	group.Send(0, id, '-1')
	return "profile" # just for flask


"""
Message DHT
"""
def postMessageData_api(id, message):
	"""
            Forward a message POST to vsync.
            @param {string} id - message id
            @param {string} message - message content
	"""
        # delegate to vsync
	group.Send(3, id, message)
	return "message" # just for flask

def postMessageData(id, message):
        '''
            Add a message to message DHT with a id.
            @param {string} id - message id
            @param {string} message - message content
        '''

	messages[id] = message
        backup()
        # for debugging
        if message == "-1":
            print "Delete the message with id :"+id
        else:
            print "Add the message with id :"+id

def getMessageData_api(id):
	"""
            Forward message GET to vsync.
            @param {string} id - message id
            @return {string} - either return the message content or -1 for not found / deleted
	"""
	if id in messages and messages[id] != "-1":
		return messages[id]
	return "-1"

def getMessageData(id):
        '''
            get a message from the message DHT with the given id.
            @param {string} id - message id
        '''
	if id in messages:
		group.Reply(messages[id])
	else:
		group.Reply(-1)
	print("Vsync server getMessageData with id=" + id.ToString())

def removeMessageData_api(id):
	"""
            Forward message DELETE to user.
            @param {string} id - message id
	"""
	group.Send(3, id, '-1')
	return "message" # just for flask


"""
    Schedule DHT
"""
def postScheduleData_api(id, schedule):
	"""
            Forward schedule POST to vsync
            @param {string} id - schedule id
            @param {string} schedule - schedule content
	"""
	group.Send(6, id, schedule)
	return "schedule" # just for flask


def postScheduleData(id, schedule):
        '''
            add a schedule with id to the schedule DHT.
            @param {string} id - schedule id
            @param {string} schedule - schedule content
        '''
        # for debugging
        if schedule == "-1":
            print "Delete the schedule with id :"+id
        else:
            print "Add the schedule with id :"+id

	schedules[id] = schedule
        backup()

def getScheduleData_api(id):
	"""
            Forward schedule GET to vsync
            @param {string} id - schedule id
            @return {string} - either return schedule content or -1 if not found / deleted
	"""
	if id in schedules and schedules[id] != "-1":
		return schedules[id]
	return "-1"

def getScheduleData(id):
        '''
            get a schedule from the schedule DHT with the given id.
            @param {string} id - schedule id
        '''
	if id in schedules:
		group.Reply(schedules[id])
	else:
		group.Reply(-1)
	print("Vsync server getScheduleData with id=" + id.ToString())

def removeScheduleData_api(id):
	"""
            Forward schedule DELETE to vsync POST with content as -1.
            @param {string} id - schedule id
	"""
	group.Send(6, id, '-1')
	return "profile"

"""
    Cache DHT - Define cache collection (cache_id - '{time:"1231231212.123",id_list:"[]"}'
"""
def postCacheData_api(id, cache_content):
	"""
            Forward cache POST to vsync
            @param {string} id - cache id
            @param {string} cache - cache content
	"""
        # delegate to vsync
	group.Send(9, id, cache_content)
        # just for flask
	return "cache"


def postCacheData(id, cache_content):
        '''
            add a cache to Cache DHT with given id.
            @param {string} id - cache id
            @param {string} cache - cache content
        '''
	cache[id] = cache_content
        backup()
        # for debugging
        if cache_content == "-1":
            print "Delete the user with id :"+id
        else:
            print "Add the user with id :"+id


def getCacheData_api(id):
	"""
            Forward cache GET to vsync.
            @param {string} id - cache id
            @return {string} either return the found cache content or -1 represent not found / deleted
	"""
	res = []
	nr = group.Query(Vsync.Group.ALL, 10, id, Vsync.EOLMarker(), res)
	for ele in res:
		if (ele != -1):
			return ele
	return "-1"


def getCacheData(id):
        '''
            get a schedule from the schedule DHT with the given id.
            @param {string} id - cache id
        '''
	if id in cache:
		group.Reply(cache[id])
	else:
		group.Reply(-1)
	print("Vsync server get Cache with id=" + id.ToString())

def removeCacheData_api(id):
	"""
            Forward cache DELETE to vsync, remove the cache = set the value for this key(id) as [], empty list.
            @param {string} id - cache id
            @return {string} useless for now
	"""
        # delegate to vsync
	group.Send(9, id, '-1')
	return "cache"


# for retrieving all user / message / schedule
def getAllUsers_api():
	"""
            Retrieve all users, including all keys and values.
            @return {string} - return stringify content of users
	"""
        return json.dumps(users)

def getAllMessages_api():
	"""
            Retrieve all messages, including all keys and values.
            @return {string} - return stringify content of users
	"""
        return json.dumps(messages)

def getAllCache_api():
	"""
            Retrieve all cache, including all keys and values.
            @return {string} - return stringify content of users
	"""
        return json.dumps(cache)

def getAllSchedules_api():
	"""
            Retrieve all schedules including all keys and values.
            @return {string} - return stringify content of users
	"""
        return json.dumps(schedules)



### Vsycn register
def myViewFunc(v):
    print('New view: ' + v.ToString())
    print('My rank = ' + v.GetMyRank().ToString())
    for a in v.joiners:
        print('  Joining: ' + a.ToString() + ', isMyAddress='+a.isMyAddress().ToString())
    for a in v.leavers:
        print('  Leaving: ' + a.ToString() + ', isMyAddress='+a.isMyAddress().ToString())
    return



# All functions registered by rpc-server

# user related functions
server.register_function(postUserData_api,'postUserData')
server.register_function(getUserData_api, 'getUserData')
server.register_function(removeUserData_api,'removeUserData')
# schedule related functions
server.register_function(postScheduleData_api,'postScheduleData')
server.register_function(getScheduleData_api,'getScheduleData')
server.register_function(removeScheduleData_api,'removeScheduleData')
# message related functions
server.register_function(postMessageData_api,'postMessageData')
server.register_function(getMessageData_api,'getMessageData')
server.register_function(removeMessageData_api,'removeMessageData')
# cache related functions
server.register_function(postCacheData_api,'postCacheData')
server.register_function(getCacheData_api,'getCacheData')
server.register_function(removeCacheData_api,'removeCacheData')
# retrieve all
server.register_function(getAllUsers_api,'getAllUsers')
server.register_function(getAllSchedules_api,'getAllSchedules')
server.register_function(getAllMessages_api,'getAllMessages')
server.register_function(getAllCache_api,'getAllCache')
# view
server.register_function(myViewFunc,'myViewFunc')


# All functions registered by vsync

# user related functions
group.RegisterHandler(0, Action[str, str](postUserData))
# group.RegisterHandler(1, Action[str](getUserData))
# group.RegisterHandler(2, Action[str](removeUserData))

# message related functions
group.RegisterHandler(3, Action[str, str](postMessageData))
# group.RegisterHandler(4, Action[str](getMessageData))
# group.RegisterHandler(5, Action[str](removeMessageData))

# schedule related functions
group.RegisterHandler(6, Action[str, str](postScheduleData))
# group.RegisterHandler(7, Action[str](getScheduleData))
# group.RegisterHandler(8, Action[str](removeScheduleData))

# cache related functions
group.RegisterHandler(9, Action[str, str](postCacheData))
# group.RegisterHandler(10, Action[str](getCacheData))
# group.RegisterHandler(11, Action[str](removeCacheData))

# view
group.RegisterViewHandler(Vsync.ViewHandler(myViewFunc))

group.Join()

### run
server.serve_forever()
Vsync.VsyncSystem.WaitForever()

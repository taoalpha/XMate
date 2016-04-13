from System import Action
import clr
clr.AddReference('VsyncLib') # The profile of the dll file.
import Vsync

from threading import Thread

Vsync.VsyncSystem.Start()


from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

server = SimpleXMLRPCServer(("localhost", 8000),requestHandler=RequestHandler)
server.register_introspection_functions()

group = Vsync.Group("Master")
print "Created Master group"
users = {}
schedules = {}
messages = {}


""" User DHT
"""
def postUserData_api(id, profile):
	"""add a profile with id to the users DHT.
		id and profile are both string.
	"""
	group.Send(0, id, profile)
	return "profile" # just for flask
server.register_function(postUserData_api,'postUserData')

def postUserData(id, profile):
	users[id] = profile
	print("Vsync server postUserData with id=" + id.ToString())

def getUserData_api(id):
	"""get a user profile from the user DHT with the given id.
		id is a string, and the functions return a string unless no macthing found.
	"""
	res = []
	print(res)
	nr = group.Query(Vsync.Group.ALL, 1, id, Vsync.EOLMarker(), res)
	for ele in res:
		if (ele != -1):
			return ele
	return -1
server.register_function(getUserData_api, 'getUserData')

def getUserData(id):
	group.Reply(users[id])
	print("Vsync server getUserData with id=" + id.ToString())

def removeUserData_api(id):
	"""set a user profile to be "" in the user DHT with the given id.
		id is a string.
	"""
	group.Send(2, id)
	return "profile" # just for flask
server.register_function(removeUserData_api,'removeUserData')

def removeUserData(id):
	users[id] = ""
	print("Vsync server removeUserData with id=" + id.ToString())


""" Message DHT
"""
def postMessageData_api(id, message):
	"""add a message with id to the message DHT.
		id and message are both string.
	"""
	group.Send(3, id, message)
	return "message" # just for flask
server.register_function(postMessageData_api,'postMessageData')

def postMessageData(id, message):
	messages[id] = message
	print("Vsync server postMessageData with id=" + id.ToString())

def getMessageData_api(id):
	"""get a message from the message DHT with the given id.
		id is a string, and the functions return a string unless no macthing found.
	"""
	res = []
	nr = group.Query(Vsync.Group.ALL, 4, id, Vsync.EOLMarker(), res)
	for ele in res:
		if (ele != -1):
			return ele
	return -1
server.register_function(getMessageData_api,'getMessageData')

def getMessageData(id):
	group.Reply(messages[id])
	print("Vsync server getMessageData with id=" + id.ToString())

def removeMessageData_api(id):
	"""set a message to be "" in the message DHT with the given id.
		id is a string.
	"""
	group.Send(5, id)
	return "message" # just for flask
server.register_function(removeMessageData_api,'removeMessageData')

def removeMessageData(id):
	messages[id] = ""
	print("Vsync server removeMessageData with id=" + id.ToString())

""" Schedule DHT 
"""
def postScheduleData_api(id, schedule):
	"""add a schedule with id to the schedule DHT.
		id and schedule are both string
	"""
	group.Send(6, id, schedule)
	return "schedule" # just for flask
server.register_function(postScheduleData_api,'postScheduleData')

def postScheduleData(id, schedule):
	schedules[id] = schedule
	print("Vsync server postScheduleData with id=" + id.ToString())

def getScheduleData_api(id):
	"""get a schedule from the schedule DHT with the given id.
		id is a string, and the functions return a string unless no macthing found.
	"""
	res = []
	nr = group.Query(Vsync.Group.ALL, 7, id, Vsync.EOLMarker(), res)
	for ele in res:
		if (ele != -1):
			return ele
	return -1
server.register_function(getScheduleData_api,'getScheduleData')

def getScheduleData(id):
	group.Reply(schedules[id])
	print("Vsync server getScheduleData with id=" + id.ToString())

def removeScheduleData_api(id):
	"""set a schedule to be "" in the schedule DHT with the given id.
		id is a string.
	"""
	group.Send(8, id)
	return "profile"
server.register_function(removeScheduleData_api,'removeScheduleData')

def removeScheduleData(id):
	schedules[id] = ""
	print("Vsync server removeScheduleData with id=" + id.ToString())

### Vsycn register
def myViewFunc(v):
    print('New view: ' + v.ToString())
    print('My rank = ' + v.GetMyRank().ToString())
    for a in v.joiners:
        print('  Joining: ' + a.ToString() + ', isMyAddress='+a.isMyAddress().ToString())
    for a in v.leavers:
        print('  Leaving: ' + a.ToString() + ', isMyAddress='+a.isMyAddress().ToString())
    return
server.register_function(myViewFunc,'myViewFunc')

print "defined functions"

# register functiosn in Vysnc
group.RegisterHandler(0, Action[str, str](postUserData))
group.RegisterHandler(1, Action[str](getUserData))
group.RegisterHandler(2, Action[str](removeUserData))

group.RegisterHandler(3, Action[str, str](postMessageData))
group.RegisterHandler(4, Action[str](getMessageData))
group.RegisterHandler(5, Action[str](removeMessageData))

group.RegisterHandler(6, Action[str, str](postScheduleData))
group.RegisterHandler(7, Action[str](getScheduleData))
group.RegisterHandler(8, Action[str](removeScheduleData))

group.RegisterViewHandler(Vsync.ViewHandler(myViewFunc))
group.Join()

### run
server.serve_forever()
Vsync.VsyncSystem.WaitForever()

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


### User DHT
def postUserData_api(id, profile):
	group.Send(0, id, profile)
	return "profile"
server.register_function(postUserData_api,'postUserData')

def postUserData(id, profile):
	users[id] = profile
	print("Vsync server postUserData with id=" + id.ToString())

def getUserData_api(id):
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


### Message DHT
def postMessageData_api(id, message):
	group.Send(2, id, message)
	return "message"
server.register_function(postMessageData_api,'postMessageData')

def postMessageData(id, message):
	messages[id] = message
	print("Vsync server postMessageData with id=" + id.ToString())

def getMessageData_api(id):
	res = []
	nr = group.Query(Vsync.Group.ALL, 3, id, Vsync.EOLMarker(), res)
	for ele in res:
		if (ele != -1):
			return ele
	return -1
server.register_function(getMessageData_api,'getMessageData')

def getMessageData(id):
	group.Reply(messages[id])
	print("Vsync server getMessageData with id=" + id.ToString())

### Schedule DHT
def postScheduleData_api(id, Schedule):
	group.Send(4, id, Schedule)
	return "Schedule"
server.register_function(postScheduleData_api,'postScheduleData')

def postScheduleData(id, Schedule):
	Schedules[id] = Schedule
	print("Vsync server postScheduleData with id=" + id.ToString())

def postScheduleData_api(id):
	res = []
	nr = group.Query(Vsync.Group.ALL, 5, id, Vsync.EOLMarker(), res)
	for ele in res:
		if (ele != -1):
			return ele
	return -1
server.register_function(postScheduleData_api,'postScheduleData')

def postScheduleData(id):
	group.Reply(Schedules[id])
	print("Vsync server postScheduleData with id=" + id.ToString())

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

group.RegisterHandler(0, Action[str, str](postUserData))
group.RegisterHandler(1, Action[str](getUserData))
group.RegisterHandler(2, Action[str, str](postMessageData))
group.RegisterHandler(3, Action[str](getMessageData))
group.RegisterHandler(4, Action[str, str](postScheduleData))
group.RegisterHandler(5, Action[str](postScheduleData))
group.RegisterViewHandler(Vsync.ViewHandler(myViewFunc))
group.Join()

### run
server.serve_forever()
Vsync.VsyncSystem.WaitForever()

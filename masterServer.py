from System import Action
import clr
clr.AddReference('VsyncLib') # The profile of the dll file.
import Vsync

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

from threading import Thread

Vsync.VsyncSystem.Start()


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

server = SimpleXMLRPCServer(("localhost", 8000),
                            requestHandler=RequestHandler)
server.register_introspection_functions()

group = Vsync.Group("Master")
users = {}


def addUser(id, profile):
	users[id] = profile
	print("Vsync server addUser with id=" + id)
server.register_function(addUser,'addUser')

def getProfile(id):
	print("Vsync get profile with id=" + id)
	group.Reply(users[id])
server.register_function(getProfile,'getProfile')

def myViewFunc(v):
    print('New view: ' + v.ToString())
    print('My rank = ' + v.GetMyRank().ToString())
    for a in v.joiners:
        print('  Joining: ' + a.ToString() + ', isMyAddress='+a.isMyAddress().ToString())
    for a in v.leavers:
        print('  Leaving: ' + a.ToString() + ', isMyAddress='+a.isMyAddress().ToString())
    return
server.register_function(myViewFunc,'myViewFunc')

group.RegisterHandler(0, Action[int, str](addUser))
group.RegisterHandler(1, Action[int](getProfile))
group.RegisterViewHandler(Vsync.ViewHandler(myViewFunc))


Vsync.VsyncSystem.WaitForever()
server.serve_forever()

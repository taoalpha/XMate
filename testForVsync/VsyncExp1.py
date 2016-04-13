# required for Vsync
from System import Action
import clr
clr.AddReference('VsyncLib') # The name of the dll file.
import Vsync
#from Vsync import *

import time

Vsync.VsyncSystem.Start()

Users = {}


def addUser(id, name):
    print('Hello from addUser with id=' + id.ToString())
    Users[id] = name
    return
def getName(id):
    print('Hello from getName with id=' + id.ToString())
    g.Reply(Users[id])
    return
def myViewFunc(v):
    print('New view: ' + v.ToString())
    print('My rank = ' + v.GetMyRank().ToString())
    for a in v.joiners:
        print('  Joining: ' + a.ToString() + ', isMyAddress='+a.isMyAddress().ToString())
    for a in v.leavers:
        print('  Leaving: ' + a.ToString() + ', isMyAddress='+a.isMyAddress().ToString())
    return

g = Vsync.Group('Experiments')
g.RegisterHandler(0, Action[int, str](addUser))
g.RegisterHandler(1, Action[int](getName))
g.RegisterViewHandler(Vsync.ViewHandler(myViewFunc))
g.Join()
g.Send(0, 19, "Test user 1")
g.Send(0, 20, "Test user 2")
g.Send(0, 30, "Test user 3")
# time.sleep(20)
res = []
nr = g.Query(Vsync.Group.ALL, 1, 15, Vsync.EOLMarker(), res);
print('After Query got ' + nr.ToString() + ' results: ', res)

Vsync.VsyncSystem.WaitForever()
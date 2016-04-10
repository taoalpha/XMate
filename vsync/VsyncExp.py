# required for Vsync
from System import Action
import clr
clr.AddReference('VsyncLib') # The name of the dll file.
import Vsync
#from Vsync import *

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

g = Vsync.Group('FooBar')
g.RegisterHandler(0, Action[int, str](addUser))
g.RegisterHandler(1, Action[int](getName))
g.RegisterViewHandler(Vsync.ViewHandler(myViewFunc))
g.Join()
g.Send(0, 17, "Yihui Fu")
g.Send(0, 16, "Changsong Li")
g.Send(0, 15, "Jerry, Mao")
res = []
nr = g.Query(Vsync.Group.ALL, 1, 15, Vsync.EOLMarker(), res);
print('After Query got ' + nr.ToString() + ' results: ', res)

Vsync.VsyncSystem.WaitForever()
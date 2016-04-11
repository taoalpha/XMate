# required for Vsync
from System import Action
import clr
clr.AddReference('VsyncLib') # The profile of the dll file.
clr.AddReference('userDataType') # The profile of the dll file.
import Vsync
import DataDefinition
#from Vsync import *

import time

Vsync.VsyncSystem.Start()

Users = {}


def addUser(id, profile):
    print('Hello from addUser with id=' + id.ToString())
    Users[id] = profile
    return
def getProfile(id):
    print('Hello from getProfile with id=' + id.ToString())
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

g = Vsync.Group('Experiment')

g.RegisterHandler(0, Action[int, DataDefinition.userProfile](addUser))
g.RegisterHandler(1, Action[int](getProfile))
g.RegisterViewHandler(Vsync.ViewHandler(myViewFunc))
DataDefinition.initializer()

g.Join()
print "Line 43"

yihui = DataDefinition.userProfile()
print "Line 46"
yihui.FacebookID = 123
print "Line 48"
yihui.id = 321
print "Line 50"
yihui.username = "Yihui"
# yihui = DataDefinition.userProfile([123,321,"Yihui"])
print "Line 52"

g.Send(0, 17, yihui)
# g.Send(0, 15, jerry)
res = []
nr = g.Query(Vsync.Group.ALL, 1, 17, Vsync.EOLMarker(), res);
print('After Query got ' + nr.ToString() + ' results: ', res)

Vsync.VsyncSystem.WaitForever()
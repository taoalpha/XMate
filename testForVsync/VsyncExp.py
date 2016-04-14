# required for Vsync
from System import Action
import clr
clr.AddReference('VsyncLib') # The profile of the dll file.
clr.AddReference('DataTypes') # The profile of the dll file.
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

g.RegisterHandler(0, Action[int, DataDefinition.profile](addUser))
g.RegisterHandler(1, Action[int](getProfile))
g.RegisterViewHandler(Vsync.ViewHandler(myViewFunc))
DataDefinition.register()

g.Join()
print "Here 1"
profile = DataDefinition.profile()
print "Here 2"
profile.FacebookID = 123
print "Here 3"
profile.ID = 321
print "Here 4"
profile.username = "User 1"
profile.age = 20;
profile.gender = "Male"
profile.preferredGender = "Male"
profile.city = "Ithaca"
profile.latitude = 42.15
profile.longitude = 70.0
profile.credits = 3
profile.lastLoginTime = 20.2
profile.height = 5.6
profile.weight = 120
print "Here 5"
profile.addScheduleToList(12)
print "Here 6"
g.Send(0, 17, profile)
print "Here 7"

# g.Send(0, 15, jerry)
res = []
nr = g.Query(Vsync.Group.ALL, 1, 17, Vsync.EOLMarker(), res);
print('After Query got ' + nr.ToString() + ' results: ', res)

Vsync.VsyncSystem.WaitForever()
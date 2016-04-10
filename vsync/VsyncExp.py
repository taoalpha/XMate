# required for Vsync
from System import Action
import clr
clr.AddReference('VsyncLib') # The profile of the dll file.
import Vsync
#from Vsync import *

import time

Vsync.VsyncSystem.Start()

Users = {}

class Profile:
    def __init__(self, name=None, gender=None, age=None, byteArray=None):
        if (name != None and gender != None and age != None):
            self.name = name
            self.gender = gender
            self.age = age
        elif byteArray != None:
            objs = Vsync.Msg.BArrayToObjects(byteArray)
            self.name = objs[0]
            self.gender = objs[1]
            self.age = objs[2]
            
    def toBArray(self):
        return Vsync.Msg.toBArray(self.name, self.gender, self.age)

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

TID = 120
Vsync.Msg.RegisterType(type(Profile),TID)

g.RegisterHandler(0, Action[int, Profile](addUser))
g.RegisterHandler(1, Action[int](getProfile))
g.RegisterViewHandler(Vsync.ViewHandler(myViewFunc))

g.Join()
yihui = Profile("Yihui","f", 100)
jerry = Profile("Jerry", "m", 100)

g.Send(0, 17, yihui)
g.Send(0, 15, jerry)
res = []
nr = g.Query(Vsync.Group.ALL, 1, 15, Vsync.EOLMarker(), res);
print('After Query got ' + nr.ToString() + ' results: ', res)

Vsync.VsyncSystem.WaitForever()
'''
res:
    status:
        0: no match
        1: everything works normal
        2: error in Vsync
        3: invalid input
    msg:
        if status == 1, no msg else store_error_msg
    content:
        if status == 1, store real content

for vsync:
    getUserData( id )
        if return -1, no match

    postUserData( id, data_string )

    removeUserData( id )

    getScheduleData( id )
        if return -1, no match

    postScheduleData( id, data_string )

    removeScheduleData( id )

    getMessageData( id )
        if return -1, no match

    postMessageData( id, data_string )

    removeMessageData( id )
'''

import sys
import json
import xmlrpclib

class CDatabase:
    '''
        client: the client connected to the server
        db: the default database in the server

        See https://docs.mongodb.org/getting-started/python/ for more details to get familiar with
        the following functions

        Note all the return value is handled by return_helper() function
    '''
    def __init__(self):
        self.rpc = None

    def buildConnection(self):
        '''
            Desc:
                Get the server info to see whether the connection is failed
        '''
        try:
            self.rpc = xmlrpclib.ServerProxy('http://localhost:8000')
            return self.returnHelper(1)
        except:
            return self.returnHelper(2,"Connection lost")


    def getStatus(self):
        '''
            Desc:
                check the connection
        '''
        try:
            system = self.rpc.system
            return self.returnHelper()
        except:
            return self.returnHelper(2,"Failed to connect to rpc server")

    def insertData(self,type,datas):
        '''
            Desc:
                insert one document into user collection
            Args:
                data is a list of json
                type: user/schedule/message
            Ret:
                return json:
                    res.inserted_id
                    res.content
        '''
        content = []
        try:
            for data in datas:
                if data != "":
                    data_to_string = json.dumps(data)
                else:
                    data_to_string = data
                if type == "user":
                    self.rpc.postUserData(data["_id"],data_to_string)
                    content.append(data)
                elif type == "schedule":
                    id = hashlib.md5(data["type"]+data["creator"]+str(int(data["created_time"]))).hexdigest()
                    self.rpc.postScheduleData(id,data_to_string)
                    data["_id"] = id
                    content.append(data)
                elif type == "message":
                    id = hashlib.md5(data["sender_id"]+data["receiver_id"]+data["post_id"]).hexdigest()
                    self.rpc.postMessageData(id,data_to_string)
                    data["_id"] = id
                    content.append(data)
                elif type == "cache":
		    id = data["_id"]
                    self.rpc.postCacheData(id,data_to_string)
                    content.append(data)
                else:
                    return self.returnHelper(3, "invalid type")
            return self.returnHelper(1, "", content)
        except:
            return self.returnHelper(2,"fail to connect")

    def insertManyData(self,type,data):
        '''
            Desc:
                insert many documents into user collection
            Args:
                data is a list of json type documents
            Ret:
                return
        '''
        try:
            for i in data:
                self.insertData(type,i)
            return self.returnHelper()
        except:
            return self.returnHelper(2,"Failed to connect to the rpc server")

    def getData(self, type, id_list):
        '''
            Desc:
                get documents by match_list
            Args:
                type: user/schedule/message
                id_list: list of ids
            Ret:
                return the matched documents list
        '''
        if len(id_list) == 0:
            # get all
            try:
                if type == "user":
                    d = json.loads(self.rpc.getAllUsers())
                    content = [k:json.loads(v) for k,v in d.iteritems() if v != "-1"]
                elif type == "message":
                    d = json.loads(self.rpc.getAllMessages())
                    content = [k:json.loads(v) for k,v in d.iteritems() if v != "-1"]
                elif type == "schedule":
                    d = json.loads(self.rpc.getAllSchedules())
                    content = [k:json.loads(v) for k,v in d.iteritems() if v != "-1"]
                elif type == "cache":
                    d = json.loads(self.rpc.getAllCache())
                    content = [k:json.loads(v) for k,v in d.iteritems() if v != "-1"]
                else:
                    return "invalid"
                return content
            except:
                return "err"


DB = new CDatabase()

DB.buildConnection()

dataset = {}

dataset["user"] = DB.getData("user",[])
dataset["schedule"] = DB.getData("schedule",[])
dataset["message"] = DB.getData("message",[])
dataset["cache"] = DB.getData("cache",[])

print dataset

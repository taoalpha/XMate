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
import hashlib
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
                    print id
                    print data
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

    def backup(self, type, id_list):
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
                    content = {k:json.loads(v) for k,v in d.iteritems() if v != "-1"}
                elif type == "message":
                    d = json.loads(self.rpc.getAllMessages())
                    content = {k:json.loads(v) for k,v in d.iteritems() if v != "-1"}
                elif type == "schedule":
                    d = json.loads(self.rpc.getAllSchedules())
                    content = {k:json.loads(v) for k,v in d.iteritems() if v != "-1"}
                elif type == "cache":
                    d = json.loads(self.rpc.getAllCache())
                    content = {k:json.loads(v) for k,v in d.iteritems() if v != "-1"}
                else:
                    return self.returnHelper(3, "invalid type")
                return self.returnHelper(1, "", content)
            except:
                return self.returnHelper(2,"Failed to get from rpc")

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
                    content = [json.loads(v) for k,v in d.iteritems() if v != "-1"]
                elif type == "message":
                    d = json.loads(self.rpc.getAllMessages())
                    content = [json.loads(v) for k,v in d.iteritems() if v != "-1"]
                elif type == "schedule":
                    d = json.loads(self.rpc.getAllSchedules())
                    content = [json.loads(v) for k,v in d.iteritems() if v != "-1"]
                elif type == "cache":
                    d = json.loads(self.rpc.getAllCache())
                    content = [json.loads(v) for k,v in d.iteritems() if v != "-1"]
                else:
                    return self.returnHelper(3, "invalid type")
                return self.returnHelper(1, "", content)
            except:
                return self.returnHelper(2,"Failed to get from rpc")

        content = []
        try:
            if type == "user":
                for i in id_list:
                    content.append(json.loads(self.rpc.getUserData(i)))
                return self.returnHelper(1, "", content)
            elif type == "schedule":
                for i in id_list:
                    content.append(json.loads(self.rpc.getScheduleData(i)))
                return self.returnHelper(1, "", content)
            elif type == "message":
                for i in id_list:
                    content.append(json.loads(self.rpc.getMessageData(i)))
                return self.returnHelper(1, "", content)
            elif type == "cache":
                for i in id_list:
                    content.append(json.loads(self.rpc.getCacheData(i)))
                return self.returnHelper(1, "", content)
            else:
                return self.returnHelper(3, "invalid type")
        except:
            return self.returnHelper(2,"Failed to get from rpc")

    def updateData(self, type, id_list, data_list):
        '''
            Desc:
                update documents by data via match_list constraint in user collection.
            Args:
                type: user/schedule/message
                id_list: list of ids
                data_list: list of json reprents the data I need to store into it.
            Res:
                # matched data by res.matched_count, # modified data by res.modified_count
        '''
        length = len(id_list)
        content = []
        try:
            for i in range(0,length):
                data_list[i]["_id"] = id_list[i]
                res = self.insertData(type,[data_list[i]])
                content.append(res["content"])
            return self.returnHelper(1, "", content)
        except:
            return self.returnHelper(2,"Failed to insert data")

    def removeData(self, type, id_list):
        '''
            Desc:
                remove the item by setting the entry to empty string
            Args:
                type: user/schedule/message
                id_list: list of id that need to be removed
            Res:
                return res
        '''
        length = len(id_list)
        content = []
        try:
            for i in range(0,length):
                if type == 'message':
                    res = self.rpc.removeMessageData(id_list[i])
                    content.append(res)
                elif type == 'schedule':
                    res = self.rpc.removeScheduleData(id_list[i])
                    content.append(res)
                elif type == 'user':
                    res = self.rpc.removeUserData(id_list[i])
                    content.append(res)
                elif type == 'cache':
                    res = self.rpc.removeCacheData(id_list[i])
                    content.append(res)

            return self.returnHelper(1, "", content)
        except:
            return self.returnHelper(2,"Failed to connect to rpc")

    def returnHelper(self, status = 1, msg = None,content = None):
        '''
            Desc:
                Handle all the other functions' return value
            Args:
                status:
                    0: no match
                    1: everything works normal
                    2: error in Vsync
                msg:
                    if status == 1, no msg else store_error_msg
                content:
                    if status == 1, store real content
        '''
        res = {}
        if content != None and "".join(str(x) for x in content) == "-1":
            res["status"] = 0
            res["msg"] = "no match"
        else:
            res["status"] = status
            res["msg"] = msg
            #res["error"] = sys.exc_info()
            res["error"] = "error"
            res["content"] = content

        return res

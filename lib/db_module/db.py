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


    def checkConnection(self):
        '''
            Desc:
                check the connection
        '''
        try:
            system = self.rpc.system
            return self.returnHelper()
        except:
            return self.returnHelper(2,"Failed to connect to rpc server")

    def insertData(self,type,data):
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
        content = {}
        if data != "":
            data_to_string = json.dumps(data)
        data_to_string = data
        try:
            if type == "user":
                self.rpc.postUserData(data["_id"],data_to_string)
                return self.returnHelper(1, "", data)
            elif type == "schedule":
                id = hashlib.md5(data["type"]+data["creator"]+data["created_time"]).hexdigest()
                self.rpc.postScheduleData(id,data_to_string)
                return self.returnHelper(1, "", data)
            elif type == "message":
                id = hashlib.md5(data["sender_id"]+data["receiver_id"]+data["post_id"]).hexdigest()
                self.rpc.postUserData(data["_id"],data_to_string)
                return self.returnHelper(1, "", data)
            else:
                return self.returnHelper(3, "invalid type")
        except:
            return self.returnHelper(2,"Failed to insert data")

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
            else:
                return self.returnHelper(3, "invalid type")
        except:
            return self.returnHelper(2,"Failed to insert data")

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
                res = self.insertData(type,id_list[i],data_list[i])
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
                res = self.insertData(type,id_list[i],"")
                content.append(res["content"])
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
        res["status"] = status
        res["msg"] = msg
        res["error"] = sys.exc_info()
        res["content"] = content

        return res

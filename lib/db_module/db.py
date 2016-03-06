import sys, pymongo

class CDatabase:
    '''
        client: the client connected to the server
        db: the default database in the server

        See https://docs.mongodb.org/getting-started/python/ for more details to get familiar with
        the following functions

        Note all the return value is handled by return_helper() function
    '''
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None

    def buildConnection(self, url_name = 'mongodb://changsong:Lcs19921126@ds011298.mongolab.com:11298/lcs1992cs'):
        '''
            Desc:
                build connection to database via the url name
            Args:
                url_name: the url of the database
        '''
        try:
            self.client = pymongo.MongoClient(url_name,connect = True, serverSelectionTimeoutMS = 1000)

            self.db = self.client.get_default_database()
            return self.returnHelper()
        except:
            return self.returnHelper(1,"Failed to build the database connection")

    def getStatus(self):
        '''
            Desc:
                Get the server info to see whether the connection is failed
                Build long-time connection to db
        '''
        try:
            self.client.server_info()
            return self.returnHelper()
        except:
            return self.returnHelper(1,"Connection lost")


    def selectCollection(self, coll_name):
        '''
            Desc:
                Select collection by coll_name
            Args:
                coll_name: "xmateHistoryPost", "xmatePost", "xmateUser","xmateMessage"
        '''
        try:
            self.collection = self.db[coll_name]
            return self.returnHelper()
        except:
            return self.returnHelper(1,"Failed to select connection")

    def closeConnection(self):
        '''
            Desc:
                close connection to database via the url name
        '''
        try:
            self.client.close()
            return self.returnHelper()
        except:
            return self.returnHelper(1,"Failed to close the database connection")


    def insertData(self,data):
        '''
            Desc:
                insert one document into user collection
            Args:
                data is a json type document
            Ret:
                return res(object), res.inserted_id is the inserted document's id
        '''
        try:
            res = self.collection.insert_one(data)
            return self.returnHelper(content = res)
        except:
            return self.returnHelper(1,"Failed to insert data")

    def insertManyData(self,data):
        '''
            Desc:
                insert many documents into user collection
            Args:
                data is json type documents
            Ret:
                return res(object), res.inserted_id is the inserted document's id list
        '''
        try:
            res = self.collection.insert_many(data)
            return self.returnHelper(content = res)
        except:
            return self.returnHelper(1,"Failed to insert many data")

    def getData(self, match_list):
        '''
            Desc:
                get documents by match_list
            Args:
                match_list is a json type dict, {"key":value",...}
            Ret:
                return the matched documents list
        '''
        try:
            cursor = self.collection.find(match_list)
            return self.returnHelper(content = cursor)
        except:
            return self.returnHelper(1,"Failed to get data")


    def updateData(self, match_list, data):
        '''
            Desc:
                update documents by data via match_list constraint in user collection.
            Args:
                match_list = {"key":"value",...}, data = {"key":"value",...}
            Ret:
                # matched data by res.matched_count, # modified data by res.modified_count
        '''
        try:
            res = self.collection.update_one(match_list, {"$set":data})
            return self.returnHelper(content = res)
        except:
            return self.returnHelper(1,"Failed to update data")

    def removeData(self, match_list):
        '''
            Desc:
                remove documents by match_list constraint in user collection.
            Args:
                match_list = {"key":"value",...}
            Ret:
                # matched data by res.matched_count, # modified data by res.modified_count
        '''
        try:
            res = self.collection.delete_many(match_list)
            return self.returnHelper(content = res)
        except:
            return self.returnHelper(1,"Failed to remove data")

    def returnHelper(self, status = 0, msg = None,content = None):
        '''
            Desc:
                Handle all the other functions' return value
            Args:
                status: 0 no error, 1 exception; msg: where the error occur
                content: store the result; error: system error information
            Ret:
                # matched data by res.matched_count, # modified data by res.modified_count
        '''
        return_val = {}
        return_val["status"] = status
        return_val["msg"] = msg
        return_val["error"] = sys.exc_info()[0]
        return_val["content"] = content

        return return_val























import sys, pymongo

class CDatabase:
    '''
        client: the client connected to the server
        db: the default database in the server
    '''
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None

    def buildConnection(self, url_name = 'mongodb://changsong:Lcs19921126@ds011298.mongolab.com:11298/lcs1992cs'):
        '''Build connection to database via the url name'''
        try:
            self.client = pymongo.MongoClient(url_name)
            self.db = self.client.get_default_database()
            self.collection = self.db[self.coll_name]
            return self.returnHelper()
        except:
            return self.returnHelper(1,"Failed to build the database connection")


    def closeConnection(self):
        '''Close the connection to database'''
        try:
            self.client.close()
            return self.returnHelper()
        except:
            return self.returnHelper(1,"Failed to close the database connection")


    def insertData(self,data):
        '''insert one document(data: jason type document) into specified collection, return its id'''
        try:
            res = self.collection.insert_one(data)
            return self.returnHelper(content = res)
        except:
            return self.returnHelper(1,"Failed to insert data")

    def insertManyData(self,data):
        '''insert many documents(data: jason type document) into specified collection, return its id list'''
        try:
            res = self.collection.insert_many(data)
            print(self.collection.count())
            return self.returnHelper(content = res)
        except:
            return self.returnHelper(1,"Failed to insert many data")

    def getData(self, match_list):
        '''Get documents by match_list = {"key":"value",...}, return the matched documents'''
        try:
            cursor = self.collection.find(match_list)
            return self.returnHelper(content = cursor)
        except:
            return self.returnHelper(1,"Failed to get data")


    def updateData(self, match_list, data):
        '''
            Update the data by match_list in the user collection.
            match_list = {"key":"value",...}, data = {"key":"value",...}
            Could get # matched data by res.matched_count, get # modified data by res.modified_count
        '''
        try:
            res = self.collection.update_one(match_list, {"$set":data})
            return self.returnHelper(content = res)
        except:
            return self.returnHelper(1,"Failed to update data")

    def removeData(self, match_list):
        '''
            Remove the data by match_list = {"key":"value",...}, in the user collections.
            Could get # deleted data by res.deleted_count
        '''
        try:
            res = self.collection.delete_many(match_list)
            return self.returnHelper(content = res)
        except:
            return self.returnHelper(1,"Failed to remove data")

    def returnHelper(self, status = 0, msg = None,content = None):
        return_val = {}
        return_val["status"] = status
        return_val["msg"] = msg
        return_val["error"] = sys.exc_info()[0]
        return_val["content"] = content

        return return_val























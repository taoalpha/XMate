import sys, pymongo
from db import CDatabase

class CMessage(CDatabase):
    def __init__(self):
        CDatabase.__init__(self)
        self.coll_name = "xmateMessage"
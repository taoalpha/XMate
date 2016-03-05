import sys, pymongo
from .db import CDatabase

class CUser(CDatabase):
	def __init__(self):
		CDatabase.__init__(self)
		self.coll = "xmateUser"


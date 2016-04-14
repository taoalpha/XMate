import xmlrpclib

s = xmlrpclib.ServerProxy('http://localhost:8000')
print "Test client ready"

# test user DHT
def testPostUserData():
	s.postUserData("1", "UserData1")
	assert s.getUserData("1") == "UserData1"
	assert s.getUserData("2") == "-1"

def testRemoveUserData():
	s.postUserData("1", "UserData1")
	s.removeUserData("1")
	assert s.getUserData("1") == ""

def testPostUserDataMultiple():
	s.postUserData("1", "UserData1")
	s.postUserData("2", "UserData2")
	assert s.getUserData("1") == "UserData1"
	assert s.getUserData("2") == "UserData2"

def testRemoveUserDataMultiple():
	s.postUserData("1", "UserData1")
	s.postUserData("2", "UserData2")
	assert s.getUserData("1") == "UserData1"
	assert s.getUserData("2") == "UserData2"
	s.removeUserData("1")
	assert s.getUserData("1") == ""
	assert s.getUserData("2") == "UserData2"
	s.removeUserData("2")
	assert s.getUserData("1") == ""
	assert s.getUserData("2") == ""

# test message DHT
def testPostMessageData():
	s.postMessageData("1", "MessageData1")
	assert s.getMessageData("1") == "MessageData1"
	assert s.getMessageData("2") == "-1"

def testRemoveMessageData():
	s.postMessageData("1", "MessageData1")
	s.removeMessageData("1")
	assert s.getMessageData("1") == ""

def testPostMessageDataMultiple():
	s.postMessageData("1", "MessageData1")
	s.postMessageData("2", "MessageData2")
	assert s.getMessageData("1") == "MessageData1"
	assert s.getMessageData("2") == "MessageData2"

def testRemoveMessageDataMultiple():
	s.postMessageData("1", "MessageData1")
	s.postMessageData("2", "MessageData2")
	assert s.getMessageData("1") == "MessageData1"
	assert s.getMessageData("2") == "MessageData2"
	s.removeMessageData("1")
	assert s.getMessageData("1") == ""
	assert s.getMessageData("2") == "MessageData2"
	s.removeMessageData("2")
	assert s.getMessageData("1") == ""
	assert s.getMessageData("2") == ""

# test schedule DHT
def testPostScheduleData():
	s.postScheduleData("1", "ScheduleData1")
	assert s.getScheduleData("1") == "ScheduleData1"
	assert s.getScheduleData("2") == "-1"

def testRemoveScheduleData():
	s.postScheduleData("1", "ScheduleData1")
	s.removeScheduleData("1")
	assert s.getScheduleData("1") == ""

def testPostScheduleDataMultiple():
	s.postScheduleData("1", "ScheduleData1")
	s.postScheduleData("2", "ScheduleData2")
	assert s.getScheduleData("1") == "ScheduleData1"
	assert s.getScheduleData("2") == "ScheduleData2"

def testRemoveScheduleDataMultiple():
	s.postScheduleData("1", "ScheduleData1")
	s.postScheduleData("2", "ScheduleData2")
	assert s.getScheduleData("1") == "ScheduleData1"
	assert s.getScheduleData("2") == "ScheduleData2"
	s.removeScheduleData("1")
	assert s.getScheduleData("1") == ""
	assert s.getScheduleData("2") == "ScheduleData2"
	s.removeScheduleData("2")
	assert s.getScheduleData("1") == ""
	assert s.getScheduleData("2") == ""

# test operations involving three DHTs
def testMixDHT():
	s.postUserData("1", "UserData1")
	s.postMessageData("1", "MessageData1")
	s.postScheduleData("1", "ScheduleData1")
	assert s.getUserData("1") == "UserData1"
	assert s.getMessageData("1") == "MessageData1"
	assert s.getScheduleData("1") == "ScheduleData1"


testPostUserData()
testRemoveUserData()
testPostUserDataMultiple()
testRemoveUserDataMultiple()

testPostMessageData()
testRemoveMessageData()
testPostMessageDataMultiple()
testRemoveMessageDataMultiple()

testPostScheduleData()
testRemoveScheduleData()
testPostScheduleDataMultiple()
testRemoveScheduleDataMultiple()
print "Testing succeeded"

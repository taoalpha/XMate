import requests

postUrl = "http://localhost:5000"

def sendUserProfile(profile):
	r = requests.post(postUrl+'/user/', data = profile)
	if (!checkStatus(r)):
		break

def sendScheduleProfile(profile):
	r = requests.post(postUrl+'/schedule/', data = profile)

def sendMessageProfile(profile):
	r = requests.post(postUrl+'/message/', data = profile)


def checkStatus(r):
	data = r.json()
	if (data["status"] != 1):
		print data
		return false
	else:
		return true
	

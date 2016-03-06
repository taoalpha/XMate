from postModule import CPost
from historyPostModule import CHistoryPost
from userModule import CUser
import random
import datetime, time

def generateSchedule():
    user_db = CUser()
    aa = user_db.buildConnection()
    # print(aa)

    # get all users in a list
    users = user_db.getData({})['content']
    user_db.closeConnection()

    # exercise type
    exer_type = ["DoTA","Hotpot","Tennis", "Coding","Running"]

    # initialize schedule dict and history dict to find participating users
    scheduleMem = {}
    historyMem = {}
    for user in users:
        uid = user['uid']
        if "schedule_list" in user:
            # print(user['schedule_list'])
            scheduleList = user['schedule_list']
            for schedule in scheduleList:
                if schedule in scheduleMem:
                    scheduleMem[schedule].append(uid)
                else:
                    scheduleMem[schedule] = [uid]

        if "history_events" in user:
            # print(user['history_events'])
            historyList = user['history_events']
            for history in historyList:
                if history in historyMem:
                    historyMem[history].append(uid)
                else:
                    historyMem[history] = [uid]

    # print(scheduleMem)
    # print(historyMem)

    schedule_res = []
    history_res = []
    # randomly generate schedule and history schedule
    for i in range(2000):
        # schedule
        if i in scheduleMem:
            schedule = {}
            schedule['sid'] = i
            schedule['type'] = random.choice(exer_type)
            schedule['status'] = "coming"

            # latitude range for ithaca [42.400000, 42.500000]
            # longitude range for ithaca[-76.560000,-76.410000]
            schedule['location'] = {"city":"Ithaca"}
            schedule['location']['latitude'] = random.uniform(42.40,42.50)
            schedule['location']['longitude'] = random.uniform(-76.56, -76.41)
            
            # time, within the past week
            schedule['post_datetime'] = getNextDateTime(1456622834.756554, 10080)
            schedule['time_range'] = {}
            schedule['time_range']['start_time'], schedule['time_range']['end_time'] = getExerRange(schedule['post_datetime'],86400, 7200)
        
            # member
            schedule['member'] = scheduleMem[i]
            schedule['owner'] = schedule['member'].pop(0)
            schedule['creator'] = schedule['owner']
            schedule['related_member'] = []

            schedule_res.append(schedule)

            print(schedule)

        # history
        if i in historyMem:
            history = {}
            history['sid'] = i
            history['type'] = random.choice(exer_type)

            # Location
            history['location'] = {"city":"Ithaca"}
            history['location']['latitude'] = random.uniform(42.40,42.50)
            history['location']['longitude'] = random.uniform(-76.56, -76.41)

            # Time
            history['post_datetime'] = getNextDateTime(1455413234.756554, 10080)
            history['time_range'] = {}
            history['time_range']['start_time'], history['time_range']['end_time'] = getExerRange(schedule['post_datetime'],86400, 7200)

            # member
            history['member'] = historyMem[i]
            history['owner'] = history['member'].pop(0)
            history['creator'] = history['owner']

            history_res.append(history)

            print(history)

    print(len(schedule_res))
    print(len(history_res))

    # write to schedule db
    schedule_db = CPost()
    schedule_db.buildConnection()
    schedule_db.insertManyData(schedule_res)
    schedule_db.closeConnection()

    # write to history schedule db
    history_db = CHistoryPost()
    history_db.buildConnection()
    history_db.insertManyData(history_res)
    history_db.closeConnection()


def getExerRange(startTime, max, range):
    '''given a start time, return a time range whose start time is within the given max
    and the time duration equals to the given range
    Args：
        startTime: the start time, represented in seconds, usually is the posting date
        max: the time range based on which to generate start time for a exercise period
        range: set to 2 hours, 7200 seconds
    '''
    begin = startTime + random.randint(1, max)
    end = begin + range
    return begin, end


def getNextDateTime(startTime, range):
    '''given a start time and a range, return a new date in the range
    after the given start time
    Args:
        startTime: the start time, represented in seconds
    Returns:
        a date time in the same format as the start time
    '''
    res = startTime + random.randint(1,range)
    return res


if __name__ == "__main__":
    generateSchedule()
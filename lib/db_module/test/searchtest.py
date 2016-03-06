import string, random, sys
from db import CDatabase
import computematch
# student_tuples = [
#     {"name":"john","grade":"A","age":15},
#     {"name":"jane","grade":"B","age":10},
#     {"name":"dave","grade":"C","age":12},
#     {"name":"david","grade":"B","age":12},
#     {"name":"Tom","grade":"A","age":12}
# ]s
# a = sorted(student_tuples, key=lambda student: (student["age"],student['grade']))
# print(a)
# student_tuples.sort(key = lambda s: s["grade"], reverse=True)
# print(student_tuples)

mydatabase = CDatabase()
res = mydatabase.buildConnection()

if(res['status']):
    print(res)



post_content = {
    "type":"DoTA",
    "time_range":
    {
          "end_time":1456689029.756554,
          "start_time":1456641029.756554
    },
    "location":{
        "latitude": 42.456890018402735,
        "longitude": -76.42710209470578,
        "city": "Ithaca"
    }
}

reslist = computematch.computeMatchPosts(10,post_content, mydatabase)
print(len(reslist))
for i in range(0,5):
    print(reslist[i]["type"], reslist[i]["time_range"]["start_time"],reslist[i]["time_range"]["start_time"])
    if('diff' in reslist[0]):
        print(reslist[i]["diff"])
















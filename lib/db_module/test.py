import sys
from userModule import CUser

userColl = CUser()

print(userColl.buildConnection())
test_data = {
	"uid":"1252",
	"name":"lll",
	"gender":"male"
}
res = userColl.insertData(test_data)
print(res)

fdata = {
	"uid":"123",
	"gender":["male", "female"]
}
print(userColl.getData(fdata))

data = {"name":"tai", "age":"25"}
print(userColl.updateData(fdata, data))

import json
from flask import Flask,request,jsonify
from lib.module.userController import userDispatch
from lib.module.scheduleController import scheduleDispatch
from lib.module.messageController import messageDispatch

from lib.db_module.db import CDatabase
# connect with db
db = CDatabase()
db.buildConnection()
#db.buildConnection("localhost:27017")

# TODO: try catch db connection

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

@app.route('/')
def hello_world():
    return 'The api interface'

@app.route('/user/', defaults={'uid':None, 'action': None},methods=['GET', 'POST'])
@app.route('/user/<uid>', defaults={'action': None},methods=['GET', 'PUT', 'DELETE'])
@app.route('/user/<uid>/<action>')
def user(uid,action):
    status = db.getStatus()
    print status
    if status["status"] != 1:
        db.buildConnection()
    #return jsonify(**userDispatch(uid,action,request,db))
    #return json.dumps(userDispatch(uid,action,request,db))
    return json.dumps(userDispatch(uid,action,request,db))


@app.route('/schedule/', defaults={'sid':None, 'action': None},methods=['GET', 'POST'])
@app.route('/schedule/<sid>', defaults={'action': None},methods=['GET', 'PUT', 'DELETE'])
@app.route('/schedule/<sid>/<action>')
def schedule(sid,action):
    status = db.getStatus()
    if status["status"] != 1:
        db.buildConnection()
    #db.selectCollection("xmateHistoryPost")
    return json.dumps(scheduleDispatch(sid,action,request,db))

@app.route('/message/', defaults={'mid':None, 'action': None},methods=['GET', 'POST','PUT','DELETE'])
@app.route('/message/<mid>', defaults={'action': None},methods=['DELETE','GET','POST','PUT'])
@app.route('/message/<mid>/<action>',methods=['GET','POST','PUT'])
def message(mid,action):
    status = db.getStatus()
    if status["status"] != 1:
        db.buildConnection()

    return json.dumps(messageDispatch(mid,action,request,db))

# test for vsync connection
@app.route('/rpc', defaults={'mid':None, 'action': None},methods=['GET', 'POST','PUT','DELETE'])
@app.route('/rpc/<mid>', defaults={'action': None},methods=['DELETE','GET','POST','PUT'])
@app.route('/rpc/<mid>/<action>',methods=['GET','POST','PUT'])
def rpc(mid,action):
    import xmlrpclib
    s = xmlrpclib.ServerProxy('http://localhost:8000')
    s.addUser(1,"fuck vysnc")
    return jsonify({"hello":s.getProfile(1)})

@app.route("/test",defaults={'type':"user"},methods=["GET"])
@app.route('/test/<type>', methods=['DELETE','GET','POST','PUT'])
def test(type):
    return jsonify(db.getAllData(type))

@app.route("/adminbackup_need_password", defaults={'type':"user"}, methods=["GET"])
@app.route("/adminbackup_need_password/<type>", methods=["GET"])
def backup(type):
    return jsonify(db.backup(type,[]))


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

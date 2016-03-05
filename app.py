from flask import Flask,request,jsonify
from lib.module.userController import userDispatch
from lib.module.scheduleController import scheduleDispatch
from lib.module.messageController import messageDispatch

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'The api interface'

@app.route('/user/', defaults={'uid':None, 'action': None},methods=['GET', 'POST'])
@app.route('/user/<uid>', defaults={'action': None},methods=['GET', 'PUT'])
@app.route('/user/<uid>/<action>')
def user(uid,action):
    return jsonify(**userDispatch(uid,action,request))

@app.route('/schedule', defaults={'sid':None, 'action': None},methods=['GET', 'POST'])
@app.route('/schedule/<sid>', defaults={'action': None})
@app.route('/schedule/<sid>/<action>')
def schedule(sid,action):
    return "schedule"

@app.route('/message', defaults={'mid':None, 'action': None},methods=['GET', 'POST'])
@app.route('/message/<mid>', defaults={'action': None})
@app.route('/message/<mid>/<action>')
def message(mid,action):
    return "message"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

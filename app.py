from flask import Flask,request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'The api interface'

@app.route('/user')
def user():
    return request.path

@app.route('/schedule')
def schedule():
    return "schedule"

@app.route('/message')
def message():
    return "message"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

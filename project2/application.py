
import os


from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app)

channels = []
users = []

message_list = {"asdf": ["hola como estas?", "bien y tu"]}

@app.route("/", methods = ["POST", "GET"])
def index():  
    reference_code = 1
    if request.method == "POST":
        channel = request.form.get("channel_name")
        if (channel not in channels):
            channels.append(channel)
            message_list[channel] = []
        else:
            reference_code = 300
        return render_template("index.html", channels=channels, reference_code=reference_code)
    else:
        return render_template("index.html", channels=channels, reference_code=reference_code)

@app.route("/register", methods = ["POST", "GET"])
def register():
    reference_code = 1
    if request.method == "POST":
        user = request.form.get("nickname")
        if (user not in users):
            users.append(user)
            return render_template("new_user.html", user = user)
        else:
            reference_code = 400
        return render_template("register.html", users= users, reference_code = reference_code)
    else:
        return render_template("register.html")

    

@app.route("/logout/<string:nickname>", methods = [ "GET"])
def logout(nickname):
    users.remove(nickname)
    return render_template("exit.html")
    


@app.route("/channel/<string:channel>", methods = ["GET"])
def create_channel(channel):
        return render_template("channels.html", channel = channel, message_list = message_list[channel])


@socketio.on('send message')
def add_new_message(message_list2):
    if (len(message_list[message_list2['channel']]) == 100):
        message_list[message_list2['channel']].pop(0)    
    message_list[message_list2['channel']].append(message_list2)
    emit("new message", {"mensaje": message_list2['mensaje'], "username": message_list2['username'], "date": message_list2['date'], "channel": message_list2['channel']}, broadcast= True)

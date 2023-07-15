from flask import Flask, request,jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/http-call")
def http_call():
    """return JSON with string data as the value"""
    data = {'data':'This text was fetched using an HTTP call to server on render'}
    return jsonify(data)

@socketio.on("connection")
def connected():
    """event listener when client connects to the server"""
    print('connecting')
    # print(request.sid)
    print("client has connected")
    emit("connect",{"data":f"id: {request.sid} is connected"})

@socketio.on('send_message')
def handle_message(data):
    """event listener when client types a message"""
    print("data from the front end: ",str(data))
    emit("receive_message",{'message': data["message"]}, broadcast=True)

@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect",f"user {request.sid} disconnected",broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True,port=5001)
# import Flask module (class) from flask package (Library)
from flask import Flask, render_template
import os

# import SocketIo (class) from flask_socketio (module)
from flask_socketio import SocketIO, emit


# creat app instance
app = Flask(__name__)
#only we have the access to cookie !
app.config['SECRET_KEY'] = os.urandom(24).hex() 

# SocketIO is being applied to ‘app’ 
socketio = SocketIO(app)



@app.route('/', methods = ['POST', 'GET'])
def sessions():
    return render_template('session.html')

def MessageRecieved():
    print('message was recieved ! ! !')

@socketio.on('my event')

def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('recieved my event' + str(json))
    socketio.emit('my response', json, callback=MessageRecieved)





# if runing directly main.py
if __name__ == '__main__':
    print("runing directly main.py")
    # take optional host and port
    socketio.run(app, debug=True)





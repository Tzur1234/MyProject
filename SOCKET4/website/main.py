from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify, make_response
from flask_session import Session
from client.client import Client
from threading import Thread
import secrets
import time


app = Flask(__name__) # creat app object according to the this module name
client = None
messages = []



#Config Session in Flask

# So this session has a default time limit: 31 days **OR** it will  when user close the browser
app.config["SESSION_PERMANENT"] = False

# Store the cookie on the usr's hard drive
app.config["SESSION_TYPE"] = "filesystem"   



app.config["SECRET_KEY"] = secrets.token_hex() # Create secret Key 

# config that each user gets its own session version
Session(app)


@app.route('/')
def index():
    """
    Receice new client and create new Client obj
    return the index page
    """
    if not session.get("name"):
        flash("You must logge in first!", "info")
        return redirect(url_for("login"))
    else:
        
        global client # using the "global" keywords to modify the client veriable   
        
        # Create cliet_socket ! ! !
        client = Client(session["name"]) 

       
        flash(f"You have been logged in! {session['name']}", "info")
        return render_template("index.html")




@app.route('/login', methods = ['GET', 'POST'])
def login():
    """
    if POST -- > create Client obj + send the user to Chat page
    """
    if session.get("name"):
        return redirect(url_for('index')) # if the user already connected

    if request.method == 'GET':
        return render_template("login.html")
    else:

        session["name"] = request.form["name"]
        return redirect(url_for("index"))


@app.route('/run')
def send_message():
    """
    manange user message 
    INPUT : messages from the index.html -- > index.js --> send_messages()
    """
    global client
    msg = request.args.get("val")
    print(msg)
    client.send_message(msg)

    if client == None:
        return "none"
    else:
        client.send_message(msg)
    
    return "hello world"



@app.route('/logout')
def logout():
    """
    close user's socket , remove from session, send "quit" message to the server
    """
    global client
    if not session.get("name"):
       return redirect(url_for('login'))
    else:
        global client
        client.send_message("{quit}")
        session.pop("name")
        flash("You have been logged out!", "info")
        return redirect(url_for("login"))    




# def update_messages():
#     """
#     updates the messages come to this client from server.py 
#     :return: None
#     """
#     global client
#     global messages
    
#     while True:
#         time.sleep(1.1)  # update every 1/10 of a second      
#         new_messages = client.get_messages()  # get new messages from client
#         messages.extend(new_messages)
        



@app.route('/send_list_back')
def send_list_back():
    global client
    res = make_response(jsonify({"messages": client.get_messages()}), 200)
    return res  



# @app.route('/send_list_back')
# def send_list_back():
#     global messages
#     msgs_copy = messages
#     messages = []
#     res = make_response(jsonify({"messages": msgs_copy}), 200)
#     return res  






if __name__ == "__main__":
    Thread(target=update_messages).start()
    app.run(debug=True)
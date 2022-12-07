from flask import Flask, render_template, request, redirect, session, url_for, flash, json
from flask_session import Session
from client.client import Client
import secrets

app = Flask(__name__) # creat app object according to the this module name

# ee



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
    if not session.get("name"):
        flash("You must logge in first!", "info")
        return redirect(url_for("login"))
    else:
        # Create cliet_socket ! ! !
        session["client"] = Client(session["name"]) 
        flash("You have been logged in!", "info")
        return render_template("index.html")




@app.route('/login', methods = ['GET', 'POST'])
def login():
    if session.get("name"):
        return redirect(url_for('index')) # if the user already connected

    if request.method == 'GET':
        return render_template("login.html")
    else:

        session["name"] = request.form["name"]
        return redirect(url_for("index"))


@app.route('/run')
def run():
    msg = request.args.get("val")
    print(msg)
    return "hello world"



@app.route('/logout')
def logout():
    if not session.get("name"):
       return redirect(url_for('login'))
    else:
        session.pop("name")
        flash("You have been logged out!", "info")
        return redirect(url_for("login"))    



if __name__ == "__main__":
    app.run(debug=True)
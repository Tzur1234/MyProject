import datetime
from flask import Flask, render_template, url_for

# creat an app instance named 'app'
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", time = datetime.datetime.utcnow())

    
@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/comments/')
def comments():
    commentss = ['This is the first comment.',
                'This is the second comment.',
                'This is the third comment.',
                'This is the fourth comment.'
                ]

    return render_template('comments.html', comments=commentss)
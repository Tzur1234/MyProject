from flask import Flask, render_template, request, url_for, flash, redirect
import os

app = Flask(__name__)

# Create a screte key for app
app.config['SECRET_KEY'] = os.urandom(24).hex()

## global veriable
messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]



@app.route('/')
def index():
    return render_template('index.html', messages=messages)

# ...

@app.route('/create/', methods=('GET', 'POST'))
def create():

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash("Give title !")
        elif not content:
            flash("Give content !")
        else:
            messages.append({"title": title, "content": content})
            return redirect(url_for('index'))
    return render_template("create.html")
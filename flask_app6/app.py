from flask import Flask, render_template, request, url_for, flash, redirect, abort
import sqlite3
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24).hex()  

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True



# open the connection to the database.db file 
def get_db_connection():
    # creat conn connection object you’ll be using to access the database
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(id):
    conn = get_db_connection()    
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (id,)).fetchone()

    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/')
def index():
    conn = get_db_connection()

    #fetchall() function  :  fetch all the rows of the query result
    posts = conn.execute('SELECT * FROM posts').fetchall()

    # close the connection 
    conn.close()

    #return a dictionary full of rows
    return render_template('index.html', posts=posts)


@app.route('/create/', methods=('GET', 'POST'))
def create():

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
    
        if not title or not content:
            flash("fill all the fields !")
        
        else:

            conn = get_db_connection()
            conn.execute("INSERT INTO posts (title,content) VALUES (?,?)", (title, content))

            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')



# edit post
# ...

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        elif not content:
            flash('Content is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


# ...

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


















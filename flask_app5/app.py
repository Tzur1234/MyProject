
# impot Flask object\class from flask package 
from flask import Flask, render_template, redirect, url_for, request
import logging

import os

# get the CourseForm object\class from forms.py (a moudel)
from forms import CourseForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()

courses_list = [{
    'title': 'Python 101',
    'description': 'Learn Python basics',
    'price': 34,
    'available': True,
    'level': 'Beginner'
    }]

@app.route('/', methods = ['POST', 'GET'])
def index():
    app.logger.info('form.validate_on_submit')
    form = CourseForm()
    if form.validate_on_submit():
        
        courses_list.append({'title': form.title.data,
                             'description': form.description.data,
                             'price': form.price.data,
                             'available': form.available.data,
                             'level': form.level.data
                             })
        return redirect(url_for('courses'))
    return render_template('index.html', form=form)
# ...

@app.route('/courses/')
def courses():
    return render_template('courses.html', courses_list=courses_list)

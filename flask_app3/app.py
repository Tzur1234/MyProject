from flask import Flask, render_template, abort
import logging 

app = Flask(__name__)

@app.route('/')
def index():
    app.logger.debug('get the index.html page')
    return render_template('index.html')



@app.route('/message/<int:i>')
def message(i):
    messages = ['Message Zero', 'Message One', 'Message Two' ]
    try:
        return render_template('message.html', message=messages[i])
    except IndexError:
        app.logger.error('the return_template is causing an IndexError')
        abort(500)

# specail decorator as handler for 404 error

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 400


# specail decorator as handler for 500 error

@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html'), 500


  
@app.route('/500')
def error500():
    abort(500)
















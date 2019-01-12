#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  	appCam.py
#  	based on tutorial ==> https://blog.miguelgrinberg.com/post/video-streaming-with-flask
# 	PiCam Local Web Server with Flask
# MJRoBot.org 19Jan18
import time,datetime,os
import subprocess

from flask import *

from SimpleCV import * 
from camera_pi import Camera

import sqlite3

DATABASE = '/tmp/flaskr2.db'
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = '123456'
 
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)	  

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/index')
def index():
	timeNow = time.asctime( time.localtime(time.time()) )
	
	templateData = {
      'time': timeNow,
	}
	return render_template('index.html', **templateData)

@app.route('/camera')
def cam():
	"""Video streaming home page."""
	timeNow = time.asctime( time.localtime(time.time()) )
	templateData = {
      'time': timeNow
	}
	return render_template('camera.html', **templateData)

 
def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

	
@app.route('/photo')			
def photo():
	
	subprocess.call("raspistill -o %s -t 100" % ("/home/pi/flask/IotWeb/static/image/test.jpg"), shell=True)
	timeNow = time.asctime( time.localtime(time.time()) )
	
	templateData = {
      'time': timeNow
	}
	return render_template('view.html', **templateData)

	
@app.route('/view')
def view():

	return render_template('view.html')
	

@app.route('/save')
def save():
	pname = "/home/pi/flask/IotWeb/photos/" + time.strftime("%Y%m%d%H%M%S",time.localtime()) + ".jpg"
	subprocess.call("mv %s %s" % ("/home/pi/flask/IotWeb/static/image/test.jpg", pname), shell=True)
	
	disp = Display() 
	
	while disp.isNotDone(): 
		segment = HaarCascade("face.xml")
		autoface = pname.findHaarFeatures(segment) 
		if ( autoface is not None ):
			face = autoface[-1].crop() 
			face.save(disp)
			face.save("/home/pi/flask/IotWeb/photos/myface.jpg") 

	
	timeNow = time.asctime( time.localtime(time.time()) )
	templateData = {
      'time': timeNow
	}
	return render_template('index.html', **templateData)
	
@app.route('/delete')
def delete():
	subprocess.call("rm -rf %s" % ("/home/pi/flask/IotWeb/static/image/test.jpg"), shell=True)
					
	timeNow = time.asctime( time.localtime(time.time()) )
	templateData = {
      'time': timeNow
	}
	return render_template('index.html', **templateData)


@app.route('/led_flush', methods=['POST'])
def led_flush():
    btn_name = get_btn_name(request)
    if btn_name == 'ON':
        arduino.flushOutput()
        arduino.write('5')
        print("The led is opened\n")
    elif btn_name == 'OFF':
        arduino.flushOutput()
        arduino.write('6')
        print("THe led is shutdowned\n")

    templateData = {}
    return render_template('led_flush.html', **templateData);
	

def get_btn_name(request):
    btn_name=""
    for key in request.form.keys():
        #print ("Button pressed:", key)
        btn_name = key
    return btn_name

@app.before_request
def before_request():
    g.db = connect_db()
    
	
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
	
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()	
    

	
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return render_template('login.html', error=error)


 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port =8080, debug=True, threaded=True)

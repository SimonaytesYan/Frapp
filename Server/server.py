import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import session
from nnc import *

UPLOAD_FOLDER = 'db'
ALLOWED_EXTENSIONS = {'jpg'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'app secret key'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file part')
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            print ("Start")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            l = what_difference()
            s = ''
            for i in l:
                s+= str(i) + ' '
            print (l)
            print (s) 
            return s
    #return what_difference1()

@app.route('/')
def index():
    if 'counter' in session:
        session['counter'] += 1
    else:
        session['counter'] = 1
    return 'Counter: '+str(session['counter'])

#sess = Session()
#app.secret_key = 'super secret key'
#app.config['SESSION_TYPE'] = 'filesystem'

#sess.init_app(app)

app.debug = True
app.run()
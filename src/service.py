import os
import re
from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask import jsonify
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_ ,DateTime
from datetime import datetime
import sys
# from jarvis.chat import manager
sys.path.insert(1, './chat/')
import manager

#detect intent
from detect_intent import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY']=os.urandom(24)
db = SQLAlchemy(app)

#user table store user information
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return '<User %r>' % self.username

#history table store chat log question and answer
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(800))
    question = db.Column(db.String(800))
    answer = db.Column(db.String(800))
    time = db.Column(DateTime, nullable=False)

@app.before_first_request
def create_db():
    if os.path.exists("src/data.db"):
        return
    # db.drop_all()
    db.create_all()
	
	#create admin, this line cannot be fixed.
    admin = User(username='admin', password='admin', email='admin@admin.com')
    db.session.add(admin)
	
	#insert some history example
    historys = [
        History(username='user1', question='hello', answer='hello',time=datetime.now()),
        History(username='user2', question='prerequisite of COMP9024', answer='COMP9021',time=datetime.now()),
    ]
    db.session.add_all(historys)
	
	#insert some user example
    guestes = [User(username='guest1', password='guest1', email='guest1@example.com'),
               User(username='guest2', password='guest4', email='guest4@example.com')]
    db.session.add_all(guestes)
    db.session.commit()

#check if the user name and password are right
def valid_login(username, password):
    user = User.query.filter(and_(User.username == username, User.password == password)).first()
    if user:
        return True
    else:
        return False

#check if the user name has been registered
def valid_regist(username, email):
    user = User.query.filter(or_(User.username == username, User.email == email)).first()
    if user:
        return False
    else:
        return True

#for security, make sure some page can only be accessed after login
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # if g.user:
        if session.get('username'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login', next=request.url))
    return wrapper

#return home page
@app.route('/')
def home():
    return render_template('mainpage.html', username=session.get('username'))

#login api
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
	#login function
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            session['username'] = request.form.get('username')
            return redirect(url_for('home'))
        else:
            error = 'wrong username or password！'
	#access login page
    return render_template('login.html', error=error)

#chat api
@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
	#access chat page
    if request.method == 'GET':
        return render_template('chat.html',username=session.get('username'))
	#chat with the bot
    else:
		#get question content from frontend
        input_text=request.values['question']
        # print('input is ', input_text)
        # processed_input = re.sub(r'([a-zA-Z]{4})([0-9])([0-9]{3})', r'\1 - \2 - \3', input_text)
        processed_input = input_text
        # print(input_text)
        username = session.get('username')
        chatbot_response = detect_intents(processed_input, username).fulfillment_text
		#store chat history
        his= History(username=session.get('username'), question=input_text, answer=chatbot_response, time= datetime.now())
        db.session.add(his)
        db.session.commit()
        # print(input)
		#return chatbot response
        return jsonify({"response": chatbot_response})

#logout api
@app.route('/logout')
def logout():
	#pop user session and return home page
    session.pop('username', None)
    return redirect(url_for('home'))

#sign in api
@app.route('/regist', methods=['GET', 'POST'])
def regist():
    error = None
	#sign in function
    if request.method == 'POST':
		#check if the password are equal
        if request.form['password1'] != request.form['password2']:
            error = 'password are different！'
		#check if user has been registed
        elif valid_regist(request.form['username'], request.form['email']):
            user = User(username=request.form['username'], password=request.form['password1'],
                        email=request.form['email'])
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('login'))
        else:
            error = 'username has been used'

    return render_template('signup.html', error=error)

@app.route('/history', methods=['GET','POST'])
@login_required
def history():
    username=session.get('username')
    print(username)
    if request.method == 'GET':
		# return history data to frontenf=d
        if username == 'admin':
            his = History.query.all()
            #his = db.execute('SELECT * FROM History').fetchall()
            return render_template('review.html', his=his, username=username ,admin='admin')
        else:
            his = History.query.filter_by(username=username).all()
            #his = db.execute('SELECT * FROM History WHERE username == username').fetchall()
            return render_template('review.html', his=his, username=username)
	#if the method is POST, get the question and description 
    else:
        que = request.values['question']
        des = request.values['description']


        intents = detect_intents(que, SESSION_ID='tmp').parameters.fields['Concept'].string_value
        manager.create_or_update(intents, des)
        return jsonify({"response": "change successfully！"})



if __name__ == '__main__':
    start = detect_intents('Hello', 'start').fulfillment_text
    app.run(debug=True)
   
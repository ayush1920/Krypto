from flask import Flask,render_template, request, redirect, flash,make_response
import secret_key
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import uuid
import datetime
from functools import wraps
import click._compat
import requests
from time import time
from threading import Thread
import monitor
from SQLClasses import Alerts, User, db
from flask_apscheduler import APScheduler

app = Flask(__name__)
scheduler = APScheduler()

app.config['SECRET_KEY'] = secret_key.init()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)

def log(text):
    '''Uses click library to print formatted text in console.
       Logs the output for debuggig'''
    click.secho(str(text), fg='green')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        else:
            if 'token' in request.cookies:
                token = request.cookies['token']
        
        if not token:
            return {'message' : 'Token is missing!'}, 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
                
        except:
            return {'message' : 'Token is invalid!'}, 401
        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/')
def home():
    return "home"

@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.admin:
        return {'message' : 'Cannot perform that function!'}

    data = request.get_json()
    if not data or not(data.get('email', False) and data.get('password', False)):
        return {'message': 'data invalid'}
    user = User.query.filter_by(email = data['email']).first()
    if user:
        return {'message': 'user already exists'}

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), email=data['email'], password=hashed_password, admin = False)
    db.session.add(new_user)
    db.session.commit()
    return {'message' : 'New user created!'}

@app.route('/login')
def login():

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(email=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' :  user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY']).decode('UTF-8')
        response = make_response( {'token' : token}  )
        response.set_cookie( "token",  token)
        return response

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

@app.route('/alerts/create', methods = ["POST"])
@token_required
def create_alert(current_user):
    data = request.get_json()
    if not data or not(data.get('value', False)):
        return {'message': 'data invalid'}
    if not isinstance(data['value'], int):
        return {'message': 'value not numeric invalid'}

    email = current_user.email
    # if alert exist do not create new
    greater = monitor.crypto.crypto_value <= data['value']
    alert = Alerts.query.filter_by(email = email, greater = greater ,value = data['value'], deleted = False).first()
    if alert:
        return {'message': 'alert with same value exists'}
    new_alert = Alerts(email = email, crypto = 'btc', value = data['value'],  greater = greater, status = "created", deleted = False, triggered = False, 
    last_triggered = int(time()) - 21600 )
    db.session.add(new_alert)
    db.session.commit()
    return {'message': 'alert created'}

@app.route('/alerts/delete', methods=['DELETE'])
@token_required
def delete_alert(current_user):
    data = request.get_json()
    if not data or not(data.get('value', False)):
        return {'message': 'data invalid'}
    if not isinstance(data['value'], int):
        return {'message': 'value not numeric invalid'}

    email = current_user.email
    alert = Alerts.query.filter_by(email=email,  value = data['value'], deleted = False).first()
    if not alert:
        return {'message': 'no alert found'}
    alert.status = "deleted"
    alert.deleted = True
    db.session.commit()
    return {'message': 'alert deleted'}

@app.route('/alerts/fetch', methods=['GET'])
@token_required
def fetch_alert(current_user):
    page = request.args.get('page', default = 1, type = int)
    per_page =  request.args.get('per_page', default = 10, type = int)
    status =  request.args.get('status', default = '', type = str)

    email = current_user.email

    if status:
        alerts = Alerts.query.filter_by(email = email , status = status.lower()).paginate(page,per_page,error_out=False)
    else:
        alerts = Alerts.query.filter_by(email = email).paginate(page,per_page,error_out=False)

    if not alerts:
        return {'message': 'no alert found'}
    res = []
    for alert in alerts.items:
        res.append({'crypto': alert.crypto, 'value': alert.value, 'status': alert.status})
    return {'result':res}


if __name__ =='__main__':
    db.create_all()
    scheduler.add_job(id = 'Scheduled task', func = monitor.get_data, trigger = 'interval', seconds = 5)
    scheduler.start()
    app.run(debug=True, use_reloader=False)

import requests
import time
import click._compat
import emailconf
import os
from threading import Thread
from SQLClasses import Alerts, User, db
from redis import Redis
from rq import Queue
from time import time
from sqlalchemy import and_, or_

q = Queue(connection=Redis())

class Status:
    def __init__(self, lower_limit = 0, upper_limit = 0, crypto_value = 0):
        self.crypto_value = crypto_value

crypto = Status()

def configure_email():
    filename = "email.conf"
    s = {}
    if os.path.isfile(filename):
        with open(filename) as f:
            try:
                s = eval(f.read())
                email = s['email']
                password = s['password']
            except:
                s = {}
    if s:
        return email, password

    email = input('Enter Email to send email from: ')
    password = input('Enter password for email: ')
    with open(filename, 'w') as f:
        f.write(str({'email': email, 'password': password}))
    return email, password

def log(text):
    '''Uses click library to print formatted text in console.
       Logs the output for debuggig'''
    click.secho(str(text), fg='green')

def email_user(data):
    email, text = data
    log(email)
    log(text)
    server.sendmail(sender_email, email, str(text))
    

sender_email, password = configure_email()
server = emailconf.init(sender_email, password)


def get_data():
    '''Fetch data every 50 seconds'''
    res = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=50&page=1&sparkline=false')
    res = res.json()
    data = {i['symbol'].lower() : int(i['current_price']) for i in res}

    # data = {"btc":119}
    log(data['btc'])
    value = data['btc']
    crypto.crypto_value = value
        
    alerts = Alerts.query.filter(and_(Alerts.triggered == False, Alerts.deleted == False ,  Alerts.greater == True , Alerts.value <= value ,
    Alerts.last_triggered < int(time()) - 21600)).all()
    for alert in alerts:
        alert.triggered = True
        alert.last_triggered = int(time())
        alert.status = 'triggered'
        db.session.commit()
        text = f'Price Alert!!! BTC now above {value}'
        q.enqueue(email_user, (alert.email, text))    

    alerts = Alerts.query.filter(and_(Alerts.triggered == False, Alerts.deleted == False ,  Alerts.greater == False , Alerts.value > value ,
    Alerts.last_triggered < int(time()) - 21600)).all()
    for alert in alerts:
        alert.triggered = True
        alert.last_triggered = int(time())
        alert.status = 'triggered'
        db.session.commit()
        text = f'Price Alert!!! BTC now below {value}'
        q.enqueue(email_user, (alert.email, text))
        

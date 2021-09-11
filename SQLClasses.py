from SharedDB import  db

class User(db.Model):
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Alerts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    crypto = db.Column(db.String(50))
    value = db.Column(db.Integer)
    greater =  db.Column(db.Boolean) 
    status = db.Column(db.String(50))
    deleted = db.Column(db.Boolean) 
    triggered =  db.Column(db.Boolean)
    last_triggered = db.Column(db.Integer)

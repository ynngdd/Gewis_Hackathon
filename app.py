from flask import Flask, Response, make_response, redirect, render_template, request, flash, session, url_for, request, jsonify
import json
import enum
from flask_sqlalchemy import SQLAlchemy
import datetime
from dataclasses import dataclass


app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["SECRET_KEY"] = '571ebf8e13ca209536c29be68d435c00'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///registration.db'
db = SQLAlchemy(app)

class Ugrency(enum.Enum):
    urgent = 0
    normal = 1
    low = 2

@dataclass
class Issue(db.Model):
    id: int
    problem: str
    urgency: str
    location: str
    aval_time_start: datetime
    aval_time_end: datetime
    taken: bool
    done: bool

    id = db.Column(db.Integer, primary_key =True)
    problem = db.Column(db.String(100), nullable = False)
    urgency = db.Column(db.String(100), nullable = False)
    location = db.Column(db.String(100), nullable = False)
    aval_time_start = db.Column(db.DateTime, default=db.func.now())
    aval_time_end = db.Column(db.DateTime, default=db.func.now())
    taken = db.Column(db.Boolean(), unique=False, default=False)
    done = db.Column(db.Boolean(), unique=False, default=False)



@app.route('/api-get')
def api():
    issues = Issue.query.all()
    return jsonify(issues)

@app.route('/api-post', methods=['POST'])
def postmethod():
    data = request.get_json()
    print(data)
    return jsonify(data)


if __name__ == '__main__':
    issue1 = Issue(problem="PROBLEM", location="KLETA MAIKA BALGARIQ", urgency="normal",aval_time_start = datetime.datetime.now(),aval_time_end = datetime.datetime.now(), taken=True, done=False)
    db.create_all()
    db.session.add(issue1)
    db.session.commit()
    app.run(debug=False, host='0.0.0.0')

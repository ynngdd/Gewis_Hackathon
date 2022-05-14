from flask import Flask, Response, make_response, redirect, render_template, request, flash, session, url_for, request, jsonify
import json
import enum
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_cors import CORS
from dataclasses import dataclass

app = Flask(__name__)
CORS(app)

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

    id = db.Column(db.Integer, primary_key=True)
    problem = db.Column(db.String(100), nullable=True, default= "Big Problem")
    urgency = db.Column(db.String(100), nullable=True, default="urgent")
    location = db.Column(db.String(100), nullable=True, default="Main office")
    aval_time_start = db.Column(db.DateTime, default=db.func.now())
    aval_time_end = db.Column(db.DateTime, default=db.func.now())
    taken = db.Column(db.Boolean(), unique=False, default=False)
    done = db.Column(db.Boolean(), unique=False, default=False)


@app.route('/api-get')
def api():
    issues = Issue.query.all()
    return jsonify(issues)


@app.route('/taken', methods=['POST'])
def postmethod_taken():
    data = request.get_json(force=True)
    issue = Issue.query.get(data["id"])
    print(issue)
    for x in data:
        print(x)
        print(data[x])
        setattr(issue, x, data[x])
    db.session.add(issue)
    db.session.commit()
    return jsonify(data)


@app.route('/done', methods=['POST'])
def postmethod():
    data = request.get_json(force=True)
    issue = Issue.query.get(data["id"])
    print(issue)
    for x in data:
        print(x)
        print(data[x])
        setattr(issue, x, data[x])
    db.session.add(issue)
    db.session.commit()
    return jsonify(data)

@app.route('/add', methods=['POST'])
def add():
    data = request.get_json(force=True)
    issue = Issue()
    print(issue)
    for x in data:
        if x!="id":
            print(x)
            print(data[x])
            setattr(issue, x, data[x])

    db.session.add(issue)
    db.session.commit()
    return jsonify(data)


if __name__ == '__main__':
    # issue1 = Issue(problem="PROBLEM", location="KLETA MAIKA BALGARIQ", urgency="normal",aval_time_start = datetime.datetime.now(),aval_time_end = datetime.datetime.now(), taken=True, done=False)
    # db.create_all()
    # db.session.add(issue1)
    # db.session.commit()
    app.run(debug=True, host='0.0.0.0')
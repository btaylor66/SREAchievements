#!/usr/bin/env python

from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SREAchievements.sqlite3'

db = SQLAlchemy(app)

# from sqlalchemy import Column, Integer, String


class Teams(db.Model):

    team_id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    team_name = db.Column(db.String(40), unique=False)

    users = db.relationship("Users", back_populates="team")

    def __init__(self, team_name):
        self.team_name = team_name


class Users(db.Model):

    user_id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    username = db.Column(db.String(40), unique=True)
    fullname = db.Column(db.String(40))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)

    team = db.relationship("Teams", back_populates="users")
    # team = relationship("Teams")

    def __init__(self, username, fullname, team_id):
        self.username = username
        self.fullname = fullname
        self.team_id = team_id


@app.route('/')
def show_all():
    return render_template('show_all.html', students=Users.query.all())


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['username'] or not request.form['fullname'] or not request.form['team']:
            flash('Please enter all the fields', 'error')
        else:
            student = Users(request.form['username'], request.form['fullname'],
                request.form['team'])

            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

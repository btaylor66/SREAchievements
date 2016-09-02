#!/usr/bin/env python

from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SREAchievements.sqlite3'
app.config['SECRET_KEY'] = "ThisIs@randomString!!"

db = SQLAlchemy(app)

# from sqlalchemy import Column, Integer, String


class Teams(db.Model):

    team_id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    team_name = db.Column(db.String(40), unique=False)

    users = db.relationship("Users", back_populates="team")
    # users = db.relationship("Users", backref="team", lazy='dynamic')
    # users = db.relationship("Users")

    # def __init__(self, team_name,users):
    #    self.team_name = team_name
    #    self.users = users

    def __repr__(self):
        return "<Team(team_name='%s')>" % (
            self.team_name)

class Users(db.Model):

    user_id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    username = db.Column(db.String(40), unique=True)
    fullname = db.Column(db.String(40))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)

    team = db.relationship("Teams", back_populates="users")
    # team = db.relationship("Teams")

    # def __init__(self, username, fullname, team_id, team):
    #    self.username = username
    #    self.fullname = fullname
    #    self.team_id = team_id
    #    self.team = team

    def __repr__(self):
        return "<Team(username='%s', fullname='%s'), team_id='%s', team='%s'>" % (
            self.username, self.fullname, self.team_id, self.team)

@app.route('/')
def show_all():
    return render_template('show_all.html', users=Users.query.all(), teams=Teams.query.all())


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['username'] or not request.form['fullname'] or not request.form['team']:
            flash('Please enter all the fields', 'error')
        else:
            user = Users(username=request.form['username'], fullname=request.form['fullname'],
                        team=Teams(team_name=request.form['team']))

            db.session.add(user)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

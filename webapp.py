""" This is the core webapp

Requires python packages
 *

"""

import logging
import os
from flask import Flask, request, flash, url_for, redirect, render_template

from sreachievementswebapp.dbmodels import db
from sreachievementswebapp.models import person, team, achievement

import flask_restless

try:
    from flask_superadmin import Admin
except Exception:
    logging.warning('missing flask.ext.superadmin')

log = logging.getLogger(__name__)


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SREAchievements.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "ThisIs@randomString!!"

db.app = app
db.init_app(app)
db.create_all()


def add_user(uname, fname, tname):
    p = person.query(person.id).filter(exists().where(person.username==uname)).all()
    if not(p):
        print('Creating username: %s, fullname: %s, team_name: %s' % (uname,fname,tname))
        p = person(username=uname, fullname=fname)
        session.add(p)
    else:
        print('User %s already exists' % uname)
    session.commit()


def create_teams():
    # I know this can be better, but trying to limit the number of issues I am trying to figure out ;/
    team_list = ['Talent Solutions', 'Marketing Solutions']
    for team in team_list:
        session.add(teams(team_name=team))
    session.commit()


@app.route('/')
def show_all():
    return render_template('show_all.html', users=person.Person.query.all(), teams=team.Team.query.all())


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['username'] or not request.form['fullname']:
            flash('Please enter all the fields', 'error')
        else:
            user = person.Person(username=request.form['username'], fullname=request.form['fullname'])

            db.session.add(user)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')


if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)

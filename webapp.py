""" This is the core webapp

Requires python packages
 *

"""

import logging
import os
from flask import Flask, request, flash, url_for, redirect, jsonify, render_template

from sreachievementswebapp.dbmodels import db
from sreachievementswebapp.models import person, team, achievement

import flask_restless

try:
    # from flask_superadmin import Admin
    from flask_admin import Admin
    from flask_admin.contrib.sqla import ModelView
except Exception:
    logging.warning('missing flask_superadmin')

log = logging.getLogger(__name__)


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SREAchievements.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "ThisIs@randomString!!"

admin = Admin(app, name='sreachievements', template_mode='bootstrap3')


db.app = app
db.init_app(app)
db.create_all()

admin.add_view(ModelView(person.Person, db.session))
admin.add_view(ModelView(team.Team, db.session))
admin.add_view(ModelView(achievement.Achievement, db.session))

def add_user(uname, fname, tname):
    p = person.query(person.id).filter(exists().where(person.username==uname)).all()
    if not(p):
        print('Creating username: %s, fullname: %s, team_name: %s' % (uname,fname,tname))
        p = person(username=uname, fullname=fname)
        session.add(p)
    else:
        print('User %s already exists' % uname)
    session.commit()


@app.route('/')
def show_all():
    return render_template('show_all.html', users=person.Person.query.all(), teams=team.Team.query.all(), achievement=achievement.Achievement.query.all())


@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        if not request.form['username'] or not request.form['fullname']:
            flash('Please enter all the fields', 'error')
        else:
            user = person.Person(username=request.form['username'], fullname=request.form['fullname'])

            db.session.add(user)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new_user.html')


@app.route('/new_achievement', methods=['GET', 'POST'])
def new_achievement():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['description']:
            flash('Please enter all the fields', 'error')
        else:
            badge = achievement.Achievement(name=request.form['name'], description=request.form['description'], image=request.form['image'])

            db.session.add(badge)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new_achievement.html')


@app.route('/user/<name>')
def user(name):
    user = person.Person.query.filter_by(username=name).first()
    if user == None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user)


# Creating a base json api to insert/delete/get user info
def person_fetch_preprocessor(
    filters=None, sort=None, group_by=None, single=None, **kw):
    """LazycreationofPerson()iftherequesteduserismissing.

    This will also lookup all the users achievements
    """
    print("person_fetch:{0}".format(locals()))

    usernames = []
    if filters:
        for filter_dict in filters:
            if filter_dict.get('name', '') not in ('username', 'firstname', 'lastname', 'fullname'):
                continue
            usernames = filter_dict.get('val')

            # wewanttooperateronalistofusernames,
            # Iftheusernameisasingleuser,thenworksomemagic
            if isinstance(usernames, (str, unicode)):
                usernames = [usernames]

    person_resource_id = kw.get('resource_id')
    if person_resource_id:
        usernames.append(person_resource_id)

    # Expandusernameswithsearchresults
    new_usernames = []
    for username in usernames:
        username = username.replace('%', '')
        print("person_fetch:{0}".format(username))
        found_usernames = search_username(username).keys()
        new_usernames += found_usernames
        if found_usernames:
            print("{0}>{1}".format(username, found_usernames))

    for username in new_usernames:
        print("MakingPERSON:{0}".format(username))
        try:
            user = person.Person(username)
            db.session.add(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            pass



api_manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

person_preprocessors = {
    'GET_COLLECTION': [person_fetch_preprocessor],
    'GET_RESOURCE': [person_fetch_preprocessor]
}

api_manager.create_api(person.Person,
                       collection_name='users',
                       preprocessors=person_preprocessors,
                       primary_key = 'username')

api_manager.create_api(team.Team,
                       collection_name='teams',
                       primary_key = 'id')

api_manager.create_api(achievement.Achievement,
                       collection_name='achievements',
                       primary_key = 'id')

if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)

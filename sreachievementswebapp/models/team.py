"""Database model for a team

"""

import collections
import operator

from sreachievementswebapp.dbmodels import db


class Team(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)

    # users = db.relationship("Users")
    # users = db.relationship("Users", backref="team", lazy='dynamic')
    # users = db.relationship("Users")

    def __init__(self, name):
        self.name = name


    # def __repr__(self):
    #    return "<Team(team_name='%s')>" % (
    #        self.team_name)
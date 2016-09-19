"""Database model for a person

"""

import collections
import operator

from sreachievementswebapp.dbmodels import db

from sqlalchemy.ext.hybrid import hybrid_property

m2m_person_achievement = db.Table(
    'm2m_person_achievement',
    db.Column('achievement_id', db.Integer, db.ForeignKey('achievement.id')),
    db.Column('person_id', db.Integer, db.ForeignKey('person.id')),
    db.PrimaryKeyConstraint('achievement_id', 'person_id')
)


class Person(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    fullname = db.Column(db.String(50))
    # team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=True)
    achievements = db.relationship('Achievement', secondary=m2m_person_achievement, backref='Person')

    # team = db.relationship("Teams", back_populates="users")
    # team = db.relationship("Teams")

    known_achievements = []

    # def __init__(self, username, fullname, team_id, team):
    def __init__(self, username, fullname):
        self.username = username
        self.fullname = fullname
        # self.team_id = team_id
        # self.team = team

    # def __repr__(self):
    #    return "<Team(username='%s', fullname='%s'), team_id='%s', team='%s'>" % (
    #        self.username, self.fullname, self.team_id, self.team)


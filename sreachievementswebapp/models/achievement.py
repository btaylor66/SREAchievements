"""Database model for an achievement

"""

import collections
import operator

from sreachievementswebapp.dbmodels import db

m2m_achievement_person = db.Table(
    'm2m_achievement_person',
    db.Column('person_id', db.Integer, db.ForeignKey('person.id')),
    db.Column('achievement_id', db.Integer, db.ForeignKey('achievement.id')),
    db.PrimaryKeyConstraint('person_id', 'achievement_id')
)


class Achievement(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(50))
    people = db.relationship('Person', secondary=m2m_achievement_person, backref='Achievement')

    # team = db.relationship("Teams", back_populates="users")
    # team = db.relationship("Teams")

    known_achievements = []

    def __init__(self, name, description):
        self.name = name
        self.description = description
        # self.team_id = team_id
        # self.team = team

    # def __repr__(self):
    #    return "<Team(username='%s', fullname='%s'), team_id='%s', team='%s'>" % (
    #        self.username, self.fullname, self.team_id, self.team)

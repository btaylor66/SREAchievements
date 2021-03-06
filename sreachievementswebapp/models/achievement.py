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
    image = db.Column(db.String(100), nullable=True)
    people = db.relationship('Person', secondary=m2m_achievement_person, backref='Achievement')

    # team = db.relationship("Teams", back_populates="users")
    # team = db.relationship("Teams")

    known_achievements = []

    def __init__(self, name, description, image):
        self.name = name
        self.description = description
        self.image = image
        # self.team_id = team_id
        # self.team = team

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
        'id'    : self.id,
        'name'  : self.name,
        'description'   : self.description,
        'image' : self.image
        }
    # def __repr__(self):
    #    return "<Team(username='%s', fullname='%s'), team_id='%s', team='%s'>" % (
    #        self.username, self.fullname, self.team_id, self.team)

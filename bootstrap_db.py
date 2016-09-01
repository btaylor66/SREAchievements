#!/usr/bin/env python
#import sqlite3
from sqlalchemy import Column, Integer, String, create_engine, Sequence, ForeignKey, exists
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


# from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=False)

Session = sessionmaker(bind=engine)

Base = declarative_base()

#from sqlalchemy import Column, Integer, String
class Teams(Base):
    __tablename__ = 'teams'

    team_id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    team_name = Column(String(40), unique=False)

    # not sure i need this... still trying to figure it out
    users = relationship("Users", back_populates="team")
    #users = relationship("Users")

    def __repr__(self):
        return "<Team(team_name='%s')>" % (
            self.team_name)

#from sqlalchemy import Column, Integer, String
class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(40), unique=True)
    fullname = Column(String(40))
    team_id = Column(Integer, ForeignKey('teams.team_id'), nullable=False)

    team = relationship("Teams", back_populates="users")
    #team = relationship("Teams")

    def __repr__(self):
        return "<Team(username='%s', fullname='%s'), team_id='%s'>" % (
                            self.username, self.fullname, self.team_id)

Base.metadata.create_all(engine)

def add_user(uname, fname, tname):
    p = session.query(Users.user_id).filter(exists().where(Users.username==uname)).all()
    if not(p):
        print('Creating username: %s, fullname: %s, team_name: %s' % (uname,fname,tname))
        p = Users(username=uname, fullname=fname, team=Teams(team_name=tname))
        session.add(p)
    else:
        print('User %s already exists' % uname)
    session.commit()

def create_teams():
    # I know this can be better, but trying to limit the number of issues I am trying to figure out ;/
    team_list = ['Talent Solutions', 'Marketing Solutions']
    for team in team_list:
        session.add(Teams(team_name=team))
    session.commit()

session = Session()
ed_user = Users(username='brtaylor', fullname='Brandon Taylor', team=Teams(team_name='Talent Solutions'))
session.add(ed_user)

create_teams()
add_user('brtaylor', 'Brandon Taylor', 'Talent Solutions')
add_user('dlawrence', 'Danny Lawrence', 'Talent Solutions')
#session.add_all([
#    Users(username='dlawrenc', fullname='Danny Lawrence', team=Teams(team_name='Talent Solutions')),
#    Users(username='vnosovsk', fullname='Vadim Nosovsky', team=Teams(team_name='Talent Solutions')),
#    Users(username='rdoyle', fullname='Ryan Doyle', team=Teams(team_name='Talent Solutions')),
#    Users(username='jopatterson', fullname='Jon Patterson', team=Teams(team_name='Talent Solutions')),
#    Users(username='wwest', fullname='Bill West', team=Teams(team_name='Talent Solutions')),
#    Users(username='xoli', fullname='Xiaolu Li', team=Teams(team_name='Talent Solutions'))
#])

print("----Results----")
print("------Users----")
for user in session.query(Users).order_by(Users.user_id):
    print(user.username, user.fullname, user.team)
print("------Teams----")
for team in session.query(Teams).order_by(Teams.team_id):
    print(team.team_id,team.team_name)
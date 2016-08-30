#!/usr/bin/env python
import sqlite3
from sqlalchemy import *
#from flask_sqlalchemy import SQLAlchemy

#import sqlalchemy

db = create_engine('sqlite:///SREAchievments.db')

db.echo = False  # Try changing this to True and see what happens

metadata = MetaData(db)

# if not db.dialect.has_table(db, 'teams'):
teams = Table('teams', metadata,
    Column('team_id', Integer, primary_key=True),
    Column('team_name', String(40)),
)
teams.create(checkfirst=True)
t = teams.insert()
t.execute(name='Talent Solutions')

# if not db.dialect.has_table(db, 'users'):
users = Table('users', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', String(40), unique=True),
    Column('full_name', String(40)),
    Column('sre_team', ForeignKey("teams.team_id"), nullable=False),
)
users.create(checkfirst=True)
i = users.insert()
i.execute(user_name='brtaylor',full_name='Brandon Taylor', sre_team='Talent Solutions')
i.execute({'user_name': 'dlawrenc', 'full_name': 'Danny Lawrence', 'sre_team': 'Talent Solutions'},
          {'user_name': 'vnosovsk', 'full_name': 'Vadim Nosovsky', 'sre_team': 'Talent Solutions'},
          {'user_name': 'rdoyle', 'full_name': 'Ryan Doyle', 'sre_team': 'Talent Solutions'},
          {'user_name': 'xoli', 'full_name': 'Xiaolu Li', 'sre_team': 'Talent Solutions'},
          {'user_name': 'jopatterson', 'full_name': 'Jon Patterson', 'sre_team': 'Talent Solutions'},
          {'user_name': 'wwest', 'full_name': 'Bill West', 'sre_team': 'Talent Solutions'})




s = users.select()
rs = s.execute()

row = rs.fetchone()
print('Id:', row[0])
print('Name:', row['user_name'])
print('Team:', row.sre_team)

for row in rs:
    print(row.user_name, 'is', row.sre_team)

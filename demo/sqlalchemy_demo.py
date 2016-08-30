#!/usr/bin/env python
import sqlite3
from sqlalchemy import *
#from flask_sqlalchemy import SQLAlchemy

#import sqlalchemy

db = create_engine('sqlite:///tutorial.db')

db.echo = False  # Try changing this to True and see what happens

metadata = MetaData(db)

users = Table('users', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('name', String(40)),
    Column('age', Integer),
    Column('password', String),
)
users.create()

i = users.insert()
i.execute(name='Mary', age=30, password='secret')
i.execute({'name': 'John', 'age': 42},
          {'name': 'Susan', 'age': 57},
          {'name': 'Carl', 'age': 33})

s = users.select()
rs = s.execute()

row = rs.fetchone()
print('Id:', row[0])
print('Name:', row['name'])
print('Age:', row.age)
print('Password:', row[users.c.password])

for row in rs:
    print(row.name, 'is', row.age, 'years old')

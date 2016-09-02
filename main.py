#!/usr/bin/env python

import sqlite3
from sqlalchemy import *
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    db = create_engine('sqlite:///SREAchievments.db')
    metadata = MetaData()
    metadata.reflect(db)
    # we can then produce a set of mappings from this MetaData.
    Base = automap_base(metadata=metadata)

    # calling prepare() just sets up mapped classes and relationships.
    Base.prepare()

    teams = Base.classes.teams
    users = Base.classes.users

    u1 = session.query(users).first()
    print (u1.address_collection)
    s = users.select()
    rs = s.execute()

    row = rs.fetchone()
    print('Id:', row[0])
    print('Name:', row['user_name'])
    print('Team:', row.sre_team)

    for row in rs:
        print(row.user_name, 'is', row.sre_team)
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
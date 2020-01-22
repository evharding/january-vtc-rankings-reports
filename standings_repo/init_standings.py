import os
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker

import base, rower, standings_sample
Base = base.Base

db_name = 'alembic_sample.sqlite'
if os.path.exists(db_name):
    os.remove(db_name)

engine = create_engine('sqlite:///' + db_name)

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
print("Finished!")

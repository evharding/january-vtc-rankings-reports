from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from standings_repo.base import Base
from standings_repo.rower import Rower
from standings_repo.standings_sample import StandingsSample as SS
db_name = 'alembic_sample.sqlite'
engine = create_engine('sqlite:///' + db_name)

Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.bind = engine

def get_rower_by_name(session, name):
  return session.query(Rower).filter(Rower.name == name).first()

def add_rower(session, name, club, age, sex, location='N/A'):
  new_rower = Rower(name=name, rowing_club=club, age=age, sex=sex)
  if not session.query(Rower, Rower.name).filter(Rower.name == name).first():
    session.add(new_rower)

def add_standing_sample(session, date_fetched, meters_total, ranking, rower_id):
  new_sample = SS(date_fetched=date_fetched, meters_total=meters_total, ranking=ranking, rower_id=rower_id)
  session.add(new_sample)

def check_for_sample(session, date_fetched, rower_id):
  return session.query(SS).filter(SS.date_fetched == date_fetched).filter(SS.rower_id == rower_id).first()
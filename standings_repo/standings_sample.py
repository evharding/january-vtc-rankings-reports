from sqlalchemy import Column, DateTime, Integer, ForeignKey, Sequence
from standings_repo.base import Base

class StandingsSample(Base):
    __tablename__='standings'
    date_fetched = Column(DateTime, primary_key=True)
    meters_total = Column(Integer)
    ranking = Column(Integer)
    rower_id = Column(Integer, ForeignKey('rower.id'), primary_key=True)

    def __repr__(self):
        return f'<StandingsSample (date_fetched={self.date_fetched}, meters_total={self.meters_total}, ranking={self.ranking}, rower_id={self.rower_id})'
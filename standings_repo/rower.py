from sqlalchemy import Column, String, Integer, Sequence
from standings_repo.base import Base

class Rower(Base):
    __tablename__='rower'
    id = Column(Integer, Sequence('rower_id_seq'),primary_key=True)
    name = Column(String(100))
    location = Column(String(100))
    age = Column(Integer)
    sex = Column(String(1))
    rowing_club = Column(String(100))

    def __repr__(self):
        return f'<Rower(name={self.name}, age={self.age}, rowing_club={self.rowing_club}, location={self.location}, id={self.id})>'
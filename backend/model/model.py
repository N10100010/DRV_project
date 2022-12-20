import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Interval

# logging stuff
import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

# In-memory
# engine = create_engine("sqlite:///:memory:", echo=True)

# sqlite file relative path
# engine = create_engine("sqlite:///foo.sqlite", echo=True)

# postgres
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/rowing", echo=True)

Session = sessionmaker(bind=engine)

# connect will actually establish a connection or create/load the sqlite file
# engine.connect()

Base = declarative_base()


"""
TODO:
    - world-rowing GUIDs -> As String or Postgres UUID ?
    - race data (high res)
    - Specify Not Null Columns
    - add backref / back_populates for easy access
    - add athlete names
    - add progression string
    - Consider foreign key checking via constraints
    - Define Indexes
    - Ask DRV: Time resolution (milli, micro) !!! -> seems to be millisec -> research what res postgres' INTERVAL has
    - No data source hints are written into db (?)
    - INCLUDE PDFs!!! -> More maximalist apporach


https://worldrowing.com/event/2022-world-rowing-cup-iii
https://world-rowing-api.soticcloud.net/stats/api/race/?include=racePhase%2Cevent.competition.competitionType%2Cevent.competition.competitionType.competitionCategory%2Cevent.boatClass&filter%5Bevent.competitionId%5D=b56cf9a5-a7d3-4e64-9571-38218f39413b&sort%5Bdate%5D=asc
"""


class Athletes(Base):
    __tablename__ = "athletes"

    id = Column(Integer, primary_key=True)

    full_name = Column(String)
    birthdate = Column(Date)
    gender_id = Column(Integer) # TODO: gender table

    # TODO: country?


class Boat_Classes(Base):
    __tablename__ = "boat_classes"

    id = Column(Integer, primary_key=True)
    
    abbreviation = Column(String, nullable=False)
    display_name = Column(String, nullable=False)

    gender_id = Column(Integer) # TODO: gender table


class Competition_Classes(Base):
    __tablename__ = "competition_classes"

    id = Column(Integer, primary_key=True)

    name = Column(String)
    abbreviation = Column(String)


class Competitions(Base):
    __tablename__ = "competitions"

    id = Column(Integer, primary_key=True)
    competition_class_id = Column(Integer, ForeignKey("competition_classes.id"))

    name = Column(String)

    start_date = Column(Date)
    end_date = Column(Date)

    venue_country = Column(String(length=3))
    venue_city = Column(String) # TODO: Normalize location data? Example https://world-rowing-api.soticcloud.net/stats/api/competition/b56cf9a5-a7d3-4e64-9571-38218f39413b?include=venue,venue.country
    venue_site = Column(String)


class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    competition_id = Column(Integer, ForeignKey("competitions.id"))
    boat_class_id = Column(Integer, ForeignKey("boat_classes.id"))


class Races(Base): # https://world-rowing-api.soticcloud.net/stats/api/race/b0eae369-8d05-4b8e-9a2e-7de5871715b7?include=racePhase%2CraceBoats.raceBoatAthletes.person%2CraceBoats.invalidMarkResultCode%2CraceBoats.raceBoatIntermediates.distance&sortInclude%5BraceBoats.raceBoatIntermediates.ResultTime%5D=asc
    __tablename__ = "races"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))

    name = Column(String) # e.g. "FA", "H3", "SA/B1", etc...
    phase = Column(String) # e.g. "Heat", "Final" // TODO: normalize?

    # TODO: add RscCode?


class Boats(Base):
    __tablename__ = "boats"

    id = Column(Integer, primary_key=True)
    race_id = Column(Integer, ForeignKey("races.id"))
    result_time = Column(Interval) # TODO: Simply milliseconds as Integer?


class Race_Data(Base):
    __tablename__ = "race_data"

    id = Column(Integer, primary_key=True) # ? needed?
    # TODO: Unique: (boat_id && distance_meter)
    boat_id = Column(Integer, ForeignKey("boats.id"))
    distance_meter = Column(Integer)

    speed_meter_per_sec = Column(Integer)
    stroke = Column(Integer)


# create all tables (init) if they don't exist
Base.metadata.create_all(engine, checkfirst=True)

session = Session()
session.commit()

if __name__ == '__main__':
    print("-"*100, "Init DB")
import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date, Interval

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
    - https://worldrowing.com/event/2018-world-rowing-coastal-championships -> Has Result PDFs but not in JSON API, only in HTML
    - https://worldrowing.com/event/2021-world-rowing-final-paralympic-qualification-regatta -> same
    - Wettkampfklassen / Competition Classes

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


class Venues(Base):
    """
    https://world-rowing-api.soticcloud.net/stats/api/competition/b56cf9a5-a7d3-4e64-9571-38218f39413b?include=venue,venue.country
    """
    __tablename__ = "venues"

    id = Column(Integer, primary_key=True)
    additional_id_ = Column(String)

    country_code = Column(String(length=3))
    city = Column(String)
    site = Column(String)

    is_world_rowing_venue = Column(Boolean)

class Athletes(Base):
    __tablename__ = "athletes"

    id = Column(Integer, primary_key=True)
    additional_id_ = Column(String)

    full_name = Column(String)
    birthdate = Column(Date)
    gender_id = Column(Integer) # TODO: gender table

    # TODO: country?


class Boat_Classes(Base):
    __tablename__ = "boat_classes"

    id = Column(Integer, primary_key=True)
    additional_id_ = Column(String)
    
    abbreviation = Column(String, nullable=False)
    display_name = Column(String, nullable=False)

    gender_id = Column(Integer) # TODO: gender table


class Competition_Category(Base):
    """https://world-rowing-api.soticcloud.net/stats/api/competition/b56cf9a5-a7d3-4e64-9571-38218f39413b/?include=competitionType,competitionType.competitionCategory"""
    __tablename__ = "competition_category"

    id = Column(Integer, primary_key=True)
    additional_id_ = Column(String)

    name = Column(String)


class Competitions(Base):
    """https://world-rowing-api.soticcloud.net/stats/api/competition/718b3256-e778-4003-88e9-832c4aad0cc2?include=venue,competitionType"""
    __tablename__ = "competitions"

    id = Column(Integer, primary_key=True)
    additional_id_ = Column(String)

    competition_class_id = Column(Integer, ForeignKey("competition_category.id"))
    venue_id = Column(Integer, ForeignKey("venues.id"))

    name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    competition_code_ = Column(String)
    is_fisa_ = Column(Boolean)
    

class Events(Base):
    """https://world-rowing-api.soticcloud.net/stats/api/event/05ad5e77-c337-4700-bd9b-a2e0fc7e5fc2?include=boatClass"""
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    additional_id_ = Column(String)


    competition_id = Column(Integer, ForeignKey("competitions.id"))
    boat_class_id = Column(Integer, ForeignKey("boat_classes.id"))

    name = Column(String)

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

if False:
    # create all tables (init) if they don't exist
    Base.metadata.create_all(engine, checkfirst=True)

    session = Session()
    session.commit()

if __name__ == '__main__':
    print("-"*100, "Init DB")
    # from ..scraping_wr import api
    # from backend.scraping_wr import api
    # print(api)

    # Problem with PYTHONPATH vs CWD/PWD: https://stackoverflow.com/a/24435742
    from sys import path as syspath
    print("PYTHONPATH", syspath[0])
    # import backend.scraping_wr.api

    # solution: run as module `python -m backend.model.model`
    from .. scraping_wr import api
    print("api", api)

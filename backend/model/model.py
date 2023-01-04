from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Table, Column, ForeignKey, Integer, Float, String, Boolean, Date

# logging stuff
import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

# In-memory
# engine = create_engine("sqlite:///:memory:", echo=True)

# sqlite file relative path
# engine = create_engine("sqlite:///foo.sqlite", echo=True)

# postgres
# engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/rowing", echo=True)

# Session = sessionmaker(bind=engine)

# connect will actually establish a connection or create/load the sqlite file
# engine.connect()

Base = declarative_base()


"""
TODO:
    - https://worldrowing.com/event/2018-world-rowing-coastal-championships -> Has Result PDFs but not in JSON API, only in HTML
    - https://worldrowing.com/event/2021-world-rowing-final-paralympic-qualification-regatta -> same
    - Wettkampfklassen / Competition Classes

    - !!! CountryCodes are not official
    - ??? communityTypes -> U23, Senior, ...
        -> https://worldrowing.com/event/2022-world-rowing-under-23-championships
        -> https://world-rowing-api.soticcloud.net/stats/api/competition/7ee519e5-288d-4585-bab4-bf916dca49b8?include=venue,venue.country,competitionType.competitionCategory,communityTypes
        -> BEWARE: Multiple communities: https://world-rowing-api.soticcloud.net/stats/api/competition/718b3256-e778-4003-88e9-832c4aad0cc2?include=venue,venue.country,competitionType.competitionCategory,communityTypes

    - world-rowing GUIDs -> As String or Postgres UUID ?
    - race data (high res)
    - Specify Not Null Columns
    - add backref / back_populates for easy access ---> use back_populates for clean code
    - add athlete names
    - add progression string
    - Consider foreign key checking via constraints
    - Define Indexes
    - Ask DRV: Time resolution (milli, micro) !!! -> seems to be millisec -> research what res postgres' INTERVAL has
    - No data source hints are written into db (?)
    - INCLUDE PDFs!!! -> More maximalist apporach

    - Timestamp and timezones:
        https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-timestamp/
        https://codeofmatt.com/please-dont-call-it-epoch-time/#:~:text=Unix%20timestamps%20are%20always%20based,without%20any%20leaps%20ever%20occurring.

    - Query ORM Examples: https://docs.sqlalchemy.org/en/14/orm/queryguide.html#select-statements

https://worldrowing.com/event/2022-world-rowing-cup-iii
https://world-rowing-api.soticcloud.net/stats/api/race/?include=racePhase%2Cevent.competition.competitionType%2Cevent.competition.competitionType.competitionCategory%2Cevent.boatClass&filter%5Bevent.competitionId%5D=b56cf9a5-a7d3-4e64-9571-38218f39413b&sort%5Bdate%5D=asc
"""

# Many-To-Many Association Tables
# -------------------------------

# https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-many

boat_athlete_association_table = Table(
    "boat_athlete_association",
    Base.metadata,
    Column("raceboat_id", ForeignKey("raceboats.id"), primary_key=True),
    Column("athlete_id", ForeignKey("athletes.id"), primary_key=True),
)
# TODO: add boatPosition # Pattern: https://stackoverflow.com/a/62378982


# ORM Classes
# -----------

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    additional_id_ = Column(String)

    country_code = Column(String(length=3))
    name = Column(String)

    # TODO: Clarify meaning and types
    is_former_country__ = Column(String)
    is_noc__ = Column(String)


class Venue(Base):
    """
    https://world-rowing-api.soticcloud.net/stats/api/competition/b56cf9a5-a7d3-4e64-9571-38218f39413b?include=venue,venue.country
    """
    __tablename__ = "venues"

    id = Column(Integer, primary_key=True)
    additional_id_ = Column(String)
    country_id = Column(Integer, ForeignKey("countries.id"))
    country    = relationship("Country")

    city = Column(String)
    site = Column(String)

    is_world_rowing_venue = Column(Boolean)

    # relationships
    competitions = relationship("Competition", back_populates="venue")


class Gender(Base):
    __tablename__ = "genders"

    id = Column(Integer, primary_key=True)
    additional_id_ = Column(String)

    name = Column(String)


class Athlete(Base):
    __tablename__ = "athletes"

    id = Column(Integer, primary_key=True)
    additional_id_ = Column(String)

    name = Column(String)
    first_name__ = Column(String)
    last_name__ = Column(String)
    birthdate = Column(Date)

    height_cm__ = Column(Integer)
    weight_kg__ = Column(Integer)

    country_id = Column(Integer, ForeignKey("countries.id"))
    # TODO: gender? already contained in Event entity
    # OVRCode?

    # relationships
    country = relationship("Country")

class Boat_Class(Base):
    __tablename__ = "boat_classes"

    id = Column(Integer, primary_key=True)
    additional_id_ = Column(String)

    abbreviation = Column(String, nullable=False)
    name = Column(String)

    # relationships
    events = relationship("Event", back_populates="boat_class")


class Competition_Category(Base):
    """https://world-rowing-api.soticcloud.net/stats/api/competition/b56cf9a5-a7d3-4e64-9571-38218f39413b/?include=competitionType,competitionType.competitionCategory"""
    __tablename__ = "competition_category"

    id = Column(Integer, primary_key=True)
    additional_id_ = Column(String)

    name = Column(String)

    # relationships
    competitions = relationship("Competition", back_populates="competition_category")


class Competition(Base):
    """https://world-rowing-api.soticcloud.net/stats/api/competition/718b3256-e778-4003-88e9-832c4aad0cc2?include=venue,competitionType"""
    __tablename__ = "competitions"

    id = Column(Integer, primary_key=True)
    additional_id_ = Column(String)

    competition_category_id = Column(Integer, ForeignKey("competition_category.id"))
    competition_category    = relationship("Competition_Category", back_populates="competitions")
    venue_id = Column(Integer, ForeignKey("venues.id"))
    venue    = relationship("Venue", back_populates="competitions")

    name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    competition_code__ = Column(String)
    is_fisa__ = Column(Boolean)

    # relationships
    events = relationship("Event", back_populates="competition")
    

class Event(Base):
    """https://world-rowing-api.soticcloud.net/stats/api/event/05ad5e77-c337-4700-bd9b-a2e0fc7e5fc2?include=boatClass"""
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    additional_id_ = Column(String)
    name = Column(String)

    competition_id = Column(Integer, ForeignKey("competitions.id"))
    competition    = relationship("Competition", back_populates="events")
    boat_class_id = Column(Integer, ForeignKey("boat_classes.id"))
    boat_class    = relationship("Boat_Class", back_populates="events")
    gender_id = Column(Integer, ForeignKey("genders.id"))
    gender    = relationship("Gender")

    rsc_code__ = Column(String) # RSC-Codes of races contain more information

    # relationships
    races = relationship("Race", back_populates="event")


class Race(Base): # https://world-rowing-api.soticcloud.net/stats/api/race/b0eae369-8d05-4b8e-9a2e-7de5871715b7?include=racePhase%2CraceBoats.raceBoatAthletes.person%2CraceBoats.invalidMarkResultCode%2CraceBoats.raceBoatIntermediates.distance&sortInclude%5BraceBoats.raceBoatIntermediates.ResultTime%5D=asc
    __tablename__ = "races"

    id = Column(Integer, primary_key=True)
    additional_id_ = Column(String)
    event_id = Column(Integer, ForeignKey("events.id"))
    event    = relationship("Event", back_populates="races")

    name = Column(String)
    date = Column(Date)
    phase_type = Column(String) # e.g. "Heat", "Final" // TODO: normalize?
    phase = Column(String) # e.g. "FA", "H3", "SA/B1", etc...

    progression = Column(String) # e.g. "1-2->SA/B, 3..->R"
    rsc_code__ = Column(String)

    pdf_url_results = Column(String)
    pdf_url_race_data = Column(String)

    # Meaning and importance not exactly clear
    race_nr__ = Column(String) # e.g. "103"
    rescheduled__ = Column(Integer) # e.g. 0 # maybe map to bool?
    rescheduled_from__ = Column(String) # low-prio TODO: Type unclear
    race_status__ = Column(String) # e.g. DisplayName "Official" id "182f6f15-8e78-41c3-95b3-8b006af2c6a1"

    # relationships
    race_boats = relationship("Race_Boat", back_populates="race")


class Race_Boat(Base):
    __tablename__ = "raceboats"

    id = Column(Integer, primary_key=True)
    additional_id_ = Column(String)
    race_id = Column(Integer, ForeignKey("races.id"))
    race    = relationship("Race", back_populates="race_boats")
    country_id = Column(Integer, ForeignKey("countries.id"))
    country    = relationship("Country")

    # many-to-many relationship
    athletes = relationship("Athletes", secondary=boat_athlete_association_table)

    name = Column(String) # e.g. "GER2" for one of the German boats

    result_time_ms = Column(Integer) # milliseconds as Integer

    lane = Column(Integer) # e.g. 1
    rank = Column(Integer) # e.g. 2
    final_rank = Column(Integer) # e.g. 8
    final_rank_index__ = Column(String) # TODO: Meaning, Importance, Type?

    # TODO: Meaning, importance and/or type unclear
    remark__ = Column(String)
    world_cup_points__ = Column(Integer)
    club_name__ = Column(String)
    # worldBestTimeId, OVRCode ?

    # relationships
    race_data = relationship("Race_Data", back_populates="raceboat")


class Race_Data(Base):
    __tablename__ = "race_data"

    # TODO: Unique: (boat_id && distance_meter) # https://stackoverflow.com/q/10059345
    # Multi Column Primary Key: https://stackoverflow.com/a/9036128
    raceboat_id = Column(Integer, ForeignKey("raceboats.id"), primary_key=True, autoincrement=False)
    raceboat    = relationship("Race", back_populates="race_boats")
    distance_meter = Column(Integer, primary_key=True, autoincrement=False)

    # Data fields from JSON Web API aka "Intermediates"
    rank = Column(Integer)
    result_time_ms = Column(Integer) # in milliseconds // TODO: as String?
    difference__ = Column(String)
    start_position__ = Column(String)

    # Data fields from race data PDFs
    speed_meter_per_sec = Column(Float)
    stroke = Column(Float)


#----------------------------------------------------------------------

def create_tables():
    engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/rowing", echo=True)

    Session = sessionmaker(bind=engine)

    # create all tables (init) if they don't exist
    Base.metadata.create_all(engine, checkfirst=True)

    session = Session()
    session.commit()


if __name__ == '__main__':
    print("-"*100, "Init DB")
    create_tables()


    # from ..scraping_wr import api
    # from backend.scraping_wr import api
    # print(api)

    # Problem with PYTHONPATH vs CWD/PWD: https://stackoverflow.com/a/24435742
    from sys import path as syspath
    print("PYTHONPATH", syspath[0])
    # import backend.scraping_wr.api

    # solution: run as module `python -m backend.model.model`
    # from .. scraping_wr import api
    # print("api", api)

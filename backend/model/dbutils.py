from . import model

from sqlalchemy import select

from contextlib import suppress
import os
import datetime as dt
import urllib.parse

from ..common.helpers import Timedelta_Parser

# from ..scraping_wr import utils_wr
from ..scraping_wr import api

# logging stuff
import logging
logger = logging.getLogger(__name__)


def get_rowing_db_url() -> str:
    """Returns URL suited for SQLAlchemy as configured in environment variables
    See: https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls
    """
    db_url = "{drivername}://{username}:{password}@{host}:{port}/{database}".format(
        drivername=os.environ.get('DB_SQLALCHEMY_DRIVERNAME', 'postgresql+psycopg2'),
        username=urllib.parse.quote_plus( os.environ.get('DB_USER', 'postgres') ),
        password=urllib.parse.quote_plus( os.environ.get('DB_PASS', 'postgres') ),
        host=os.environ.get('DB_HOST', 'localhost'),
        port=os.environ.get('DB_PORT', '5432'),
        database=os.environ.get('DB_NAME', 'rowing')
    )
    return db_url


def get_(data, key, default=None):
    if data == None:
        return default
    
    if not isinstance(data, dict):
        raise ValueError("data Parameter is not dict type")
    
    return data.get(key, default)


def create_tables(engine):
    # create all tables (init) if they don't exist
    model.Base.metadata.create_all(engine, checkfirst=True)


def drop_all_tables(engine):
    model.Base.metadata.drop_all(engine, checkfirst=True)


def query_by_uuid_(session, Entity_Class, uuid):
    """Helper function.
    If an entity with given uuid exists:
        returns ORM object linked to db
    If not existing:
        returns None
    """
    statement = select(Entity_Class).where(Entity_Class.additional_id_ == uuid.lower())
    result_list = session.execute(statement).first()

    if result_list:
        return result_list[0]
    
    return None


def wr_insert(session, Entity_Class, map_func, data):
    """Proxy function to fetch or create an entity.
    Usage: wr_insert(session, model.Country, wr_map_country, data_dict)"""
    if data == None:
        return None

    uuid = data.get('id','').lower()
    entity = query_by_uuid_(session, Entity_Class, uuid)
    create_entity = entity == None

    if create_entity:
        entity = Entity_Class()
        entity.additional_id_ = uuid

    map_func(session, entity, data)

    if create_entity:
        session.add(entity)

    return entity


def wr_map_country(session, entity, data):
    entity.country_code = get_(data, 'CountryCode')
    entity.name = get_(data, 'DisplayName')

    entity.is_former_country__ = repr(get_(data, 'IsFormerCountry'))
    entity.is_noc__ = repr(get_(data, 'IsNOC'))


def wr_map_boat_class(session, entity, data):
    entity.abbreviation = get_(data, 'DisplayName')
    # TODO: entity.name // full name not in API data


def wr_map_gender(session, entity, data):
    entity.name = get_(data, 'DisplayName')


def wr_map_athlete(session, entity, data):
    entity.name = get_(data, 'DisplayName')
    entity.first_name__ = get_(data, 'FirstName')
    entity.last_name__ = get_(data, 'LastName')
    with suppress(ValueError):
        entity.birthdate = dt.datetime.fromisoformat(get_(data, 'BirthDate', '')).date()

    entity.height_cm__ = get_(data, 'HeightCm')
    entity.weight_kg__ = get_(data, 'WeightKg')

def wr_map_race_boat(session, entity, data):
    entity.country = wr_insert(session, model.Country, wr_map_country, get_(data, 'country'))
    
    # Current Strategy: Delete all associations and create new ones according to given data.
    entity.athletes.clear()
    for raceBoatAthlete in get_(data, 'raceBoatAthletes', []):
        athlete_data = get_(raceBoatAthlete, 'person', {})
        if athlete_data:
            association = model.Association_Race_Boat_Athlete(boat_position=get_(raceBoatAthlete,'boatPosition'))
            association.athlete = wr_insert(session, model.Athlete, wr_map_athlete, athlete_data)
            session.add(association)
            
            entity.athletes.append(association)

    entity.name = get_(data, 'DisplayName') # e.g. "GER2" for the second German boat
    
    result_time_ms = None
    try:
        result_time_ms = Timedelta_Parser.to_millis( get_(data, 'ResultTime') )
    except ValueError:
        pass # TODO: consider logging
    entity.result_time_ms = result_time_ms
    
    entity.lane = get_(data, 'Lane')
    entity.rank = get_(data, 'Rank')
    entity.final_rank = get_( get_(data, 'boat', {}), 'finalRank' )
    entity.final_rank_index__ = repr( get_ (get_(data, 'boat', {}), 'finalRankIndex' ) )
    
    entity.remark__ = repr( get_(data, 'Remark') )
    entity.world_cup_points__ = get_(data, 'WorldCupPoints')
    entity.club_name__ = get_( get_(data, 'boat', {}), 'clubName' )

    # TODO: Race Data

def wr_map_race(session, entity, data):
    entity.name = get_(data, 'DisplayName')
    with suppress(ValueError):
        entity.date = dt.datetime.fromisoformat(get_(data, 'Date', ''))
    entity.phase_type = get_( get_(data, 'racePhase', {}), 'DisplayName','' ).lower()
    entity.phase = get_(data, 'FB') # !!! TODO: Extract from RSC Code !!!
    entity.progression = get_(data, 'Progression')
    entity.rsc_code = get_(data, 'RscCode')

    entity.pdf_url_results = get_(api.select_pdf_(get_(data, 'pdfUrls', []), 'results'), 'url')
    entity.pdf_url_race_data = get_(api.select_pdf_(get_(data, 'pdfUrls', []), 'race data'), 'url')

    entity.race_nr__ = repr( get_(data, 'RaceNr') )
    entity.rescheduled__ = repr( get_(data, 'Rescheduled') )
    entity.rescheduled_from__ = repr( get_(data, 'RescheduledFrom') )
    entity.race_status__ = repr( get_( get_(data, 'raceStatus', {} ), 'DisplayName' ) )

    # Race Boats
    race_boats = map(
        lambda d : wr_insert(session, model.Race_Boat, wr_map_race_boat, d),
        get_(data, 'raceBoats', [])
    )
    entity.race_boats.extend(race_boats)


def wr_map_event(session, entity, data):
    entity.name = get_(data, 'DisplayName')
    entity.boat_class = wr_insert(session, model.Boat_Class, wr_map_boat_class, get_(data, 'boatClass'))
    entity.gender = wr_insert(session, model.Gender, wr_map_gender, get_(data, 'gender'))
    entity.rsc_code__ = get_(data, 'RscCode')

    # Races
    races = map(
        lambda d : wr_insert(session, model.Race, wr_map_race, d),
        get_(data, 'races', [])
    )
    entity.races.extend(races)


def wr_map_competition_category(session, entity, data):
    entity.name = get_(data, 'DisplayName')


def wr_map_venue(session, entity, data):
    entity.country = wr_insert(session, model.Country, wr_map_country, get_(data, 'country'))
    entity.city = get_(data, 'RegionCity')
    entity.site = get_(data, 'Site')
    entity.is_world_rowing_venue = get_(data, 'IsWorldRowingVenue')


def wr_map_competition(session, entity, data):
    # Competition_Category
    competition_category = wr_insert(
        session,
        model.Competition_Category,
        wr_map_competition_category,
        get_(get_(data, 'competitionType'), 'competitionCategory')
    )

    # Venue
    venue = wr_insert(session, model.Venue, wr_map_venue, get_(data, 'venue'))

    entity.competition_category = competition_category
    entity.venue = venue
    entity.name = get_(data, 'DisplayName')
    with suppress(ValueError):
        entity.start_date = dt.datetime.fromisoformat(get_(data, 'StartDate', ''))
        entity.end_date = dt.datetime.fromisoformat(get_(data, 'EndDate', ''))

    entity.competition_code__ = get_(data, 'CompetitionCode')
    entity.is_fisa__ = get_(data, 'IsFisa')

    # Events
    # Insert 1:m https://stackoverflow.com/q/16433338
    events = map(
        lambda d : wr_insert(session, model.Event, wr_map_event, d),
        get_(competition_data, 'events', [])
    )
    entity.events.extend(events)


def wr_insert_competition(session, competition_data):
    # HIGH PRIO TODO: Check for Enum_Maintenance_State and leave untouched it's world_rowing_postprocessed
    wr_insert(session, model.Competition, wr_map_competition, competition_data)
    session.commit()
    pass



if __name__ == '__main__':
    # Command line interface (CLI)
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", help="Create tables if not yet existing", action="store_true")
    parser.add_argument("-d", "--drop", help="Drop all tables described by the schema defined in model.py", action="store_true")
    parser.add_argument("-i", "--insert", help="Import JSON data for a rowing competition")
    args = parser.parse_args()
    print(args)


    from sys import exit as sysexit
    import json

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # Database: session / connection str
    db_url = get_rowing_db_url()
    engine = create_engine(db_url, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    # HIGH PRIO TODO: use scoped_session(...)
    # Use this Flask/SQLAlchemy Pattern: https://stackoverflow.com/questions/66046801/sqlalchemy-used-in-flask-session-management-implementation
    # https://towardsdatascience.com/use-flask-and-sqlalchemy-not-flask-sqlalchemy-5a64fafe22a4
    
    if args.insert:
        print("Load JSON file:", args.insert)
        with open(args.insert, mode="r", encoding="utf-8") as fp:
            competition_data = json.load(fp)
        wr_insert_competition(session, competition_data)

    else:
        if args.drop:
            print("----- Drop All Tables -----")
            drop_all_tables(engine)

        if args.create:
            print("----- Create Tables -----")
            create_tables(engine)
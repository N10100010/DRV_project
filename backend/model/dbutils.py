from . import model

from sqlalchemy import select

import datetime as dt
import re

import urllib.parse

# from ..scraping_wr import utils_wr
# from ..scraping_wr import api

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


class Timedelta_Parser:
    regex = re.compile( r"^(((\d*):)?((\d*):)?(\d*))(\.(\d*))?$" )
    
    def int_(s):
        is_digit_str = isinstance(s, str) and s.isdigit()
        is_int = isinstance(s, int)
        if is_digit_str or is_int:
            return int(s)
        return 0
    
    def to_millis(delta_str):
        """returns int in milliseconds
        
        Input format 'HH:MM:SS.mmm'. Examples: 
        '00:01:53.920', '00:07:59.75', '59.920', '::59.920', '::.', '::1.'
        """
        error = ValueError("Timedelta string does not match the format 'HH:MM:SS.mmm'")

        SECOND_IN_MILLIS = 1000
        MINUTE_IN_MILLIS = 60 * SECOND_IN_MILLIS
        HOUR_IN_MILLIS   = 60 * MINUTE_IN_MILLIS
        
        result = Timedelta_Parser.regex.match(delta_str)
        
        if result == None:
            raise error

        parsed = dict(hours=None, minutes=None, seconds=None, milliseconds=None)
        left_part, parsed['milliseconds'] = result.group(1,8)

        # Now split colon separated left part

        left_part_split = left_part.split(':')
        
        if len(left_part_split) > 3:
            raise error

        for unit, string in zip(('seconds','minutes','hours'), reversed(left_part_split)):
            parsed[unit] = string

        sum_ms  = Timedelta_Parser.int_(parsed['milliseconds'])
        sum_ms += Timedelta_Parser.int_(parsed['seconds']) * SECOND_IN_MILLIS
        sum_ms += Timedelta_Parser.int_(parsed['minutes']) * MINUTE_IN_MILLIS
        sum_ms += Timedelta_Parser.int_(parsed['hours']) * HOUR_IN_MILLIS

        return sum_ms


def create_tables(engine):
    # create all tables (init) if they don't exist
    model.Base.metadata.create_all(engine, checkfirst=True)


def drop_all_tables(engine):
    model.Base.metadata.drop_all(engine)


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

    uuid = data['id'].lower()
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
    pass

def wr_map_race_boat(session, entity, data):
    entity.country = wr_insert(session, model.Country, wr_map_country, data['country'])
    
    # Athletes # TODO: Fix raceBoatAthlete.get('person', {}) => None
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
    entity.final_rank = get_( get_(data, 'boat', {}), 'finalRank' ) #  TODO use chained get_()
    entity.final_rank_index__ = repr( get_ (get_(data, 'boat', {}), 'finalRankIndex' ) ) #  TODO use chained get_()
    
    entity.remark__ = repr( get_(data, 'Remark') )
    entity.world_cup_points__ = get_(data, 'WorldCupPoints')
    entity.club_name__ = get_( get_(data, 'boat', {}), 'clubName' )

    # TODO: Race Data

def wr_map_race(session, entity, data):
    entity.name = get_(data, 'DisplayName')
    entity.date = dt.datetime.fromisoformat(data['Date'])
    entity.phase_type = get_( get_(data, 'racePhase', {}), 'DisplayName','' ).lower() #  TODO use chained get_()
    entity.phase = get_(data, 'FB') # !!! TODO: Extract from RSC Code !!!
    entity.progression = get_(data, 'Progression')
    entity.rsc_code = get_(data, 'RscCode')

    # TODO: PDF URLs from pdf parser output?
    entity.pdf_url_results = "https://dummy.url/race_results.pdf"
    entity.pdf_url_race_data = "https://dummy.url/race_data.pdf"

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
    entity.boat_class = wr_insert(session, model.Boat_Class, wr_map_boat_class, data['boatClass'])
    entity.gender = wr_insert(session, model.Gender, wr_map_gender, data['gender'])
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
    entity.country = wr_insert(session, model.Country, wr_map_country, data['country'])
    entity.city = get_(data, 'RegionCity')
    entity.site = get_(data, 'Site')
    entity.is_world_rowing_venue = get_(data, 'IsWorldRowingVenue')


def wr_map_competition(session, entity, data):
    # Competition_Category
    competition_category = wr_insert(
        session,
        model.Competition_Category,
        wr_map_competition_category,
        data['competitionType']['competitionCategory']
    )

    # Venue
    venue = wr_insert(session, model.Venue, wr_map_venue, data['venue'])

    entity.competition_category = competition_category
    entity.venue = venue
    entity.name = get_(data, 'DisplayName')
    entity.start_date = dt.datetime.fromisoformat(data['StartDate'])
    entity.end_date = dt.datetime.fromisoformat(data['EndDate'])

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

    # Environment variables
    from dotenv import load_dotenv
    load_dotenv()
    import os

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # Database: session / connection str
    db_url = get_rowing_db_url()
    engine = create_engine(db_url, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    if args.insert:
        print("Load JSON file:", args.insert)
        with open(args.insert, mode="r", encoding="utf-8") as fp:
            competition_data = json.load(fp)

        wr_insert_competition(session, competition_data)
        sysexit()

    if args.drop:
        print("----- Drop All Tables -----")
        drop_all_tables(engine)

    if args.create:
        print("----- Create Tables -----")
        create_tables(engine)
import model

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

import datetime as dt

# logging stuff
import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

# session / connection str
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/rowing", echo=True)
Session = sessionmaker(bind=engine)


def create_tables():
    # create all tables (init) if they don't exist
    model.Base.metadata.create_all(engine, checkfirst=True)

    # session = Session()
    # session.commit()


def drop_all_tables():
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
    entity.country_code = data.get('CountryCode')
    entity.name = data.get('DisplayName')

    entity.is_former_country__ = repr(data.get('IsFormerCountry'))
    entity.is_noc__ = repr(data.get('IsNOC'))


def wr_map_boat_class(session, entity, data):
    entity.abbreviation = data.get('DisplayName')
    # TODO: entity.name // full name not in API data


def wr_map_gender(session, entity, data):
    entity.name = data.get('DisplayName')


def wr_map_race_boat(session, entity, data):
    pass


def wr_map_race(session, entity, data):
    entity.name = data.get('DisplayName')
    entity.date = dt.datetime.fromisoformat(data['Date'])
    entity.phase_type = data.get('racePhase', {}).get('DisplayName','').lower()
    entity.phase = data.get('FB') # !!! TODO !!!
    entity.progression = data.get('Progression')
    entity.rsc_code = data.get('RscCode')

    # TODO: PDF URLs from pdf parser output?
    entity.pdf_url_results = "https://dummy.url/race_results.pdf"
    entity.pdf_url_race_data = "https://dummy.url/race_data.pdf"

    entity.race_nr__ = repr( data.get('RaceNr') )
    entity.rescheduled__ = repr( data.get('Rescheduled') )
    entity.rescheduled_from__ = repr( data.get('RescheduledFrom') )
    entity.race_status__ = repr( data.get('raceStatus', {}).get('DisplayName') )

    # Race Boats
    race_boats = map(
        lambda d : wr_insert(session, model.Race_Boat, wr_map_race_boat, d),
        data.get('raceBoats', [])
    )
    entity.race_boats.extend(race_boats)


def wr_map_event(session, entity, data):
    entity.name = data.get('DisplayName')
    entity.boat_class = wr_insert(session, model.Boat_Class, wr_map_boat_class, data['boatClass'])
    entity.gender = wr_insert(session, model.Gender, wr_map_gender, data['gender'])
    entity.rsc_code__ = data.get('RscCode')

    # Races
    races = map(
        lambda d : wr_insert(session, model.Race, wr_map_race, d),
        data.get('races', [])
    )
    entity.races.extend(races)


def wr_map_competition_category(session, entity, data):
    entity.name = data.get('DisplayName')


def wr_map_venue(session, entity, data):
    entity.country = wr_insert(session, model.Country, wr_map_country, data['country'])
    entity.city = data.get('RegionCity')
    entity.site = data.get('Site')
    entity.is_world_rowing_venue = data.get('IsWorldRowingVenue')


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
    entity.name = data.get('DisplayName')
    entity.start_date = dt.datetime.fromisoformat(data['StartDate'])
    entity.end_date = dt.datetime.fromisoformat(data['EndDate'])

    entity.competition_code__ = data.get('CompetitionCode')
    entity.is_fisa__ = data.get('IsFisa')

    # Events
    # Insert 1:m https://stackoverflow.com/q/16433338
    events = map(
        lambda d : wr_insert(session, model.Event, wr_map_event, d),
        competition_data.get('events', [])
    )
    entity.events.extend(events)


def wr_insert_competition(competition_data):
    session = Session()

    wr_insert(session, model.Competition, wr_map_competition, competition_data)

    session.commit()
    pass



if __name__ == '__main__':
    import argparse
    from sys import exit as sysexit
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", help="Create tables if not yet existing", action="store_true")
    parser.add_argument("-d", "--drop", help="Drop all tables described by the schema defined in model.py", action="store_true")
    parser.add_argument("-i", "--insert", help="Import JSON data for a rowing competition")
    args = parser.parse_args()
    print(args)

    if args.insert:
        print("Load JSON file:", args.insert)
        with open(args.insert, mode="r", encoding="utf-8") as fp:
            competition_data = json.load(fp)

        wr_insert_competition(competition_data)
        sysexit()

    if args.drop:
        print("----- Drop All Tables -----")
        drop_all_tables()

    if args.create:
        print("----- Create Tables -----")
        create_tables()
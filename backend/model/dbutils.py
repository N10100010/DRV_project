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


def wr_insert_country(session, data):
    """Creates or queries entity with given data and returns entity object."""
    Entity_Class = model.Country
    uuid = data['id'].lower()
    entity = query_by_uuid_(session, Entity_Class, uuid)
    if not entity:
        entity = Entity_Class()
        entity.additional_id_ = uuid
        entity.country_code = data.get('CountryCode')
        entity.name = data.get('DisplayName')

        entity.is_former_country__ = repr(data.get('IsFormerCountry'))
        entity.is_noc__ = repr(data.get('IsNOC'))

        session.add(entity)
    return entity


def wr_insert_boat_class(session, data):
    """Creates or queries entity with given data and returns entity object."""
    Entity_Class = model.Boat_Class
    uuid = data['id'].lower()
    
    entity = query_by_uuid_(session, Entity_Class, uuid)
    if not entity:
        entity = Entity_Class()
        entity.additional_id_ = uuid
        entity.abbreviation = data.get('DisplayName')
        # TODO: entity.name // full name not in API data

        session.add(entity)
    return entity



def wr_insert_gender(session, data):
    """Creates or queries entity with given data and returns entity object."""
    Entity_Class = model.Gender
    uuid = data['id'].lower()
    
    entity = query_by_uuid_(session, Entity_Class, uuid)
    if not entity:
        entity = Entity_Class()
        entity.additional_id_ = uuid
        entity.name = data.get('DisplayName')

        session.add(entity)
    return entity


def wr_insert_event(session, data):
    """Creates or queries entity with given data and returns entity object."""
    Entity_Class = model.Event
    uuid = data['id'].lower()
    
    entity = query_by_uuid_(session, Entity_Class, uuid)
    if not entity:
        entity = Entity_Class()
        entity.additional_id_ = uuid
        entity.name = data.get('DisplayName')
        entity.boat_class = wr_insert_boat_class(session, data['boatClass'])
        entity.gender = wr_insert_gender(session, data['gender'])
        entity.rsc_code__ = data.get('RscCode')

        session.add(entity)
    return entity


def wr_insert_competition_category(session, data):
    """Creates or queries entity with given data and returns entity object."""
    Entity_Class = model.Competition_Category
    uuid = data['id'].lower()
    
    entity = query_by_uuid_(session, Entity_Class, uuid)
    if not entity:
        entity = Entity_Class()
        entity.additional_id_ = uuid
        entity.name = data.get('DisplayName')

        session.add(entity)
    return entity


def wr_insert_venue(session, data):
    """Creates or queries entity with given data and returns entity object."""
    Entity_Class = model.Venue
    uuid = data['id'].lower()
    
    entity = query_by_uuid_(session, Entity_Class, uuid)
    if not entity:
        entity = Entity_Class()
        entity.additional_id_ = uuid
        entity.country = wr_insert_country(session, data['country'])
        entity.city = data.get('RegionCity')
        entity.site = data.get('Site')
        entity.is_world_rowing_venue = data.get('IsWorldRowingVenue')

        session.add(entity)
    return entity


def wr_insert_competition(competition_data):
    session = Session()

    # Competition
    uuid = competition_data['id'].lower()
    competition = query_by_uuid_(session, model.Competition, uuid)
    if not competition:
        competition = model.Competition()

    # Competition_Category
    competition_category = wr_insert_competition_category(
        session,
        competition_data['competitionType']['competitionCategory']
    )

    # Venue
    venue = wr_insert_venue(session, competition_data['venue'])

    competition.additional_id_ = uuid
    competition.competition_category = competition_category
    competition.venue = venue
    competition.name = competition_data.get('DisplayName')
    competition.start_date = dt.datetime.fromisoformat(competition_data['StartDate'])
    competition.end_date = dt.datetime.fromisoformat(competition_data['EndDate'])

    competition.competition_code__ = competition_data.get('CompetitionCode')
    competition.is_fisa__ = competition_data.get('IsFisa')

    # Events
    # Insert 1:m https://stackoverflow.com/q/16433338
    events = list(map(lambda i : wr_insert_event(session, i), competition_data['events']))
    competition.events.extend(events)

    session.add(competition)
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
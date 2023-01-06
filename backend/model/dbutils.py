import model

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

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


def query_by_uuid_(session, entity_class, uuid):
    """Helper function.
    If an entity with given uuid exists:
        returns ORM object linked to db
    If not existing:
        returns None
    """
    statement = select(entity_class).where(entity_class.additional_id_ == uuid.lower())
    result_list = session.execute(statement).first()

    if result_list:
        return result_list[0]
    
    return None


def wr_insert_country(session, data):
    """Creates or queries entity with given data and returns entity object."""
    entity_class = model.Country
    uuid = data['id']
    entity = query_by_uuid_(session, entity_class, uuid)
    if not entity:
        entity = entity_class()
        entity.additional_id_ = uuid
        entity.country_code = data.get('CountryCode')
        entity.name = data.get('DisplayName')

        entity.is_former_country__ = repr(data.get('IsFormerCountry'))
        entity.is_noc__ = repr(data.get('IsNOC'))

    return entity

def wr_insert_competition(competition_data):
    session = Session()

    # Competition_Category
    comp_cat = competition_data['competitionType']['competitionCategory']
    uuid = comp_cat['id'].lower()

    competition_category = query_by_uuid_(session, model.Competition_Category, uuid)
    if not competition_category:
        competition_category = model.Competition_Category()
        competition_category.additional_id_ = uuid
        competition_category.name = comp_cat.get('DisplayName')

    # Country (Venue)
    venue_country = wr_insert_country(session, competition_data['venue']['country'])

    # Venue
    venue_data = competition_data['venue']
    uuid = venue_data['id'].lower()

    venue = query_by_uuid_(session, model.Venue, uuid)
    if not venue:
        venue = model.Venue()
        venue.additional_id_ = uuid
        venue.country = venue_country
        venue.city = venue_data.get('RegionCity')
        venue.site = venue_data.get('Site')
        venue.is_world_rowing_venue = venue_data.get('IsWorldRowingVenue')


    # Competition
    uuid = competition_data['id'].lower()
    competition = query_by_uuid_(session, model.Competition, uuid)
    if not competition:
        competition = model.Competition()
    competition.additional_id_ = uuid
    competition.name = competition_data.get('DisplayName')
    competition.competition_category = competition_category
    competition.venue = venue



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
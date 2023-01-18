from . import model

from sqlalchemy import select

from contextlib import suppress
import datetime as dt

from ..common.helpers import Timedelta_Parser, parse_wr_intermediate_distance_key

# from ..scraping_wr import utils_wr
from ..scraping_wr import api

# logging stuff
import logging
logger = logging.getLogger(__name__)


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
    # 1.4 / 2.0 https://docs.sqlalchemy.org/en/14/orm/queryguide.html
    # 2.0 https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#selecting-orm-entities
    statement = select(Entity_Class).where(Entity_Class.additional_id_ == uuid.lower())
    result_entity = session.scalars(statement).first()
    return result_entity


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
    with suppress(TypeError, ValueError):
        entity.birthdate = dt.datetime.fromisoformat(get_(data, 'BirthDate', '')).date()

    entity.height_cm__ = get_(data, 'HeightCm')
    entity.weight_kg__ = get_(data, 'WeightKg')


def wr_insert_invalid_mark_result_code(session, data):
    """data example: {"code": "Did not start", "displayName": "DNS", "id": "4b554cb1-8468-4fa7-b75b-434ff1732d81"}"""
    Entity_Class = model.Invalid_Mark_Result_Code
    
    if data == None:
        return None

    # TODO: Force uppercase: Use validator or getter/setter
    #    - https://gist.github.com/luhn/4170996
    #    - https://stackoverflow.com/a/34322323
    #    - https://docs.sqlalchemy.org/en/14/orm/mapped_attributes.html

    abbreviation = get_(data, 'displayName', '').upper()
    if not abbreviation:
        return None

    entity = session.get(Entity_Class, {'id': abbreviation})
    create_entity = entity == None

    if create_entity:
        entity = Entity_Class()
        entity.id = abbreviation
        entity.name = get_(data, 'code')
        session.add(entity)
    
    return entity


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
    
    with suppress(TypeError, ValueError):
        entity.result_time_ms = Timedelta_Parser.to_millis( get_(data, 'ResultTime') )
    
    entity.invalid_mark_result_code = wr_insert_invalid_mark_result_code(session, get_(data, 'invalidMarkResultCode'))

    entity.lane = get_(data, 'Lane')
    entity.rank = get_(data, 'Rank')
    
    entity.remark__ = repr( get_(data, 'Remark') )
    entity.world_cup_points__ = get_(data, 'WorldCupPoints')
    entity.club_name__ = get_( get_(data, 'boat', {}), 'clubName' )

    # Intermediate times
    # (Beware: Contains duplicates for same distance raceID:931fd903-1d44-4ace-8665-bf1230dc0227 -> boat:2d5a3f94-37ba-480d-9d72-eada6a4c30f9 (DEN))
    entity.intermediates.clear()
    seen_set = set()
    for interm_data in get_(data, 'raceBoatIntermediates', []):
        intermediate = model.Intermediate_Time()

        # filter out duplicates // Future TODO/NOTE: Check if current strategy is appropriate
        distance_key = get_(get_(interm_data, 'distance'), 'DisplayName', '')
        if distance_key in seen_set:
            pass
            continue

        with suppress(TypeError, ValueError):
            intermediate.distance_meter = parse_wr_intermediate_distance_key(distance_key)
            intermediate.data_source_ = model.Enum_Data_Source.world_rowing_api.value
            intermediate.rank = get_(interm_data, 'Rank')
            intermediate.result_time_ms = Timedelta_Parser.to_millis( get_(interm_data, 'ResultTime') )

            intermediate.difference__ = repr( get_(interm_data, 'Difference') )
            intermediate.start_position__ = repr( get_(interm_data, 'StartPosition') )

            session.add(intermediate)
            entity.intermediates.append(intermediate)

            seen_set.add(distance_key)


def wr_map_race(session, entity, data):
    entity.name = get_(data, 'DisplayName')
    with suppress(TypeError, ValueError):
        entity.date = dt.datetime.fromisoformat(get_(data, 'Date', ''))
    entity.phase_type = get_( get_(data, 'racePhase', {}), 'DisplayName','' ).lower()
    entity.phase = get_(data, 'FB') # !!! HIGH PRIO TODO: Extract from RSC Code !!!
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
    # Check maintenance state
    STATE_DEFAULT = model.Enum_Maintenance_Level.world_rowing_api_grabbed.value
    STATE_UPPER_LIMIT = model.Enum_Maintenance_Level.world_rowing_api_grabbed.value

    state = entity.maintenance_level
    update_entity = state == None or state <= STATE_UPPER_LIMIT
    if not update_entity:
        return entity

    if entity.maintenance_level == None:
        entity.maintenance_level = STATE_DEFAULT

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
    with suppress(TypeError, ValueError):
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

    # ----------------------------------

    import json
    from .model import engine, Scoped_Session

    if args.insert:
        print("Load JSON file:", args.insert)
        with Scoped_Session() as session: # implicit commit when leaving context w/o errors
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
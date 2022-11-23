from backend.scraping.world_rowing import utils as ut
import pandas as pd

# CONSTANTS
WR_BASE_URL = "https://world-rowing-api.soticcloud.net/stats/api/"
# ENDPOINTS FOR THE BASE-URL
WR_ENDPOINT_RACE = "race/"
WR_ENDPOINT_EVENT = "event/"
WR_ENDPOINT_COMPETITION = "competition/"
WR_ENDPOINT_COMPETITION = "competitionCategory/"
WR_ENDPOINT_COMPETITIONTYPE = "competitionType/"
WR_ENDPOINT_STATS = "statistic/"
WR_ENDPOINT_VENUE = "venue/"
WR_ENDPOINT_BOATCLASSES = "boatClass/"
WR_ENDPOINT_COUNTIRES = "country/"

# add function descriptions

PIPE_PRE_PROCESS = ut.Pipeline(
    functions=[ut.alter_dataframe_column_types, ut.extract_rsc_codes],
    default_kwargs=None
)


def _pre_process_to_dataframe(_dict: dict) -> pd.DataFrame:
    """
    Identifies date- and binary-columns and transforms their types.

    FYI: since python >= 3.9, one can merge dict's the following way:
        d1 = {1:1, 2:2}
        d2 = {2:2, 3:3}
        d1 | d2 == {1: 1, 2: 2, 3: 3}
    """
    df = ut.preprocess_json_to_dataframe(_dict)

    date_cols = ut.get_date_columns(df.columns.to_list())
    binary_cols = ut.get_binary_columns(df)

    date_cols = {k: "date" for k in date_cols}
    binary_cols = {k: "bool" for k in binary_cols}
    datatypes = {'type_mapping': date_cols | binary_cols}

    return PIPE_PRE_PROCESS(df, kwargs_list=[datatypes, None])


def get_competitiontype(kwargs: dict = {}) -> pd.DataFrame:
    _json_dict = ut.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_COMPETITIONTYPE}', **kwargs)
    df = _pre_process_to_dataframe(_json_dict)

    return df


def get_countries(kwargs: dict = {}) -> pd.DataFrame:
    _json_dict = ut.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_COUNTIRES}', **kwargs)
    df = _pre_process_to_dataframe(_json_dict)

    return df


def get_boatclasses(kwargs: dict = {}) -> pd.DataFrame:
    _json_dict = ut.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_BOATCLASSES}', **kwargs)
    df = _pre_process_to_dataframe(_json_dict)

    return df


def get_statistics(kwargs: dict = {}) -> pd.DataFrame:
    _json_dict = ut.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_STATS}', **kwargs)
    df = _pre_process_to_dataframe(_json_dict)

    return df


def get_venues(kwargs: dict = {}) -> pd.DataFrame:
    _json_dict = ut.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_VENUE}', **kwargs)
    df = _pre_process_to_dataframe(_json_dict)

    return df


def get_competitions(year: int = None, kind: str = None, kwargs: dict = {}) -> pd.DataFrame:
    _extend_by = kwargs.get('extend_by', None)
    if _extend_by:
        del kwargs['extend_by']

    _json_dict = ut.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_COMPETITION}', **kwargs)
    df = _pre_process_to_dataframe(_json_dict)

    if _extend_by:
        _extend_by_venue = _extend_by.get('venue', None)
        _extend_by_country = _extend_by.get('country', None)

        if _extend_by_venue and _extend_by_country:
            df = ut.merge(
                (df, get_venues(), get_countries()),
                how='left',
                left_on=('venueid', 'countryid'),
                right_on=('id', 'id'),
                suffixes=(
                    (None, '_venue'),
                    (None, '_county')
                )
            )
        elif _extend_by_venue:
            df = ut.merge(
                (df, get_venues()),
                how='left',
                left_on=('venueid'),
                right_on=('id'),
                suffixes=(
                    (None, '_venue')
                )
            )

    if year:
        # if the date column is known, one can filter for it
        # df = df[df['date'].year == year]
        return df
    else:
        return df


def get_races(year: int = None, kind: str = None, kwargs: dict = {}) -> pd.DataFrame:
    _json_dict = ut.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_RACE}', **kwargs)
    df = _pre_process_to_dataframe(_json_dict)

    if year:
        # if the date column is known, one can filter for it
        # df = df[df['date'].year == year]
        return df
    else:
        return df


def get_events(year: int = None, kind: str = None, kwargs: dict = {}) -> pd.DataFrame:
    _json_dict = ut.load_json(url=f'{WR_BASE_URL}{WR_ENDPOINT_EVENT}', **kwargs)
    df = _pre_process_to_dataframe(_json_dict)

    if year:
        # if the date column is known, one can filter for it
        # df = df[df['date'].year == year]
        return df
    else:
        return df


def merge_race_event_competitions(races: pd.DataFrame, events: pd.DataFrame, competitions: pd.DataFrame) -> pd.DataFrame:
    return ut.merge(
        (
            races.reset_index(), events,
            competitions, get_boatclasses()
        ),
        how='left',
        left_on=('eventid', 'competitionid', 'boatclassid'),
        right_on='id',
        suffixes=(
            (None, '_event'),
            (None, '_competition'),
            (None, '_boat_class')
        )
    ).set_index('id')

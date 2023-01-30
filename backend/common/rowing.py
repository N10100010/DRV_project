from datetime import date

import logging
logger = logging.getLogger(__name__)

from .helpers import make_keys_lowercase

__course_length_2000m_lookup_table = make_keys_lowercase({
    "LW1x": date(1998,1,1),
    "PR3 W2-": date(2007,1,1)
    # ... TODO: Kay ...
})

def get_course_length(boat_class: str, race_date: date, **kwargs) -> int:
    """
    Returns course length

    Parameters
    ----------
    boat_class: Short form of the boat class e.g. "LW1x", "PR3 W2-", etc.
    date: Date of the race
    """
    DEFAULT_LENGTH = None

    threshold_date = __course_length_2000m_lookup_table.get(boat_class.strip())
    
    if not threshold_date:
        # TODO: uncomment logging when lookup table is complete
        # logger.error(f"Boat class '{boat_class}' not found in course length lookup table (2km)")
        return DEFAULT_LENGTH

    if race_date > threshold_date:
        return 2000
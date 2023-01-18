import re


def get_(data, key, default=None):
    if data == None:
        return default
    
    if not isinstance(data, dict):
        raise ValueError("data Parameter is not dict type")
    
    return data.get(key, default)


def int_(s):
    is_digit_str = isinstance(s, str) and s.isdigit()
    is_int = isinstance(s, int)
    if is_digit_str or is_int:
        return int(s)
    return 0


class Timedelta_Parser:
    regex = re.compile( r"^(((\d*):)?((\d*):)?(\d*))(\.(\d*))?$" )
    
    def to_millis(delta_str: str) -> int:
        """returns int in milliseconds
        
        Input format 'HH:MM:SS.mmm'. Examples: 
        '00:01:53.920', '00:07:59.75', '59.920', '::59.920', '::.', '::1.'
        """
        error = ValueError("Timedelta string does not match the format 'HH:MM:SS.mmm'")

        if not isinstance(delta_str, str):
            raise TypeError("Not a string")

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

        sum_ms  = int_(parsed['milliseconds'])
        sum_ms += int_(parsed['seconds']) * SECOND_IN_MILLIS
        sum_ms += int_(parsed['minutes']) * MINUTE_IN_MILLIS
        sum_ms += int_(parsed['hours']) * HOUR_IN_MILLIS

        return sum_ms


__wr_distance_regex = re.compile( r"^d(\d+)m$" )
def parse_wr_intermediate_distance_key(distancy_key: str) -> int:
    """Input: "d2000m" -> Output: int(2000)"""

    if not isinstance(distancy_key, str):
        raise TypeError("Not a string")

    result = __wr_distance_regex.match(distancy_key)
    if result == None:
        raise ValueError("distancy_key does not look like e.g. 'd1234m'")

    meters = result.group(1)
    return int(meters)

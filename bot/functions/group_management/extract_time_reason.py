import re
from time import time

async def _extract_time_reason(string):
    time_regex = re.compile(r'(\d+)([smhd])')
    find_time = time_regex.findall(string)
    
    multipliers = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    time_duration = None
    logical_time = None

    if find_time:
        for value, unit in find_time:
            value = int(value)
            unit = unit.lower()
            time_duration = time() + value * multipliers.get(unit)
            if (value < 35 and unit == "s") or (value > 365 and unit == "d"):
                logical_time = "forever"
                time_duration = None
            else:
                logical_time = f"{value}{unit}"
    
    reason = re.sub(time_regex, '', string).strip()
    return time_duration, logical_time, reason

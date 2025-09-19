import subprocess
from datetime import datetime as dt

# THIS METHOD IS UNFINISHED!!
def seconds_to_YMD(seconds: float):
    age = dt.fromtimestamp(seconds)
    return_str = ""

    if age.year > 1:
        return_str += f"{age.year} years"
    elif age.year == 1:
        return_str += f"{age.year} year"
    
    # if age.month > 1:
    #     return_str += f" {}"
    return f"{age.year} years, {age.month} months, and {age.day} days."
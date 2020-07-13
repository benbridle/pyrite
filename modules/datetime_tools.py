from datetime import datetime, timedelta
import pytz

def get_start_of_week(date):
    dt = date - timedelta(days=date.weekday())
    dt = datetime.combine(dt.date(), datetime.min.time())
    return localize_datetime(dt)

def get_end_of_week(date):
    return get_start_of_week(date) + one_week_delta - timedelta(seconds=1)

def is_within_period(date, start_date, end_date):
    return start_date <= date <= end_date

def now():
    return datetime.now(tz=nz_tz)

def localize_datetime(dt):
    return nz_tz.localize(dt)

def get_human_readable_string(dt):
    date_with_suffix = get_date_with_suffix(dt)
    formatted_date = dt.strftime(date_with_suffix+" %B %Y")
    return formatted_date

def get_date_with_suffix(dt):
    date = dt.strftime("%e").strip()
    day_suffix = "th"
    if date[-1] == "1" and date != "11":
        day_suffix = "st"
    if date[-1] == "2" and date != "12":
        day_suffix = "nd"
    if date[-1] == "3" and date != "13":
        day_suffix = "rd"
    return date+day_suffix

one_week_delta = timedelta(days=7)
one_year_delta = timedelta(days=365)
nz_tz = pytz.timezone("Pacific/Auckland")
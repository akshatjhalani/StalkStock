import datetime
import calendar
import pytz

sgtz = pytz.timezone('Asia/Singapore')


def get_current_hour_datetime():
    current_time = datetime.datetime.now(sgtz)
    current_hour_time = current_time.strftime('%Y-%m-%dT%H:00:00%z')
    current_hour_time = f"{current_hour_time[:-2]}:{current_hour_time[-2:]}"

    return datetime.datetime.fromisoformat(current_hour_time)


def to_next_month(date):
    year = date.year
    month = date.month
    days_in_month = calendar.monthrange(year, month)[1]
    next_month = date + datetime.timedelta(days=days_in_month)
    return next_month




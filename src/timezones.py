import pytz


priorities = ('US/Pacific', 'US/Mountain', 'US/Central', 'US/Eastern',
              'Brazil/East', 'UTC')

all_tz = pytz.all_timezones_set.copy()
for priority in priorities:
    all_tz.remove(priority)

all_tz = sorted(list(all_tz))
all_tz[:0] = priorities  # prepend list to list

all_tz = tuple((tz, tz) for tz in all_tz)  # tuples for selection widget


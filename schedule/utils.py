# Matches => Round robin
# Days Available
# Days for matches
from datetime import datetime, timedelta

import random

from schedule.models import Division, Ground, Schedule


def calculate_weekends(start_date, end_date, exception_dates):
    start_date = datetime.strptime(start_date, '%m/%d/%Y')
    end_date = datetime.strptime(end_date, '%m/%d/%Y')
    exception_dates = [datetime.strptime(date, '%m/%d/%Y') for date in exception_dates]
    available_days = {}
    while start_date <= end_date:
        if start_date not in exception_dates:
            if start_date.weekday() in [5, 6]:
                if 'weekends' in available_days.keys():
                    available_days['weekends'].append(start_date)
                else:
                    available_days['weekends'] = [start_date]
            else:
                if 'weekdays' in available_days.keys():
                    available_days['weekdays'].append(start_date)
                    available_days['weekdays'].append(start_date)
                else:
                    available_days['weekdays'] = [start_date]
        start_date += timedelta(days=1)

    return available_days


def schedule_matches(start_date, end_date, exception_dates):
    available_days = calculate_weekends(start_date, end_date, exception_dates)
    print(available_days)

    divisions = Division.objects.all()
    matches = {}

    divisions_teams = [list(div.team_set.all()) for div in divisions]

    per_division_matches = {}
    total_matches = 0
    for div in divisions:
        for rounds in create_schedule(list(div.team_set.all())):
            for match in rounds:
                if 'BYE' != match[0] and 'BYE' != match[1]:

                    if div.name in per_division_matches.keys():
                        per_division_matches[div.name].append(match)
                    else:
                        per_division_matches[div.name] = [match]

        per_division_matches[div.name].extend(per_division_matches[div.name])
        total_matches += len(per_division_matches[div.name])

    print(per_division_matches)
    print(total_matches)


    all_div_keys = [key for key in per_division_matches.keys()]
    all_matches_tuples = list(zip(per_division_matches[all_div_keys[0]], per_division_matches[all_div_keys[1]]))
    available_grounds = Ground.objects.all()
    number_matches_on_weekdays = total_matches - ((2 * available_grounds.count()) * len(available_days.get('weekends')))

    weekdays_match_dates = random.sample(available_days.get('weekdays'),
                                         number_matches_on_weekdays) if number_matches_on_weekdays > 0 else []

    create_schedule_on_dates(available_days.get('weekends'), weekdays_match_dates, all_matches_tuples,
                             available_grounds)


def create_schedule_on_dates(week_ends, week_days, matches, grounds):
    all_available_dates = []
    all_available_dates.extend(week_days)
    all_available_dates.extend(week_ends)
    all_available_dates.sort()
    start_matches = list(matches.pop())
    sched = {}

    for day in all_available_dates:
        for ground in grounds:
            try:

                if day.weekday() in [5, 6]:
                    if start_matches:
                        append_or_create_a_list(sched, day, start_matches, ground)
                        if start_matches:
                            append_or_create_a_list(sched, day, start_matches, ground)
                        else:
                            start_matches = list(matches.pop())
                            append_or_create_a_list(sched, day, start_matches, ground)
                    else:
                        start_matches = list(matches.pop())
                        append_or_create_a_list(sched, day, start_matches, ground)
                        append_or_create_a_list(sched, day, start_matches, ground)
                else:

                    if start_matches:
                        append_or_create_a_list(sched, day, start_matches, ground)
                    else:
                        start_matches = list(matches.pop())
                        append_or_create_a_list(sched, day, start_matches, ground)
            except Exception as e:
                print(e)
                pass

    print(sched)
    final_schedule(sched)


def final_schedule(sched):
    Schedule.objects.all().delete()
    for key in sched.keys():
        grounds = []
        for match_schedule in sched[key]:
            if key.weekday() in [5, 6]:
                if match_schedule[1] in grounds:  # Second match
                    grounds.append(match_schedule[1])
                    temp = key
                    temp = temp.replace(hour=14, minute=30)
                    Schedule.objects.create(team1=match_schedule[0][0], team2=match_schedule[0][1],
                                            ground=match_schedule[1], schedule_time=temp)
                    print('Team1 : %s - Team2: %s , Ground: %s , start_time: %s' % (
                        str(match_schedule[0][0]), str(match_schedule[0][1]), str(match_schedule[1]), str(temp)))
                else:  # first match
                    grounds.append(match_schedule[1])
                    temp = key
                    temp = temp.replace(hour=9, minute=30)
                    Schedule.objects.create(team1=match_schedule[0][0], team2=match_schedule[0][1],
                                            ground=match_schedule[1], schedule_time=temp)
                    print('Team1 : %s - Team2: %s , Ground: %s , start_time: %s' % (
                        str(match_schedule[0][0]), str(match_schedule[0][1]), str(match_schedule[1]), str(temp)))
            else:
                grounds.append(match_schedule[1])
                temp = key
                temp = temp.replace(hour=16, minute=30)
                Schedule.objects.create(team1=match_schedule[0][0], team2=match_schedule[0][1],
                                        ground=match_schedule[1], schedule_time=temp)
                print('Team1 : %s - Team2: %s , Ground: %s , start_time: %s' % (
                    str(match_schedule[0][0]), str(match_schedule[0][1]), str(match_schedule[1]), str(temp)))


def append_or_create_a_list(sched, day, start_matches, ground):
    if day in sched.keys():
        if day.weekday() in [5, 6] and len(sched[day]) < 4:
            sched[day].append((start_matches.pop(), ground))
        elif day.weekday() not in [5, 6] and len(sched[day]) < 2:
            sched[day].append((start_matches.pop(), ground))
    else:
        sched[day] = [(start_matches.pop(), ground)]


def create_schedule(team_list):
    """ Create a schedule for the teams in the list and return it"""
    schedule = []
    if len(team_list) % 2 == 1: team_list = team_list + ["BYE"]
    for i in range(len(team_list) - 1):
        mid = int(len(team_list) / 2)
        l1 = team_list[:mid]
        l2 = team_list[mid:]
        l2.reverse()

        if (i % 2 == 1):
            schedule = schedule + [zip(l1, l2)]
        else:
            schedule = schedule + [zip(l2, l1)]

        team_list.insert(1, team_list.pop())
    return schedule

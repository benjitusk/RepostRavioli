#!/usr/bin/python3
from psaw import PushshiftAPI
import datetime
from math import floor
import json
import calendar
import time

# Instructions:
#
# Collect the most recent 2 hours of submissions
# Scan against the last 3 months of copypasta
# Add to file in day.month.year.{submissions|comments}.json format
#


def main():

    api = PushshiftAPI()
    sub = 'copypasta'
    total_entries = 0
    total_time = time.time()
    now = datetime.datetime.now()
    monthcount = abs(int(input('Number of months to archive: ')))
    print('Preparing to archive the following months:')
    now = datetime.datetime.now()
    month = now.month
    year = now.year
    for n in range(monthcount):
        n += 2
        if month - n <= 0:
            month += 12
            year -= 1
        n_months_ago = month - n
        print(f'{n_months_ago}/{year}')
    for months_ago in range(monthcount):

        months_ago += 2

        end_month = now.month - (months_ago - 1)
        end_year = now.year

        if end_month <= 0:
            end_month += 12
            end_year -= 1

        start_month = now.month - (months_ago)
        start_year = now.year

        if start_month <= 0:
            start_month += 12
            start_year -= 1

        start_timestamp = int(datetime.datetime(
            start_year, start_month, 1).timestamp())
        end_timestamp = int(datetime.datetime(
            end_year, end_month, 1).timestamp())

        month = name_of_month(start_month).lower()
        month_entries = 0
        # month_start = time.time()

        print(f'Starting archival for {month} {start_year}...')
        print(
            f'Starting submissions fetch for {month} {start_year} [{start_timestamp} - {end_timestamp}] at {time.ctime()}...')
        start_timer = time.time()
        new_fetch = list(api.search_submissions(
            after=start_timestamp, before=end_timestamp, subreddit=sub))
        print(
            f'Finished submissions fetch for {month} {start_year} after {get_time_from_seconds(time.time()-start_timer)}. This month contains {len(new_fetch)} submissions.')
        total_entries += len(new_fetch)
        month_entries += len(new_fetch)
        print('Writing new submissions to disk')
        start_timer = time.time()
        with open(f'{month}.{start_year}.submissions.json', 'w') as output:
            json.dump(new_fetch, output)
        print(
            f'Done. Writing submissions to disk completed after: {get_time_from_seconds(time.time()-start_timer)}')
        new_fetch = None
        print(
            f'Starting comments fetch for {month} {start_year} [{start_timestamp} - {end_timestamp}] at {time.ctime()}...')
        start_timer = time.time()
        new_fetch = list(api.search_comments(
            after=start_timestamp, before=end_timestamp, subreddit=sub))
        print(
            f'Finished comments fetch for {month} {start_year} after {get_time_from_seconds(time.time()-start_timer)}. This month contains {len(new_fetch)} comments.')
        total_entries += len(new_fetch)
        month_entries += len(new_fetch)
        print('Writing new comments to disk')
        start_timer = time.time()
        with open(f'{month}.{start_year}.comments.json', 'w') as output:
            json.dump(new_fetch, output)
        print(
            f'Done. Writing comments to disk completed after: {get_time_from_seconds(time.time()-start_timer)}')
        new_fetch = None
        print(
            f'Finished archiving {month_entries} entries for {month} {start_year}.')
        print(f'{total_entries} total entries written to disk')
    total_time = time.time() - total_time
    total_time_seconds = total_time % 60
    total_time_minutes = floor((total_time / 60) - total_time_seconds) % 60
    total_time_hours = floor((total_time / 60) - total_time_seconds)
    print(
        f'Done! Elapsed time: {total_time_hours}h, {total_time_minutes}m, {total_time_seconds}s')


def get_time_from_seconds(sec):
    return str(datetime.timedelta(seconds=(time.time() - sec)))


def name_of_month(month_number):
    return calendar.month_name[month_number]


if __name__ == "__main__":
    main()

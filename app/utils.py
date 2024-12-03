from datetime import datetime, timedelta

import requests
from dateutil import parser, tz


def is_item_within_year(data, item_type):
    if item_type == 'commits':
        return is_within_year(data["commit"]["author"]["date"])

    if item_type == 'issues' or item_type == 'requests':
        return is_within_year(data["created_at"])

    if item_type == 'reviews':
        return is_within_year(data["closed_at"])


def is_within_year(date):
    check_date = parser.isoparse(date)
    current_date = datetime.now(tz=tz.UTC)

    difference = current_date - check_date

    return difference <= timedelta(days=365)


def get_linguist_colours():
    response = requests.get("https://raw.githubusercontent.com/ozh/github-colors/master/colors.json")

    return response.json()

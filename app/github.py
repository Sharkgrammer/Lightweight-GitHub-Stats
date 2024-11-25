import requests

from utils import is_item_within_year
import settings as s

key = ""

base_url = "https://api.github.com/"
base_username = ""

headers = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

data = {}


def get_data():
    return data


def get_item_amt(item_type, params, url):
    page = 1
    total = 0

    while True:
        items = get_item(page, params, url)

        item_len = len(items)

        if item_len == 0:
            break

        if is_item_within_year(items[item_len - 1], item_type):
            total += item_len

        else:
            # check the first, for a hopefully faster exit
            if not is_item_within_year(items[0], item_type):
                break

            # RIP. Rather than loop through 100 items, do a search
            point = int(item_len / 2)
            jump = int(point / 2)
            counter = 0

            while True:
                old_point = point

                if is_item_within_year(items[point], item_type):

                    if jump == 1 and abs(point - old_point) < 2:
                        if counter > 3:
                            break

                        counter += 1

                    point += jump

                else:
                    point -= jump

                jump = max(int(jump / 2), 1)

            total += point + 1
            break

        if item_len < 100:
            break

        else:
            page += 1

    data[item_type] = total


def get_item(page, params, url):
    global base_username

    params["page"] = page

    response = requests.get(get_url(url), params=params, headers=headers)

    return response.json()["items"]


def get_commits():
    item_type = "commits"

    params = {
        "q": "author:" + base_username,
        "per_page": "100",
        "sort": "author-date",
        "order": "desc",
    }

    get_public(item_type)
    get_item_amt(item_type, params, "search/commits")


def get_issues():
    item_type = "issues"

    params = {
        "q": "author:" + base_username + " type:issue",
        "per_page": "100",
        "sort": "author-date",
        "order": "desc",
    }

    get_public(item_type)
    get_item_amt(item_type, params, "search/issues")


def get_requests():
    item_type = "requests"

    params = {
        "q": "author:" + base_username + " type:pr",
        "per_page": "100",
        "sort": "author-date",
        "order": "desc",
    }

    get_public(item_type)
    get_item_amt(item_type, params, "search/issues")


def get_reviews():
    item_type = "reviews"

    params = {
        "q": "reviewed-by:" + base_username + " type:pr review:approved",
        "per_page": "100",
        "sort": "author-date",
        "order": "desc",
    }

    get_public(item_type)
    get_item_amt(item_type, params, "search/issues")


def get_url(end):
    return base_url + end


def get_user():
    global base_username

    get_public("user")

    url = get_url("user" if not s.PUBLIC else "users/" + s.PUBLIC_USER)

    response = requests.get(url, headers=headers)
    json = response.json()

    user = json["login"]
    name = json["name"]

    data["username"] = user
    data["name"] = name

    base_username = user


def get_repo_data():
    url = get_url("user/repos" if not s.PUBLIC and s.ALLOW_PRIVATE_REPOS else "users/" + base_username + "/repos")

    repo_amt = 0
    stars = 0
    page = 1
    languages = {}

    get_public("repos")

    while True:
        repos = get_repos(url, page)
        amt = len(repos)

        repo_amt += amt

        for repo in repos:
            stars += int(repo["stargazers_count"])

            lan = repo["language"]

            if lan is not None:
                if lan in languages:
                    languages[lan] = int(languages[lan]) + 1
                else:
                    languages[lan] = 1

        if amt < 100:
            break
        else:
            page += 1

    data["repos"] = repo_amt
    data["stars"] = stars
    data["languages"] = languages


def get_repos(url, page):
    params = {
        "per_page": "100",
        "sort": "author-date",
        "order": "desc",
        "affiliation": "owner",
        "page": page
    }

    response = requests.get(url, params=params, headers=headers)

    return response.json()


def set_key(val):
    global key

    key = "Bearer " + val


def get_public(item_type):
    items_setting = {
        "user": not s.PUBLIC,
        "repos": s.ALLOW_PRIVATE_REPOS,
        "commits": s.ALLOW_PRIVATE_COMMITS,
        "issues": s.ALLOW_PRIVATE_ISSUES,
        "requests": s.ALLOW_PRIVATE_REQUESTS,
        "reviews": s.ALLOW_PRIVATE_REVIEWS
    }

    headers["Authorization"] = key if items_setting[item_type] else ""

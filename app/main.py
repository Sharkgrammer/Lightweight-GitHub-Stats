import image as image
import github as github
import settings as s
import sys

from utils import get_test_data


def run():
    print("Starting")
    print("Accessing Github API...")

    # use the github api to get data
    github.get_user()
    github.get_repo_data()

    if s.DISPLAY_COMMITS:
        github.get_commits()

    if s.DISPLAY_REQUESTS:
        github.get_requests()

    if s.DISPLAY_REVIEWS:
        github.get_reviews()

    if s.DISPLAY_ISSUES:
        github.get_issues()

    print("Saving Image...")

    data = github.get_data()

    image.create_big_image(data)
    image.create_graph_image(data)
    image.create_stats_image(data)

    print("Complete!")


def run_with_test():
    print("Starting")
    print("Saving Image...")
    data = get_test_data()

    image.create_big_image(data)
    image.create_graph_image(data)
    image.create_stats_image(data)
    print("Complete!")


# If you don't give your api_key but don't set settings to public, auto set to public for your username
# If you set public manually, it assumes you've set PUBLIC_USER
if len(sys.argv) > 1 and not s.PUBLIC:
    s.PUBLIC_USER = sys.argv[1]

if len(sys.argv) > 2:
    github.set_key(sys.argv[2])
else:
    s.PUBLIC = True

if s.USE_TEST_DATA:
    run_with_test()
else:
    run()

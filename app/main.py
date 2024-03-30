import image as image
import github as github
import settings as s
import sys


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
    # convert data into a nice image
    image.create_image(github.get_data())
    print("Complete!")


k = sys.argv[1]

if k is not None:
    github.key = k
else:
    s.PUBLIC = True

run()

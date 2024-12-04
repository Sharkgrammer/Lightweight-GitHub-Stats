import pytest
import github as github
import settings as s

user = "octocat"


def test_url():
    text = "test"

    assert github.get_url(text) == github.base_url + text


def test_user():
    s.PUBLIC = True
    s.PUBLIC_USER = user

    github.get_user()
    data = github.get_data()

    assert data["username"] == "octocat"
    assert data["name"] == "The Octocat"


def test_repo():
    s.PUBLIC = True
    github.base_username = user

    github.get_repo_data()
    data = github.get_data()

    assert data["repos"] == 8
    assert isinstance(data["stars"], int)
    assert data["languages"] == {'Ruby': 1, 'CSS': 1, 'HTML': 1}
